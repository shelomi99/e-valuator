import swagger_client
from swagger_client.rest import ApiException
import requests


def generate_knowledge_graph(question_no, student_id, is_model_answer):
    # create an instance of the API class
    api_instance = swagger_client.DefaultApi()
    # String | The input natural language text.
    text = 'Dominant allele always expressed in heterozygote'
    # String | The prefix used for the namespace of terms introduced by FRED in the output
    prefix = 'e-valuator'
    # # String | The namespace used for the terms introduced by FRED in the output.
    namespace = 'http://www.ontologydesignpatterns.org/ont/e-valuator/domain.owl#'
    # Boolean | Perform Word Sense Disambiguation on input terms. By default it is set to false. (optional)
    wsd = True
    # Boolean | Perform Word Frame Disambiguation on input terms in order to provide alignments to WordNet synsets.
    wfd = True
    # String | The profile associated with the Word Frame Disambiguation (optional) (default to b)
    wfd_profile = 'b'
    # String | The vocabulary used for annotating the text in RDF. EARMARK or NIF
    text_annotation = 'earmark'
    # Boolean | Generate a RDF which only expresses the semantics of a sentence without additional RDF triples.
    semantic_subgraph = False
    try:
        headers = {
            'accept': 'application/rdf+xml',
            'Authorization': 'Bearer 06d0bc6e-9fec-3e8c-b862-34136ca9331e',
        }

        params = {
            'text': text,
            'prefix': prefix,
            'namespace': namespace,
            'wsd': wsd,
            'wfd': wsd,
            'wfd_profile': wfd_profile,
            'textannotation': text_annotation,
            'semantic-subgraph': semantic_subgraph,
        }

        response = requests.get('http://wit.istc.cnr.it/stlab-tools/fred', headers=headers, params=params)
        rdf_content = response.content
    except ApiException as e:
        print("Exception when calling DefaultApi->stlabToolsFredGet: %s\n" % e)

    if is_model_answer:
        file = open('test.owl', 'wb')
        file.write(rdf_content)
        file.close()
    return rdf_content


generate_knowledge_graph(1, 1, True)

