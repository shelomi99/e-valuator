import os
from Core.config import Config
import requests

from Core.modules.graphGeneratorModule.knowledgeGraphComparison import upload_rdf_file


def generate_knowledge_graph_similarity(model_answer, student_answer, question_no, student_id):
    # Initializing the params
    API_KEY = Config.API_KEY
    # The input natural language text.
    text = model_answer
    # The prefix used for the namespace of terms introduced by FRED in the output
    prefix = 'e-valuator'
    # The namespace used for the terms introduced by FRED in the output.
    namespace = 'http://www.ontologydesignpatterns.org/ont/e-valuator/domain.owl#'
    # Perform Word Sense Disambiguation on input terms.
    wsd = True
    # Perform Word Frame Disambiguation on input terms in order to provide alignments to WordNet synsets.
    wfd = True
    # The profile associated with the Word Frame Disambiguation (default to b)
    wfd_profile = 'b'
    # The vocabulary used for annotating the text in RDF. EARMARK or NIF
    text_annotation = 'earmark'
    # Generate a RDF which only expresses the semantics of a sentence without additional RDF triples.
    semantic_subgraph = False
    # Generating RDF files
    try:
        headers = {
            'accept': 'application/rdf+xml',
            'Authorization': API_KEY,
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
    except Exception as e:
        print("Exception when calling stlabToolsFredGet: %s\n" % e)

    filename = str(student_id) + "_" + str(question_no)
    filename = filename + "_model" + ".owl"
    complete_file_name = os.path.join('C:\\Shelomi\\Final year\\E-Valuator\\e-valuator\\Core\\modules\\graphGeneratorModule\\rdfFiles\\modelAnswers', filename)
    file = open(complete_file_name, 'wb')

    file.write(rdf_content)
    file.close()

    # upload rdf file to fuseki server
    rdf_file = upload_rdf_file(complete_file_name, question_no, student_id, text, student_answer)
    return rdf_file


# test method
# generate_knowledge_graph_similarity("Goblet cells release mucus. Mucus traps dirt. Cilia beat to move fluid of airway.", " Mucus traps dirt", 5, 1)