import spacy
from fuzzywuzzy import process
from fuzzywuzzy.fuzz import ratio
from fuzzywuzzy import utils
from keybert import KeyBERT

nlp = spacy.load('en_core_web_md')


# keyword generation is executed when the evaluator hasn't included any keywords in the marking scheme
def generateKeywords(text):
    kw_model = KeyBERT()
    # extracting the top 5 keywords
    model_keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 1),
                                               stop_words='english', highlight=True, top_n=10)

    # removing duplicate keywords
    extracted_keywords = list(dict(model_keywords).keys())
    print(extracted_keywords)
    return extracted_keywords


def get_fuzzy_keyword_similarity(text=None, dictionary=None):
    doc = nlp(text)
    tokens = []
    keyword_similarity = []
    expected_num_of_keywords = len(dictionary)
    matched_num_of_keywords = 0
    keyword_similarity_score = 0
    for token in doc:
        if not token.is_stop:
            tokens.append(token.text)

    # removing duplicates in the token list
    cleaned_token_list = (list(dict.fromkeys(tokens)))

    for token in cleaned_token_list:
        if token and dictionary:
            if utils.full_process(token):
                keyword_similarity.append(process.extractBests(token, dictionary, scorer=ratio, score_cutoff=70))
        else:
            return []

    for item in keyword_similarity:
        for i in item:
            matched_num_of_keywords += 1

    keyword_similarity_score = "{:.2f}".format(expected_num_of_keywords / matched_num_of_keywords)
    print("expected_num_of_keywords =", expected_num_of_keywords)
    print("matched_num_of_keywords =", matched_num_of_keywords)
    print("keyword_similarity_score = ", keyword_similarity_score)
    # to remove empty lists
    similarity = [x for x in keyword_similarity if x]
    return similarity
