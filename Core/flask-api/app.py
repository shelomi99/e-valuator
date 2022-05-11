from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

from Core.modules.evaluationModule.finalScoreCalculation import calculate_final_score
from Core.modules.evaluationModule.keywordSimilarity import get_fuzzy_keyword_similarity
from Core.modules.evaluationModule.stringMatchSimilarity import get_string_similarity
from Core.modules.graphGeneratorModule.knowledgeGraphGenerator import generate_knowledge_graph_similarity

app = Flask(__name__)
CORS(app, resources={r"/": {"origins": ""}})

# Add configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///results.db'
app.config['SECRET_KEY'] = '2018576'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Create the DB
db = SQLAlchemy(app)


class Results(db.Model):
    result_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer)
    question_number = db.Column(db.String)
    question = db.Column(db.String)
    given_mark = db.Column(db.String)
    mark_allocated = db.Column(db.String)


def validate_mark(keyword_similarity_score, string_similarity, semantic_similarity):
    if keyword_similarity_score == 0 and string_similarity == 0:
        string_similarity = 0
    if keyword_similarity_score == 0 and semantic_similarity == 0:
        string_similarity = 0
    if keyword_similarity_score == 20 and semantic_similarity == 40:
        string_similarity = 40

    return keyword_similarity_score, string_similarity, semantic_similarity


@app.route('/', methods=["GET"])
@cross_origin()
def get_form_data():
    keywords = []
    incorrect_questions = []
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
    string_similarity = get_string_similarity(model_answer, student_answer)
    # calculating semantic similarity
    semantic_similarity = generate_knowledge_graph_similarity(model_answer, student_answer, question_number, id)

    val_keyword_similarity_score, val_string_similarity, val_semantic_similarity = validate_mark(keyword_similarity_score, string_similarity, semantic_similarity)
    mark_percentage = val_keyword_similarity_score + val_string_similarity + val_semantic_similarity
    rounded_percentage, final_mark = calculate_final_score(mark_percentage, marks_allocated)
    if mark_percentage < 30:
        incorrect_questions.append(question)
    output_values = jsonify(required_keywords=required_keywords,
                            matched_keyword=matched_keyword,
                            keyword_similarity_score=val_keyword_similarity_score,
                            string_similarity_score=val_string_similarity,
                            semantic_similarity_score=val_semantic_similarity,
                            total_mark_percentage=mark_percentage,
                            final_mark=final_mark,
                            incorrect_questions=incorrect_questions,
                            marks_allocated=marks_allocated)
    return output_values


@app.route('/add', methods=['GET'])
@cross_origin()
# Add result to the database
def add_results():
    student_id = request.args.get('id')
    question_number = request.args.get('questionNumber')
    question = request.args.get('question')
    given_mark = request.args.get('givenMarks')
    marks_allocated = request.args.get('marksAllocated')
    results = Results(student_id=student_id, question_number=question_number, question=question, given_mark=given_mark,
                      mark_allocated=marks_allocated)
    db.session.add(results)
    db.session.commit()

    return 'Result Added Successfully'


@app.route('/get', methods=['GET'])
@cross_origin()
def get_student_ids():
    id_list = []
    filtered_id_list = []
    all_results = Results.query.order_by(Results.student_id).all()
    for result in all_results:
        id_list.append(result.student_id)
        for i in id_list:
            if i not in filtered_id_list:
                filtered_id_list.append(i)
        # id_list[result.result_id] = result.student_id
    return jsonify(filtered_id_list)


@app.route('/get-marks', methods=['GET'])
@cross_origin()
def get_marks_from_id():
    final_results = []
    marks = {}
    student_id = request.args.get('id')

    all_results = Results.query.filter(Results.student_id == student_id).order_by(Results.question_number).all()
    for questions in all_results:
        question = Results.query.filter(Results.result_id == questions.result_id).all()
        for mark in question:
            marks['question_number'] = mark.question_number
            marks['given_mark'] = mark.given_mark
            marks['allocated_mark'] = mark.mark_allocated
            dictionary_copy = marks.copy()
            final_results.append(dictionary_copy)
    return jsonify(final_results)


if __name__ == "__main__":
    app.run(debug=True)
