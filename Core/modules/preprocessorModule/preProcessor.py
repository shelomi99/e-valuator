import spacy

nlp = spacy.load('en_core_web_md')


def mainPreprocess(text):
    # Extracting the sentences
    extractSentences(text)
    # Extracting tokens of the text
    extractTokens(text)
    # Extracting the pos tags and named entities
    extractPosAndNamedEntity(text)


def extractTokens(text):
    doc = nlp(text)
    tokens = []

    # Extracting the tokens
    for token in doc:
        if not token.is_stop and not token.is_punct:
            tokens.append(token.text)
    return tokens


def extractPosAndNamedEntity(text):
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


def extractSentences(text):
    doc = nlp(text)
    sentences = ""
    sentences = [sent.text for sent in doc.sents]
    return sentences

