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

    print("Tokens --> ", tokens, "\n")


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

    print("POS tags --> ", posTags, "\n")
    print("NER tags --> ", nerTags, "\n")


def extractSentences(text):
    doc = nlp(text)
    sentences = ""
    sentences = [sent.text for sent in doc.sents]
    print("Sentences --> ", sentences, "\n")

