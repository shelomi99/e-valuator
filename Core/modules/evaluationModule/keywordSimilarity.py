import spacy
from fuzzywuzzy import process
from fuzzywuzzy.fuzz import ratio
from fuzzywuzzy import utils
from keybert import KeyBERT

nlp = spacy.load('en_core_web_md')


# keyword generation is executed when the evaluator hasn't included any keywords in the marking scheme
def generate_keywords(model_answer):
    kw_model = KeyBERT()
    # extracting the top 5 keywords
    model_keywords = kw_model.extract_keywords(model_answer, keyphrase_ngram_range=(1, 1),
                                               stop_words='english', highlight=True, top_n=10)

    # removing duplicate keywords
    extracted_keywords = list(dict(model_keywords).keys())
    print(extracted_keywords)
    return extracted_keywords


def get_fuzzy_keyword_similarity(student_answer=None, model_answer=None, dictionary=None):
    # check if keyword list is empty
    is_keywords_empty = not (bool(dictionary))
    if is_keywords_empty:
        dictionary = generate_keywords(model_answer)
    doc = nlp(student_answer)
    tokens = []
    keyword_similarity = []
    matched_keywords = []
    expected_num_of_keywords = len(dictionary)
    matched_num_of_keywords = 0
    keyword_similarity_score = 0
    # extracting tokens
    for token in doc:
        if not token.is_stop:
            tokens.append(token.text.lower())

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

    # to remove empty lists
    similarity = [x for x in keyword_similarity if x]
    for x in range(len(similarity)):
        matched_keywords.append(similarity[x][0][0])

    try:
        # 20% of the total score is allocated for the keyword similarity score
        keyword_similarity_score = "{:.2f}".format((len(matched_keywords) / expected_num_of_keywords) * 20)
    except ZeroDivisionError:
        keyword_similarity_score = 0

    return dictionary, matched_keywords, float(keyword_similarity_score)


# # # testing method
# test_student = "this sentence is wrong Photosynthesis"
# test_model = "Photosynthesis is the process by which plants use, water, and carbon to create and energy in the form of."
#
# required_keywords, matched_keyword, keyword_similarity_score = get_fuzzy_keyword_similarity(test_student, test_model,
#                                                                                             ["Photosynthesis"])
# print(required_keywords)
# print(matched_keyword)
# print(keyword_similarity_score)
