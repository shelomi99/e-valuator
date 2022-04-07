import requests
from SPARQLWrapper import SPARQLWrapper, JSON

MODEL_DATASET_NAME = "ds"
STUDENTL_DATASET_NAME = "test"

# Url of the Apache jena fuseki server
FUSEKI_SERVER_URL_MODEL = "http://localhost:3030/" + MODEL_DATASET_NAME
FUSEKI_SERVER_URL_STUDENT = "http://localhost:3030/" + STUDENTL_DATASET_NAME
model_answer_spo = []
student_answer_spo = []
model_answer_spo_list = []
student_answer_spo_list = []

# Upload generated RDF graph to the fuseki server
serviceURL = FUSEKI_SERVER_URL_MODEL
data = open('rdfFiles/test.owl').read()
headers = {'Content-Type': 'application/rdf+xml;charset=utf-8'}
# r = requests.post(serviceURL, data=data, headers=headers)
rtest = requests.delete(serviceURL, headers=headers)

# def rdf_triple_extraction(server_url, spos, spo_list):
#     query = """
#     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#     SELECT *
#     WHERE {{
#    ?entity rdfs:label ?name . }}
#
#     """
#
#     # qyery forextraction
#     sparql = SPARQLWrapper(server_url)
#     sparql.setQuery(query)
#     sparql.setReturnFormat(JSON)
#     results = sparql.query()
#     converted_answer = results.convert()
#
#     for entry in range(len(converted_answer["results"]["bindings"])):
#         spos.append((converted_answer['results']['bindings'][entry]['entity']['value']))
#
#     return spos
#
#
# model_rdf_list = rdf_triple_extraction(FUSEKI_SERVER_URL_MODEL, model_answer_spo, model_answer_spo_list)
# student_rdf_list = rdf_triple_extraction(FUSEKI_SERVER_URL_STUDENT, student_answer_spo, student_answer_spo_list)
#
# print("model answer class list", model_rdf_list)
# print("student answer class list", student_rdf_list)
#
# # identify common classes between thw two corpuses
# common_classes = set(model_rdf_list).intersection(student_rdf_list)
