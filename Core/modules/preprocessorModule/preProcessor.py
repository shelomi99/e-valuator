import spacy

nlp = spacy.load('en_core_web_md')


def main_pre_preprocess(text):
    # Extracting the sentences
    extract_sentences(text)
    # Extracting tokens of the text
    extract_tokens(text)
    # Extracting the pos tags and named entities
    extract_pos_and_namedentity(text)


def extract_tokens(text):
    doc = nlp(text)
    tokens = []

    # Extracting the tokens
    for token in doc:
        if not token.is_stop and not token.is_punct:
            tokens.append(token.text)
    return tokens


def extract_pos_and_namedentity(text):
    doc = nlp(text)
    posTags = []
    nerTags = []

    # Extracting the pos tags
    for token in doc:
        if not token.is_stop and not token.is_punct:
            posTags.append((token.text, token.tag_))

    # Extracting Named Entities
    for ent in doc.ents:
        nerTags.append((ent.text, ent.label_))
    return nerTags


def extract_sentences(text):
    doc = nlp(text)
    sentences = ""
    sentences = [sent.text for sent in doc.sents]
    return sentences

