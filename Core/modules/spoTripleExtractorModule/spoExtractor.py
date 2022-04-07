import spacy

nlp = spacy.load('en_core_web_md')

# dependency markers for subjects
SUBJECTS_LIST = {"nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"}
# dependency markers for objects
OBJECTS_LIST = {"dobj", "dative", "attr", "oprd"}
# POS tags that will break adjoining items
BREAKER_POS = {"CCONJ", "VERB"}
# words that are negations
NEGATIONS = {"no", "not", "n't", "never", "none"}
spos = []

model_answer = "Oxygen enters the blood through diffusion into the alveoli. This is because alveoli has a high " \
               "concentration of O2. Blood has a low concentration of O2 so the oxygen diffuses into the blood "


# check if the token is a verb  (excluding auxiliary verbs)
def is_non_aux_verb(tok):
    return tok.pos_ == "VERB" and (tok.dep_ != "aux" and tok.dep_ != "auxpass")


# get all the functional subjects adjacent to the verb passed in
def get_all_subs(v):
    verb_negated = is_negated(v)
    subs = [tok for tok in v.lefts if tok.dep_ in SUBJECTS_LIST and tok.pos_ != "DET"]
    if len(subs) > 0:
        subs.extend(get_subs_from_conjunctions(subs))
    else:
        foundSubs, verb_negated = find_subs(v)
        subs.extend(foundSubs)
    return subs, verb_negated


# returns a tuple, first part True|False and second part the modified verb if True
def right_of_verb_is_conj_verb(v):
    # rights is a generator
    rights = list(v.rights)

    # VERB CCONJ VERB (e.g. he beat and hurt me)
    if len(rights) > 1 and rights[0].pos_ == 'CCONJ':
        for tok in rights[1:]:
            if is_non_aux_verb(tok):
                return True, tok

    return False, v


# get all objects for an active/passive sentence
def get_all_objs(v, is_pas):
    # rights is a generator
    rights = list(v.rights)

    objs = [tok for tok in rights if tok.dep_ in OBJECTS_LIST or (is_pas and tok.dep_ == 'pobj')]
    objs.extend(get_objs_from_prepositions(rights, is_pas))

    potential_new_verb, potential_new_objs = get_obj_from_xcomp(rights, is_pas)
    if potential_new_verb is not None and potential_new_objs is not None and len(potential_new_objs) > 0:
        objs.extend(potential_new_objs)
        v = potential_new_verb
    if len(objs) > 0:
        objs.extend(get_objs_from_conjunctions(objs))
    return v, objs


# is the tok set's left or right negated?
def is_negated(tok):
    parts = list(tok.lefts) + list(tok.rights)
    for dep in parts:
        if dep.lower_ in NEGATIONS:
            return True
    return False


# xcomp; open complement - verb has no suject
def get_obj_from_xcomp(deps, is_pas):
    for dep in deps:
        if dep.pos_ == "VERB" and dep.dep_ == "xcomp":
            v = dep
            rights = list(v.rights)
            objs = [tok for tok in rights if tok.dep_ in OBJECTS_LIST]
            objs.extend(get_objs_from_prepositions(rights, is_pas))
            if len(objs) > 0:
                return v, objs
    return None, None


# get objects joined by conjunctions
def get_objs_from_conjunctions(objs):
    more_objs = []
    for obj in objs:
        # rights is a generator
        rights = list(obj.rights)
        rightDeps = {tok.lower_ for tok in rights}
        if contains_conj(rightDeps):
            more_objs.extend([tok for tok in rights if tok.dep_ in OBJECTS_LIST or tok.pos_ == "NOUN"])
            if len(more_objs) > 0:
                more_objs.extend(get_objs_from_conjunctions(more_objs))
    return more_objs


# convert a list of tokens to a string
def to_str(tokens):
    return ' '.join([item.text for item in tokens])


# resolve a 'that' where/if appropriate
def get_that_resolution(toks):
    for tok in toks:
        if 'that' in [t.orth_ for t in tok.lefts]:
            return tok.head
    return toks


