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
    current_books = formatted_questions[ start:end ]
    return current_books


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
                    'current_category': 'all',
                    'categories': category_names
                })
            else:
                abort(404)
        # if an category id is sent display questions with that id
        elif isinstance(category, int):
            questions = Question.query.filter(Question.category == category).first()
            if questions is not None:
                page_questions = my_page(request, questions)
                current_category = Category.query.get(category).type
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

        # get all books with pagination

    @app.route('/categories', methods=['GET'])
    def get_all_categories():
        categories = Category.query.order_by('id').all()
        category = []

        for cat in categories:
            category.append({'name': cat.type,
                            'id': cat.id})
        if len(category):
            return jsonify({
                'success': True,
                'categories': category,
                'all_categories': len(category)
            })
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
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": 'Unprocessable!!! : The request was well-formed but was unable to be followed due to semantic '
                       'errors. '
        }), 422

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": 'Method Not Allowed: A request was made of a resource using a request method not supported by '
                       'that resource '
        }), 405

    @app.errorhandler(400)
    def not_found(error):
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
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

    '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

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

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    return app
