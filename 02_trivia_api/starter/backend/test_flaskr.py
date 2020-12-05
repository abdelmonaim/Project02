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
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.proper_formatted_question = {
            'question': 'this is a question?',
            'answer': 'this is an answer.',
            'difficulty': '3',
            'category': 2
        }
        self.improper_formatted_question = {
            'question': '',
            'answer': 'this is an answer.',
            'difficulty': '3',
            'category': 2
        }
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
    def test_adding_new_properly_formatted_question(self):
        res = self.client().post('/questions', json=self.proper_formatted_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question'], self.proper_formatted_question['question'])
        self.assertEqual(data['answer'], self.proper_formatted_question['answer'])
        self.assertTrue(data['total_number_of_questions'])

    def test_adding_new_improperly_formatted_question(self):
        res = self.client().post('/questions', json=self.improper_formatted_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)

    def test_search_function(self):
        res = self.client().post('/questions', json={'searchTerm': 'w'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue('w' in data['questions'][0]['question'])

    def test_search_function_not_working(self):
        res = self.client().post('/questions', json={'searchTerm': 'sadfasd'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)

    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['categories']))

    def test_get_all_categories_not_working(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_get_questions_by_page_in_range(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))

    def test_get_questions_by_page_out_of_range(self):
        res = self.client().get('/questions?page=20')

        self.assertEqual(res.status_code, 404)

    def test_delete_question_not_in_database(self):
        res = self.client().delete('/questions/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_get_questions_by_category_not_working(self):
        res = self.client().get('/categories/10/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_playing(self):
        res = self.client().post('/quizzes',
                                 json={'previous_questions': [],
                                       'quiz_category': {'id': 1,
                                                         'type': 'Science'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_playing_with_wrong_parameters(self):
        res = self.client().post('/quizzes',
                                 json={'previous_questions': [],
                                       'quiz_category': {'id': 10,
                                                         'type': 'Science'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()