from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from Core.modules.evaluationModule.finalScoreCalculation import calculate_final_score
from Core.modules.evaluationModule.keywordSimilarity import get_fuzzy_keyword_similarity
from Core.modules.evaluationModule.stringMatchSimilarity import stringSimilarity
from Core.modules.graphGeneratorModule.knowledgeGraphGenerator import generate_knowledge_graph_similarity

app = Flask(__name__)
CORS(app, resources={r"/": {"origins": ""}})


@app.route('/', methods=["GET"])
@cross_origin()
def get_form_data():
    keywords = []
    id = request.args.get('id')
    question_number = request.args.get('questionNumber')
    question = request.args.get('question')
    marks_allocated = request.args.get('marks')
    model_answer = request.args.get('modelAnswer')
    student_answer = request.args.get('studentAnswer')
    keywords = request.args.get('keywords')
    if len(keywords) > 0:
        keywords = keywords.split(",")
    else:
        keywords = keywords
    # calculating keyword similarity score
    required_keywords, matched_keyword, keyword_similarity_score = get_fuzzy_keyword_similarity(student_answer,
                                                                                                model_answer, keywords)
    # calculating string similarity
    string_similarity = stringSimilarity(model_answer, student_answer)
    # calculating semantic similarity
    semantic_similarity = generate_knowledge_graph_similarity(model_answer, student_answer, 10, 1)
    if keyword_similarity_score == 0 and string_similarity == 0:
        semantic_similarity = 0
    mark_percentage = keyword_similarity_score + string_similarity + semantic_similarity
    rounded_percentage, final_mark = calculate_final_score(mark_percentage, marks_allocated)
    output_values = jsonify(required_keywords=required_keywords,
                            matched_keyword=matched_keyword,
                            keyword_similarity_score=keyword_similarity_score,
                            string_similarity_score=string_similarity,
                            semantic_similarity_score=semantic_similarity,
                            total_mark_percentage=mark_percentage,
                            final_mark=final_mark)
    return output_values


if __name__ == "__main__":
    app.run(debug=True)
