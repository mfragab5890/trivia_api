import os
from flask_cors import CORS
import random
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from models import setup_db, Question, Category, database_name

# variable for pagination
QUESTIONS_PER_PAGE = 10


# pagination function
def my_page(req, questions):
    page = req.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_questions = [ question.format() for question in questions ]
    current_questions = formatted_questions[ start:end ]
    return current_questions


# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app, database_name)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # connection in configuration file added

    # ----------------------------------------------------------------------------#
    # Filters.
    # ----------------------------------------------------------------------------#

    def format_datetime(value, format='medium'):
        if isinstance(value, str):
            date = dateutil.parser.parse(value)
        else:
            date = value

        if format == 'full':
            format = "EEEE MMMM, d, y 'at' h:mma"
        elif format == 'medium':
            format = "EE MM, dd, y h:mma"
        return babel.dates.format_datetime(date, format, locale='en')

    app.jinja_env.filters[ 'datetime' ] = format_datetime

    # ----------------------------------------------------------------------------#
    # Controllers.
    # ----------------------------------------------------------------------------#

    # Get all questions with/without categories and paginated
    @app.route('/questions', methods=[ 'GET' ])
    def get_questions_per_page():
        # check if category is sent as argument and store id
        category = request.args.get('category', 0, type=int)
        # if no category sent display all in page
        if category == 0:
            questions = Question.query.order_by('category').all()
            page_questions = my_page(request, questions)
            categories = Category.query.all()
            category_names = [ ]
            for cat in categories:
                category_names.append(cat.type)

            if len(page_questions):
                return jsonify({
                    'success': True,
                    'questions': page_questions,
                    'total_questions': len(questions),
                    'current_category': 'All',
                    'categories': category_names
                })
            else:
                abort(404)
        # if an category id is sent display questions with that id
        elif isinstance(category, int):
            questions = Question.query.filter(Question.category == category).all()
            if questions is not None:
                page_questions = my_page(request, questions)
                current_category_data = Category.query.get(category)
                if current_category_data is not None:
                    current_category = current_category_data.type
                    categories = Category.query.all()
                    category_names = [ ]
                    for cat in categories:
                        category_names.append(cat.type)

                    if len(page_questions):
                        return jsonify({
                            'success': True,
                            'questions': page_questions,
                            'total_questions': len(questions),
                            'current_category': current_category,
                            'categories': category_names
                        })
                    else:
                        abort(404)
                else:
                    abort(404)
            else:
                abort(404)
        else:
            abort(404)

    # get all available categories
    @app.route('/categories', methods=['GET'])
    def get_all_categories():
        categories = Category.query.order_by('id').all()
        category = [ cat.format() for cat in categories ]

        if len(category):
            return jsonify({
                'success': True,
                'categories': category,
                'total_categories': len(category)
            })
        else:
            abort(404)

    # Delete a certain Question with id
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_user_question(question_id):
        try:
            question = Question.query.filter_by(id=question_id).one_or_none()
            if question is not None:
                question.delete()
                questions = Question.query.order_by('id').all()
                current_questions = my_page(request, questions)
                return jsonify({
                    'success': True,
                    'deleted_question': question_id,
                    'current_questions': current_questions,
                    'total_questions': len(questions)
                })
            else:
                abort(404)

        except:
            abort(422)

    # create a new question and post to database
    @app.route('/questions', methods=[ 'POST' ])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)

        try:
            if new_question is None or new_answer is None or new_difficulty is None or new_category is None:

                abort(422)

            else:
                question = Question(question=new_question,
                                    answer=new_answer,
                                    difficulty=new_difficulty,
                                    category=new_category
                                    )
                question.insert()

                questions = Question.query.order_by('id').all()
                current_questions = my_page(request, questions)
                return jsonify({
                    'success': True,
                    'created': question.id,
                    'questions': current_questions,
                    'total_questions': len(questions)
                })


        except:
            abort(422)

    # search all question from database with user's search_term and return results.
    @app.route('/questions/search', methods=[ 'POST' ])
    def search_question():
        body = request.get_json()
        search_term = body.get('search_term', None)

        search_term_formatted = '%' + search_term + '%'
        try:
            questions = Question.query.filter(Question.question.ilike(search_term_formatted)).all()
            questions_paged = my_page(request, questions)
            total_results = len(questions)
            if total_results:
                return jsonify({
                    'success': True,
                    'search_term': search_term,
                    'questions': questions_paged,
                    'total_questions': total_results
                })
            else:
                abort(404)
        except:
            abort(422)

    # Get all questions within a certain category and paginated
    @app.route('/category/questions', methods=[ 'POST' ])
    def get_category_questions_per_page():
        # check if category is sent in request
        body = request.get_json()
        category = body.get('category', None)
        if category is not None:
            questions = Question.query.filter(Question.category == category).all()
            if questions is not None:
                page_questions = my_page(request, questions)
                current_category_data = Category.query.get(category)
                if current_category_data is not None:
                    current_category = current_category_data.type
                    categories = Category.query.all()
                    category_names = [ ]
                    for cat in categories:
                        category_names.append(cat.type)

                    if len(page_questions):
                        return jsonify({
                            'success': True,
                            'questions': page_questions,
                            'total_category_questions': len(questions),
                            'current_category': current_category,
                            'categories': category_names
                        })
                    else:
                        abort(404)
                else:
                    abort(404)
            else:
                abort(404)
        else:
            abort(404)

    # quiz game takes category and previous questions if exist and send next question
    @app.route('/category/quiz/questions', methods=[ 'POST' ])
    def get_quiz_questions_per_category():
        # check if category & previous questions is sent in request
        body = request.get_json()
        category = body.get('category', None)
        previous_questions = body.get('previous_questions', [])

        if category is not None:
            current_category_data = Category.query.get(category)
            if current_category_data is not None:
                current_category = current_category_data.type
            else:
                abort(404)
            all_questions = Question.query.filter(Question.category == category).all()
            formatted_questions = [question.format() for question in all_questions]
            if formatted_questions is not None:
                all_questions_id = []
                for ques in formatted_questions:
                    all_questions_id.append(ques['id'])
                quiz_question_id = 0
                while quiz_question_id == 0:
                    random_question = random.choice(all_questions_id)
                    if str(random_question) not in previous_questions:
                        quiz_question_id = random_question
                    else:
                        continue
                quiz_question = Question.query.filter_by(id=quiz_question_id).one_or_none()
                quiz_question_formatted = quiz_question.format()
                if quiz_question:
                    return jsonify({
                        'success': True,
                        'question': quiz_question_formatted,
                        'total_category_questions': len(formatted_questions),
                        'current_category': current_category,
                    })

                else:
                    abort(404)

            else:
                abort(404)
        else:
            abort(404)


    # ----------------------------------------------------------------------------#
    # Error Handlers.
    # ----------------------------------------------------------------------------#
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": 'Not found!!! : please check your Data or maybe your request is currently not available.'
        }), 404

    @app.errorhandler(422)
    def not_processable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": 'Unprocessable!!! : The request was well-formed but was unable to be followed'
        }), 422

    @app.errorhandler(405)
    def not_allowed_method(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": 'Method Not Allowed!!!: Your request method not supported by that API '
        }), 405

    @app.errorhandler(400)
    def not_good_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'Bad Request!!!! Please make sure the data you entered is correct'
        }), 400

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": 'Internal Server Error!!!: Please try again later or reload request. '
        }), 500


    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''


    return app
