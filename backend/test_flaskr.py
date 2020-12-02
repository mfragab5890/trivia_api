import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'trivia_test'
        setup_db(self.app, self.database_name)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # test get all questions if exist
    def test_get_questions_per_page(self):
        """Test if all questions returned from database call and set to pages """
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    # test get questions where page nonexistent or database empty
    def test_get_questions_on_page_not_exist(self):
        """Test that calling an nonexistent page will abort 404 """
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not found!!! : please check your Data or maybe your request is currently '
                                            'not available.')

    # test get questions where category nonexistent or database empty
    def test_get_questions_on_category_not_exist(self):
        """Test that calling an nonexistent category will abort 404 """
        res = self.client().get('/questions?category=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data[ 'success' ], False)
        self.assertEqual(data[ 'error' ], 404)
        self.assertEqual(data[ 'message' ],
                         'Not found!!! : please check your Data or maybe your request is currently '
                         'not available.')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()