# expand an obj / subj np using its chunk
def expand(item, tokens, visited):
    if item.lower_ == 'that':
        item = get_that_resolution(tokens)

    parts = []

    if hasattr(item, 'lefts'):
        for part in item.lefts:
            if part.pos_ in BREAKER_POS:
                break
            if not part.lower_ in NEGATIONS:
                parts.append(part)

    parts.append(item)

    if hasattr(item, 'rights'):
        for part in item.rights:
            if part.pos_ in BREAKER_POS:
                break
            if not part.lower_ in NEGATIONS:
                parts.append(part)

    if hasattr(parts[-1], 'rights'):
        for item2 in parts[-1].rights:
            if item2.pos_ == "DET" or item2.pos_ == "NOUN":
                if item2.i not in visited:
                    visited.add(item2.i)
                    parts.extend(expand(item2, tokens, visited))
            break

    return parts


# does dependency set contain any coordinating conjunctions?
def contains_conj(depSet):
    return "and" in depSet or "or" in depSet or "nor" in depSet or \
           "but" in depSet or "yet" in depSet or "so" in depSet or "for" in depSet


# get subs joined by conjunctions
def get_subs_from_conjunctions(subs):
    more_subs = []
    for sub in subs:
        # rights is a generator
        rights = list(sub.rights)
        rightDeps = {tok.lower_ for tok in rights}
        if contains_conj(rightDeps):
            more_subs.extend([tok for tok in rights if tok.dep_ in SUBJECTS_LIST or tok.pos_ == "NOUN"])
            if len(more_subs) > 0:
                more_subs.extend(get_subs_from_conjunctions(more_subs))
    return more_subs


# find sub dependencies
def find_subs(tok):
    head = tok.head
    while head.pos_ != "VERB" and head.pos_ != "NOUN" and head.head != head:
        head = head.head
    if head.pos_ == "VERB":
        subs = [tok for tok in head.lefts if tok.dep_ == "SUB"]
        if len(subs) > 0:
            verb_negated = is_negated(head)
            subs.extend(get_subs_from_conjunctions(subs))
            return subs, verb_negated
        elif head.head != head:
            return find_subs(head)
    elif head.pos_ == "NOUN":
        return [head], is_negated(tok)
    return [], False


# get grammatical objects for a given set of dependencies (including passive sentences)
def get_objs_from_prepositions(deps, is_pas):
    objs = []
    for dep in deps:
        if dep.pos_ == "ADP" and (dep.dep_ == "prep" or (is_pas and dep.dep_ == "agent")):
            objs.extend([tok for tok in dep.rights if tok.dep_ in OBJECTS_LIST or
                         (tok.pos_ == "PRON" and tok.lower_ == "me") or
                         (is_pas and tok.dep_ == 'pobj')])
    return objs

# get all the subject predicate object list from
def get_spo_triples(text):
    fullText = nlp(text)

    # Getting all verbs excluding auxiliary verbs
    verbs = [tok for tok in fullText if is_non_aux_verb(tok)]
    # Visited set for recursion detection
    visited = set()

    # Looping through all the verbs
    for v in verbs:
        # Getting all functional subjects adjacent to the verb passed in and check if verb is negated
        subs, verbNegated = get_all_subs(v)

        # If no subjects, don't examine this verb any longer
        if len(subs) > 0:
            # Return the verb to the right of this verb in a CCONJ relationship if applicable
            isConjVerb, conjV = right_of_verb_is_conj_verb(v)

            if isConjVerb:
                # Getting all objects
                v2, objs = get_all_objs(conjV, False)

                for sub in subs:
                    for obj in objs:
                        objNegated = is_negated(obj)
                        spos.append((to_str(expand(sub, fullText, visited)),
                                     "!" + v.lower_ if verbNegated or objNegated else v.lower_,
                                     to_str(expand(obj, fullText, visited))))
                        spos.append((to_str(expand(sub, fullText, visited)),
                                     "!" + v2.lower_ if verbNegated or objNegated else v2.lower_,
                                     to_str(expand(obj, fullText, visited))))
            else:
                v, objs = get_all_objs(v, False)
                for sub in subs:
                    for obj in objs:
                        objNegated = is_negated(obj)
                        spos.append((to_str(expand(sub, fullText, visited)),
                                     "!" + v.lower_ if verbNegated or objNegated else v.lower_,
                                     to_str(expand(obj, fullText, visited))))

    return spos
