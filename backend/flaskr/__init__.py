import os
import random
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_question = questions[start:end]

    return current_question



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    @app.route("/", methods=["GET"])
    def get_example():
        """GET in server"""
        response = jsonify(message="Simple server is running")
        # Enable Access-Control-Allow-Origin
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    # CORS Headers
    @app.after_request
    def after_request(response):
        #response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        return response

    """
    @TODO: Create an endpoint to handle GET requests for all available categories.
    """
    @app.route("/categories")
    def retrieve_categories():
        try: 
            cat_dict = {}
            categories = Category.query.order_by(Category.id).all()
            for category in categories:
                cat = category.format()
                cat_dict.update(cat)

            return jsonify(
                {
                    "success": True,
                    "categories": cat_dict,
                    "total_category": len(Category.query.all()),
                }
            )
        except:
            abort(405)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions")
    def retrieve_questions():
        cat_dict = {}
        categories = Category.query.order_by(Category.id).all()
        for category in categories:
            cat = category.format()
            cat_dict.update(cat)
        try: 
            selection = Question.query.order_by(Question.id).all()
            current_question = paginate_questions(request, selection)

            if len(current_question) == 0:
                abort(404)

            return jsonify(
                {
                    "success": True,
                    "questions": current_question,
                    "totalQuestions": len(Question.query.all()),
                    "categories": cat_dict,
                }
            )
        except:
            abort(404)
        

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        #format for delete command
        #curl -X DELETE http://127.0.0.1:5000/questions/8 
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                abort(404)

            question.delete()
            # selection = Question.query.order_by(Question.id).all()
            # current_questions = paginate_questions (request, selection)

            return jsonify(
                {
                    "id": question_id,
                    "message": "Delete completed",
                    "success": True,
                }
            )
        except:
            abort(404)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def new_question():
        #POST command format
        #curl -X POST -H "Content-Type: application/json" -d '{"question":"What is an API", "answer":"Application Programming Interface", "difficulty":"3", "category":"1"}' http://127.0.0.1:5000/questions  
        body = request.get_json()
        if "question" in body and "answer" in body and "difficulty" in body and "category" in body: 
            question= body.get("question", None)
            answer= body.get("answer", None)
            difficulty= body.get("difficulty", None)
            category= body.get("category", None)
        else:
            abort(400)

        try:
            add_question = Question(question=question, answer=answer, difficulty=difficulty, category=category)
            add_question.insert()

            selection = Question.query.order_by(Question.id.desc()).first()
            #filter(Question.id == Question.query(func.max(Question.id)))
            return jsonify(
                {
                    "success": True,
                    "question": selection.format(),
                    "total_questions": len(Question.query.all()),
                    "created": selection.id
                }
            )

        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questions/search", methods=["POST"])
    def search_question():
        #the endpoint above will return a result if the user specified the searchword parameter properly
        #curl -X POST -H "Content-Type: application/json" -d '{"searchTerm":"What is an API"}' http://127.0.0.1:5000/questions/search
        body = request.get_json()
        #checks if the search parameter is in the body
        if "searchTerm" in body:
            searchTerm = body.get("searchTerm", None)
        else:
            #if not return unprocessable
            abort(404)

        try:
            selection = Question.query.filter(Question.question.ilike
                                                  (f'%{searchTerm}%')).all()
            #selection = Question.query.filter(Question.question.ilike(searchTerm)).all()
            question = [question.format() for question in selection]
            #check if the result of the query is empty
            if selection == '':
                abort(404)
            else:
                return jsonify(
                    {
                        "success": True,
                        "questions": question,
                        "totalQuestions": len(selection),
                        "currentCategory": 'History'
                    }
                )
        except:
            abort(405)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the categories in the left column will cause only questions of that category to be shown.
    """
    @app.route("/categories/<int:cat>/questions", methods=['GET'])
    def get_question(cat):
        #curl http://127.0.0.1:5000/categories/1/questions  
        category = Category.query.get(cat)
        category = category.type
        try:
            selection = Question.query.order_by(Question.id).filter(Question.category==cat)
            current_question = paginate_questions(request, selection)
            return jsonify(
                {
                    "success": True,
                    "questions": current_question,
                    "totalQuestions": len(selection.all()),
                    "currentCategory": category
                }
            )
                
        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category, one question at a time is displayed, the user is allowed to answer and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=['POST'])
    def play_quiz():
        try:
            body = request.get_json()
            quiz_category = body.get('quiz_category', None)
            previous_questions = body.get('previous_questions', None)

            category_id = quiz_category["id"]
            if category_id:
                questions = Question.query.filter(Question.id.notin_(previous_questions),Question.category==category_id).all()
            else:
                questions = Question.query.filter(Question.id.notin_(previous_questions)).all()

            if not questions: 
                question = None
                abort(404)
            else: 
                question = random.choice(questions)

            formatted_question = question.format()
            return jsonify({
                'success': True,
                'question': formatted_question
            })

        except:
            abort(400)
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                "success": False, 
                "error": 404,
                "message": "resource not found"
            }), 404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({
                "success": False, 
                "error": 422, 
                "message": "unprocessable: invalid parameter"
            }), 422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400, 
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({
                "success": False, 
                "error": 405, 
                "message": "method not allowed"
            }), 405,
        )

    @app.errorhandler(500)
    def server_error(error):
        return (
            jsonify({
                "success": False, 
                "error": 500, 
                "message": "Internal server error"
            }), 500,
        )

    return app

