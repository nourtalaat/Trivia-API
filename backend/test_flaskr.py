import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from dotenv import load_dotenv

load_dotenv()


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(os.getenv('DB_USER'),os.getenv('DB_PASSWORD'),'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

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

    '''
        Tests for the GET /categories route
    '''

    # Tests the GET route (/categories)
    def test_get_categories_success(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    '''
        Tests for the GET /questions route
    '''

    # Tests the GET route (/questions)
    def test_get_questions_success(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Tests the GET route (/questions) with 'page' argument within range
    def test_get_questions_page_success(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Tests the GET route (/questions) with 'page' argument out of range
    def test_get_questions_page_not_found(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''
        Tests for the DELETE /questions/<quest_id> route
    '''

    # Tests the DELETE route (/questions/<quest_id>) with a valid question ID
    def test_delete_question_success(self):
        quest_id = '10'
        res = self.client().delete(f'/questions/{quest_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question'], quest_id)

    # Tests the DELETE route (/questions/<quest_id>) with an invalid question ID
    def test_delete_question_not_found(self):
        quest_id = '100000'
        res = self.client().delete(f'/questions/{quest_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # Tests the DELETE route (/questions/<quest_id>) with a non-numeric question ID
    def test_delete_question_bad_id_type(self):
        quest_id = 'break_the_server'
        res = self.client().delete(f'/questions/{quest_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    
    '''
        Tests for the POST /questions route
    '''

    # Tests the POST route (/questions) with valid and complete JSON data to add a question to the DB
    def test_post_add_question_success(self):
        body = {
            'question': 'a',
            'answer': 'a',
            'difficulty': 3,
            'category': 2
        }
        res = self.client().post('/questions', data=json.dumps(body), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Tests the POST route (/questions) with invalid JSON data to add a question to the DB
    def test_post_add_question_bad_request(self):
        body = {
            'question': 123,
            'answer': 123,
            'difficulty': 'a',
            'category': 1
        }
        res = self.client().post('/questions', data=json.dumps(body), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # Tests the POST route (/questions) with valid and complete JSON data to search for questions in the DB
    def test_post_search_question_success(self):
        body = {
            'searchTerm': 'what'
        }
        res = self.client().post('/questions', data=json.dumps(body), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    '''
        Tests for the GET /categories/<cat_id>/questions route
    '''

    # Tests the GET route (/categories/<cat_id>/questions) with a valid category ID (that has questions in it)
    def test_get_questions_category_success(self):
        cat_id = '2'
        res = self.client().get(f'/categories/{cat_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Tests the GET route (/categories/<cat_id>/questions) with a valid category ID (that has NO questions in it)
    def test_get_questions_category_empty_category(self):
        cat_id = '20'
        res = self.client().get(f'/categories/{cat_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    # Tests the GET route (/categories/<cat_id>/questions) with an invalid category ID
    def test_get_questions_category_not_found(self):
        cat_id = '2000'
        res = self.client().get(f'/categories/{cat_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # Tests the GET route (/categories/<cat_id>/questions) with an invalid category ID
    def test_get_questions_category_bad_request(self):
        cat_id = 'break_the_server'
        res = self.client().get(f'/categories/{cat_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    '''
        Tests for the POST /quizzes route
    '''

    # Tests the POST route (/quizzes) with valid and complete JSON data, with no previous questions asked
    def test_post_play_quiz_success_no_prev(self):
        body = {
            'previous_questions': [],
            'quiz_category': {
                'id': 1,
                'type': 'Science'
            }
        }
        res = self.client().post('/quizzes', data=json.dumps(body), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        
    # Tests the POST route (/quizzes) with valid and complete JSON data, with previous questions asked
    def test_post_play_quiz_success_prev(self):
        body = {
            'previous_questions': [20],
            'quiz_category': {
                'id': 1,
                'type': 'Science'
            }
        }
        res = self.client().post('/quizzes', data=json.dumps(body), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    # Tests the POST route (/quizzes) with valid and complete JSON data but no remaining questions
    def test_post_play_quiz_success_no_remaining(self):
        body = {
            'previous_questions': [20, 21, 22],
            'quiz_category': {
                'id': 1,
                'type': 'Science'
            }
        }
        res = self.client().post('/quizzes', data=json.dumps(body), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(data['question'])
    
    # Tests the POST route (/quizzes) with invalid JSON data
    def test_post_play_quiz_bad_request(self):
        body = {
            'previous_questions': [],
            'quiz_category': {
                'id': 'break_the_server',
                'type': 'invalid category'
            }
        }

        res = self.client().post('/quizzes', data=json.dumps(body), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()