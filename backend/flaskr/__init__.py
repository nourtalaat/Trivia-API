# I'm suppressing this warning because all functions (route handlers in this case) inside the function create_app() are marked as "unused variable" which I find really annoying
# pylint: disable=unused-variable

import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from werkzeug.exceptions import NotFound

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # Create and configure the app
  app = Flask(__name__)
  setup_db(app)
  '''
  OK @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  # Setup CORS to accept requests from any origin (*)
  cors = CORS(app, origins=['*'])
  '''
  OK @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  # Enumerates accepted headers and methods
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Allow-Control-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Allow-Control-Methods', 'GET,POST,DELETE,OPTIONS')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  # GET route that queries, formats and returns all categories
  @app.route('/categories', methods=['GET'])
  def get_categories():
    try:
      rawCats = Category.query.all()
      cats = {}
      for rawCat in rawCats:
        cat = rawCat.format()
        cats[cat['id']] = cat['type']

      return jsonify({
        'success': True,
        'categories': cats
      })
    # In case of a malformed request return 400 (bad request)
    except Exception:
      abort(400)


  '''
  OK @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  OK TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  # GET route to retrieve paginated questions and categories as well as total number of questions
  @app.route('/questions', methods=['GET'])
  def get_questions():
    try:
      # get current page, defaults to 1 if not present
      page = request.args.get('page', default=1, type=int)

      # Query one page of questions then format them and extract total number of questions
      quests_query = Question.query.order_by(Question.category.asc()).paginate(page, QUESTIONS_PER_PAGE)
      total_quests = quests_query.total
      rawQuests = quests_query.items
      quests = [rawQuest.format() for rawQuest in rawQuests]

      # Query and format all categories
      rawCats = Category.query.all()
      cats = {}
      for rawCat in rawCats:
        cat = rawCat.format()
        cats[cat['id']] = cat['type']

      current_cats = []
      for quest in quests:
        cat = quest['category']
        if cat not in current_cats:
          current_cats.append(cat)
      return jsonify({
        'success': True,
        'questions': quests,
        'total_questions': total_quests,
        'current_category': current_cats,
        'categories': cats
      })
    # In case of page being out of range
    except NotFound:
      abort(404)
    # In case of a malformed request return 400 (bad request)
    except Exception:
      abort(400)

  '''
  OK @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  OK TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  # DELETE route that accepts a question ID in the URL, retrieves and deletes said question
  @app.route('/questions/<quest_id>', methods=['DELETE'])
  def delete_question(quest_id):
    try:
      # Queries question by ID then uses delete function
      Question.query.get(quest_id).delete()
      return jsonify({
        'success': True,
        'question': quest_id
      })
    # If question does not exist we rollback (while there's no real need for a rollback here, it is a standard practice)
    except (NameError, AttributeError):
      Question.rollback(Question)
      abort(404)
    # If question ID is not of type string return 400 (bad request) and rollback
    except Exception:
      Question.rollback(Question)
      abort(400)

  # POST route handles post requests to /questions (which contains 2 functions, as shown below)
  @app.route('/questions', methods=['POST'])
  # Since 2 functions use the same route we need a routing function here
  def questions_router():
    # If the request's JSON body contains the key "searchTerm" route to the search function
    try:
      request.get_json()['searchTerm']
      return search_questions()
    # Otherwise route to the add question function
    except KeyError:
      return add_question()
  '''
  OK @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  OK TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  # POST function that adds questions to the DB using the JSON data submitted in the request
  def add_question():
    try:
      # Extract JSON data from request, create question object then insert it into the DB
      data = request.get_json()
      question = Question(question=data['question'], answer=data['answer'], category=data['category'], difficulty=data['difficulty'])
      question.insert()
      return jsonify({
        'success': True,
        'question': question.format()
      })
    # On malformed requests, rollsback and returns 400 (bad request) response
    except Exception:
      Question.rollback(Question)
      abort(400)
  '''
  OK @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  OK TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  # POST function that searches questions using a JSON searchTerm sent with the request
  def search_questions():
    try:
      searchTerm = request.get_json()['searchTerm']
      # Queries questions that contain the search term (case insensitive via ilike())
      rawResultQuests = Question.query.filter(Question.question.ilike(f"%{searchTerm}%"))
      # Formats the questions
      resultQuests = [rRQuest.format() for rRQuest in rawResultQuests]
      # Gets total_questions count
      total_quests = Question.query.count()

      current_cats = []
      for quest in resultQuests:
        cat = quest['category']
        if cat not in current_cats:
          current_cats.append(cat)

      return jsonify({
        'success': True,
        'questions': resultQuests,
        'total_questions': total_quests,
        'current_category': current_cats
      })
    # In case of a malformed request we abort with status 400 (bad request)
    except Exception:
      abort(400)
  '''
  OK @TODO: 
  Create a GET endpoint to get questions based on category. 

  OK TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  # GET route that takes category id (cat_id) and returns all questions that fall into that category
  @app.route('/categories/<cat_id>/questions', methods=['GET'])
  def get_questions_by_category(cat_id):
    try:
      if not Category.query.get(cat_id):
        raise KeyError
      # Retrieve questions that have a category id of cat_id and formats them
      rawCatQuests = Question.query.filter(Question.category==cat_id)
      catQuests = [rCQuest.format() for rCQuest in rawCatQuests]
      # gets total_questions count
      total_quests = Question.query.count()
      return jsonify({
        'success': True,
        'questions': catQuests,
        'total_questions': total_quests,
        'current_category': cat_id
      })
    # If category does not exist returns 404 (not found)
    except KeyError:
      abort(404)
    # In case of a malformed request returns 400 (bad request)
    except Exception:
      abort(400)

  '''
  OK @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  OK TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  # POST route that takes previous questions (if any) and quiz category (or 0 for all categories) and returns a random question of that category that was not asked before
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    try:
      # Gets previous questions' IDs and the quiz category
      data = request.get_json()
      prevQuests_id = data['previous_questions']
      quizCat = data['quiz_category']
      # When selecting "ALL" the value 0 is sent, here we handle this condition
      if quizCat['id'] == 0:
        rawCatQuests = Question.query.all()
      else:
        rawCatQuests = Question.query.filter(Question.category==quizCat['id'])
      # Formats questions of that category and extracts the questions that were not asked before
      catQuests = [rCQuest.format() for rCQuest in rawCatQuests]
      quizQuest = [catQuest for catQuest in catQuests if catQuest['id'] not in prevQuests_id]
      # Here randQuizQuest is defaulted to None in the case of there being no more questions in that category to ask
      randQuizQuest = None
      # If there are questions that were not asked yet, select a random question of that list
      if quizQuest:
        randQuizQuest = random.choice(quizQuest)
      return jsonify({
        'success': True,
        'question': randQuizQuest
      })
    # In case of a malformed request returns 400 (bad request)
    except Exception:
      abort(400)
  '''
  OK @TODO: 
  Create error handlers for all expected errors 
  including 400, 404, 405, 422, and 500. 
  '''
  # Error handler for status 400 (bad request)
  @app.errorhandler(400)
  def bad_request(e):
    return jsonify({
      'success': False,
      'message': 'Bad Request'
    }), 400

  # Error handler for status 404 (not found)
  @app.errorhandler(404)
  def not_found(e):
    return jsonify({
      'success': False,
      'message': 'Not Found'
    }), 404

  # Error handler for status 405 (method not allowed)
  @app.errorhandler(405)
  def method_not_allowed(e):
    return jsonify({
      'success': False,
      'message': 'Method Not Allowed'
    }), 405

  # Error handler for status 422 (unprocessable entity)
  @app.errorhandler(422)
  def unprocessable_entity(e):
    return jsonify({
      'success': False,
      'message': 'Unprocessable Entity'
    }), 422
  
  # Error handler for status 500 (internal server error)
  @app.errorhandler(500)
  def internal_error(e):
    return jsonify({
      'success': False,
      'message': 'Internal Server Error'
    }), 500

  return app

    