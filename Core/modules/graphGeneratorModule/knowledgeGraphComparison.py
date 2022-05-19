import re

import requests
import spacy
from SPARQLWrapper import SPARQLWrapper, JSON

model_answer_spo = []
student_answer_spo = []
model_answer_spo_list = []
student_answer_spo_list = []


def upload_rdf_file(complete_file_name, question_no, student_id, model_answer, student_answer):
    # dataset is named in the format of {questionNumber}_model
    dataset_name = str(question_no) + "_model"
    # Url of the Apache jena fuseki server
    FUSEKI_SERVER_URL = "http://localhost:3030/" + dataset_name

    serviceURL = FUSEKI_SERVER_URL
    # locally saved owl file
    add_data = open(complete_file_name).read()
    add_data_headers = {'Content-Type': 'application/rdf+xml;charset=utf-8'}
    create_dataset_header = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    # setting fuseki db values
    create_data = {
        'dbName': dataset_name,
        'dbType': 'mem',
    }
    # create new dataset
    response = requests.post('http://localhost:3030/$/datasets', headers=create_dataset_header, data=create_data)
    # Upload generated OWL file to the fuseki server
    request = requests.post(serviceURL, data=add_data, headers=add_data_headers)
    # get knowledge graph similarity
    semantic_similarity_score = knowledgeGraphSimialrityRatio(serviceURL, student_answer, model_answer)

    return semantic_similarity_score


def format_token(token):
    # Making the literal lower cased
    formatToken = token.lower()
    # Removing all new line and tab chars from literal
    formatToken = formatToken.replace("\n", "")
    formatToken = formatToken.replace("\t", "")
    formatToken = formatToken.replace('"', "")
    formatToken = formatToken.replace("'", "")
    formatToken = formatToken.replace("’", "")
    formatToken = formatToken.replace(".", "")
    formatToken = formatToken.replace("/", "")
    formatToken = formatToken.replace("-", "")
    formatToken = formatToken.replace("\\", "")
    formatToken = formatToken.replace(",", "")
    formatToken = formatToken.replace("'", "")
    formatToken = formatToken.replace("(", "")
    formatToken = formatToken.replace(")", "")
    # Return formatedLiteral
    return formatToken


def knowledgeGraphSimialrityRatio(server_url, student_answer, model_answer):
    nlp = spacy.load('en_core_web_md')
    model_answer_tokens = []
    student_answer_tokens = []
    words_present = 0
    total_words = 0
    answer_spo_list = []

    model_answer_doc = nlp(model_answer)
    for token_model in model_answer_doc:
        if not token_model.is_stop:
            model_answer_tokens.append(token_model.text)

    total_words = len(set(model_answer_tokens))
    # Url of the Apache jena fuseki server
    FUSEKI_SERVER_URL = server_url

    student_answer_doc = nlp(student_answer)
    for token in student_answer_doc:
        if not token.is_stop:
            student_answer_tokens.append(token.text)

    for token in set(student_answer_tokens):
        token = format_token(str(token))
        query = """
        SELECT
        ?subject ?predicate ?object
        WHERE {{ 
            ?subject ?predicate ?object
            .FILTER regex(str(?subject), "{token}", "i") 
      .}}
      """

        sparql = SPARQLWrapper(FUSEKI_SERVER_URL)
        sparql.setQuery(query.format(token=token))
        sparql.setReturnFormat(JSON)
        results = sparql.query()
        converted = results.convert()

        if converted["results"]["bindings"]:
            words_present += 1

    knowledge_graph_similarity = "{:.2f}".format((words_present / total_words) * 40)
    return float(knowledge_graph_similarity)


def rdf_triple_extraction(server_url, spos, spo_list):
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT *
    WHERE {{
   ?entity rdfs:label ?name . }}
    """

    # qyery for extraction
    sparql = SPARQLWrapper(server_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query()
    converted_answer = results.convert()

    for entry in range(len(converted_answer["results"]["bindings"])):
        spos.append((converted_answer['results']['bindings'][entry]['entity']['value']))

    return spos


# convert a list of tokens to a string
def to_str(tokens):
    return ' '.join([item.text for item in tokens])


# def identifyCommonClasses():
#     model_rdf_list = rdf_triple_extraction(FUSEKI_SERVER_URL_MODEL, model_answer_spo, model_answer_spo_list)
#     student_rdf_list = rdf_triple_extraction(FUSEKI_SERVER_URL_STUDENT, student_answer_spo, student_answer_spo_list)
#
#     print("model answer class list", model_rdf_list)
#     print("student answer class list", student_rdf_list)
#
#     # identify common classes between the two corpses
#     common_classes = set(model_rdf_list).intersection(student_rdf_list)
