import requests
import spacy
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
request = requests.post(serviceURL, data=data, headers=headers)


def formatToken(token):
    # Making the literal lower cased
    formatToken = token.lower()
    # Removing all new line and tab chars from literal
    formatToken = formatToken.replace("\n", "")
    formatToken = formatToken.replace("\t", "")
    formatToken = formatToken.replace('"', "")
    formatToken = formatToken.replace("'", "")
    formatToken = formatToken.replace("’", "")
    formatToken = formatToken.replace(".", "")
    # Return formatedLiteral
    return formatToken


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


model_rdf_list = rdf_triple_extraction(FUSEKI_SERVER_URL_MODEL, model_answer_spo, model_answer_spo_list)
student_rdf_list = rdf_triple_extraction(FUSEKI_SERVER_URL_STUDENT, student_answer_spo, student_answer_spo_list)

print("model answer class list", model_rdf_list)
print("student answer class list", student_rdf_list)

# identify common classes between thw two corpses
common_classes = set(model_rdf_list).intersection(student_rdf_list)


def knowledgeGraphSimialrityRatio(text, ):
    # convert a list of tokens to a string
    def to_str(tokens):
        return ' '.join([item.text for item in tokens])

    nlp = spacy.load('en_core_web_md')
    # declaring the students scheme
    text = "A dominant allele is the allele that is always expressed while the recessive allele is only expressed when it has 2 copies of the allele"
    tokens = []
    words_present = 0
    total_words = 0
    answer_spo_list = []

    Doc = nlp(text)
    for token in Doc:
        if not token.is_stop:
            tokens.append(token.text)

    total_words = len(set(tokens))
    # Name of dataset
    DATASET_NAME = "ds"
    # Url of the Apache jena fuseki server
    FUSEKI_SERVER_URL = "http://localhost:3030/" + DATASET_NAME

    for token in set(tokens):
        token = formatToken(token)
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

    print(words_present)
    print(total_words)
