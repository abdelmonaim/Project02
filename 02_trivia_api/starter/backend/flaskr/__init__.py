import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, all_questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in all_questions]
    current_questions_view = questions[start:end]

    return current_questions_view


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    '''
    # @TODO: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    '''
    CORS(app)

    # @TODO: Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
    # @TODO: Create an endpoint to handle GET requests
    for all available categories.
    '''

    @app.route('/categories', methods=['GET'])
    def get_categories():
        all_categories = Category.query.order_by(Category.id).all()
        categories = [category.format() for category in all_categories]

        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': {category.id: category.type
                           for category in all_categories},
            'all_categories': len(Category.query.all())
        })

    ''' @TODO: Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    TEST: At this point, when you start the application you should see
    questions and categories generated, ten questions per page and
    pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. '''

    @app.route('/questions', methods=['GET'])
    def get_questions():
        all_questions = Question.query.order_by(Question.id).all()
        current_questions_view = paginate_questions(request, all_questions)

        all_categories = Category.query.order_by(Category.id).all()
        categories = [category.format() for category in all_categories]
        # cate = [cat['type'] for cat in categories]
        # print(cate)
        if len(current_questions_view) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions_view,
            'total_questions': len(Question.query.all()),
            'current_category': None,
            'categories': {category.id: category.type
                           for category in all_categories}
        })

    '''

    @app.route('/questions', methods=['GET'])
    def get_questions():
        categories=[]
        temp_list=[]
        questions=Question.query.all()
        current_question=paginate_questions(request,questions)
        for cat_id in current_question:
            category=Category.query.get(cat_id['category'])
            if not(cat_id['category'] in temp_list):
                categories.append(category.type)
            temp_list.append(cat_id['category'])
        print(categories)
        return jsonify({
            'success': True,
            'question': current_question,
            'total_questions': len(current_question),
            'category': categories# ['Science', 'Art', 'Geography', 'History', 'Entertainment', 'Sports']
        })
        
    '''
    ''' @TODO: Create an endpoint to DELETE question using a question_ID.
    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question_by_id(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except:
            abort(422)

    '''@TODO: Create an endpoint to POST a new question, which will require
    the question and answer text, category, and difficulty score.
    TEST: When you submit a question on the "Add" tab, the form will clear
    and the question will appear at the end of the last page of the
    questions list in the "List" tab. '''
    '''@TODO: Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term is a substring
    of the question. TEST: Search by any phrase.
    The questions list will update to include only question that include
    that string within their question. Try using the word "title" to start.'''

    @app.route('/questions', methods=['POST'])
    def create_search_question():
        body = request.get_json()
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_score = body.get('difficulty', None)
        search = body.get('searchTerm', None)
        try:
            if search:
                search_query = Question.query.filter(
                    Question.question.ilike('%{}%'.format(search)))
                # print('Total number of entities found using search term: ' + str(search_query.count()))
                if search_query.count() == 0:
                    # print('Inside of the abort condition.')
                    abort(422)
                # print('Out of the abort condition')
                search_query_formatted = [query_formatted.format()
                                          for query_formatted in search_query]
                return jsonify({
                    'questions': search_query_formatted,
                    'total_search_questions': len(search_query_formatted),
                    'current_category': 'All'
                })
            else:
                if len(new_question) == 0 or len(new_answer) == 0 or int(
                        new_category) <= 0 or int(new_score) < 0 or int(
                    new_score) > 5:
                    abort(422)
                question = Question(question=new_question,
                                    answer=new_answer,
                                    category=new_category,
                                    difficulty=new_score)
                question.insert()
                return jsonify({
                    'success': True,
                    'question': new_question,
                    'answer': new_answer,
                    'total_number_of_questions': len(Question.query.all())
                })
        except:
            abort(422)

    '''@TODO: Create a GET endpoint to get questions based on category.
    TEST: In the "List" tab / main screen, clicking on one of the categories
    in the left column will cause only questions of that category to be shown.
    '''

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        questions = Question.query.filter(
            Question.category == category_id)
        if Category.query.filter(Category.id == category_id) \
                .one_or_none() is None:
            abort(404)
        current_questions_view = paginate_questions(request, questions)
        # print(current_questions_view)
        return jsonify({
            'success': True,
            'questions': current_questions_view,
            'total_questions': questions.count(),
            'current_category': category_id
        })

    '''@TODO: Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters and
    return a random questions within the given category, if provided,
    and that is not one of the previous questions. TEST: In the "Play" tab,
    after a user selects "All" or a category, one question at a time is
    displayed, the user is allowed to answer and
    shown whether they were correct or not. '''

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        force_end = False
        body = request.get_json()
        category_id = int(body.get('quiz_category')['id'])

        # print('Selected category is: ' + str(category_id))

        if category_id == 0:
            all_questions = Question.query.all()
        else:
            all_questions = Question.query.filter(
                Question.category == category_id)

        if category_id > len(Category.query.all()):
            abort(404)
        # print('Questions before formatting: ')
        # print(all_questions)

        # all_questions = get_questions_by_category(
        # int(body.get('quiz_category')['id'])+1)
        formatted_question = [question.format() for question in all_questions]
        # print('Questions after formatting: ')
        # print(formatted_question)

        previous_questions = body.get('previous_questions', None)
        # print('Previous questions')
        # print(previous_questions)

        remaining_questions_per_category = []
        formatted_questions_id = []
        for question_id in formatted_question:
            formatted_questions_id.append(int(question_id['id']))
        # print('Formatted question IDs: ')
        # print(formatted_questions_id)

        for question_to_be_removed in previous_questions:
            if question_to_be_removed in formatted_questions_id:
                formatted_questions_id.remove(question_to_be_removed)

        for queston_available_to_be_asked in formatted_question:
            if int(queston_available_to_be_asked['id']) in \
                    formatted_questions_id:
                remaining_questions_per_category.append(
                    queston_available_to_be_asked)
        # print('number of remaining question per current category: ' +
        #     str(len(remaining_questions_per_category)))

        if len(remaining_questions_per_category) == 0:
            current_question = None
            force_end = True
        else:
            current_question = random.choice(remaining_questions_per_category)
        # print('Selected Question')
        # print(current_question)

        return jsonify({
            'success': True,
            'question': current_question,
            'forceEnd': force_end
        })

    ''' @TODO: Create error handlers for all expected errors
    including 404 and 422.'''

    # Client side errors
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return ({
            'success': False,
            'error': 404,
            'message': "resource not found"
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return ({
            'success': False,
            'error': 405,
            'message': "method not allowed"
        }), 405

    @app.errorhandler(422)
    def un_processable(error):
        return ({
            'success': False,
            'error': 422,
            'message': "un-processable"
        }), 422

    # Server side errors
    @app.errorhandler(500)
    def internal_server_error(error):
        return ({
            'success': False,
            'error': 500,
            'message': "Internal server error"
        }), 500

    @app.errorhandler(502)
    def bad_gateway(error):
        return ({
            'success': False,
            'error': 502,
            'message': "Bad Gateway"
        }), 502

    @app.errorhandler(504)
    def gateway_timeout(error):
        return ({
            'success': False,
            'error': 504,
            'message': "Gateway Timeout"
        }), 504

    return app
