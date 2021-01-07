# Trivia Quizzing Game

## Introduction

This project is a trivia quizzing game for Udacity code reviewers, tell me how much you scored on the first try with your chosen category in the code review!

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 

## Getting Started

### Pre-requisites and Local Development

This project is written in 2 parts, a front-end and a back-end each using a different tech stack such as:

#### Front-end:

The front-end is mainly written in React with the help of NodeJS.

Pre-requisites include:
* NodeJS
* React
* JQuery
* CorsProxy

To install all of them at once, simply `cd` into the `frontend` directory and using your terminal execute `npm install`, afterwards you'd be ready to use `npm start` to start the front-end server.

By default the front-end runs on [localhost:3000](http://localhost:3000). 

#### Back-end:

The back-end is mainly written in Flask/Python.

Pre-requisites include:
* Flask
* Flask-Cors
* Flask-RESTful
* Flask-SQLAlchemy
* SQLAlchemy
* Werkzeug
* python-dotenv
* aniso8601
* Click
* itsdangerous
* Jinja2
* MarkupSafe
* psycopg2
* pytz
* six

To install all of them at once, simply `cd` into the `backend` directory and using your terminal execute `pip install -r requirements.txt`

Before you try starting the server you need to initialize the `database credentials`!

You can do this by creating a file named `.env` in the `backend` directory and inserting two lines:
```bash
DB_USER=<postgres_db_username>
DB_PASSWORD=<postgres_db_password>
```
Replace the `<postgres_db_username>` and `<postgres_db_password>` with your actual credentials, afterwards you'd be ready to set the environment variables to start the Flask app, this depends on which OS you're on and which command-line environment you're using:

* Windows using CMD:
    * `set FLASK_APP=flaskr`
    * `set FLASK_ENV=development`
    * `flask run`

* Windows using PS:
    * `$env:FLASK_APP='flaskr'`
    * `$env:FLASK_ENV='development'`
    * `flask run`

* Unix using Bash (e.g. Linux and MacOS):
    * `export FLASK_APP=flaskr`
    * `export FLASK_ENV=development`
    * `flask run`

By default the back-end runs on `localhost:5000`, but the back-end doesn't serve an index page so if you visit that link nothing will show up.

## API Endpoints

Base URL: `localhost:5000`

* `GET /categories`:
    * Description: Retrieves all categories from the database
    * Usage: `curl -X GET http://localhost:5000/categories`
    * Example: `curl -X GET http://localhost:5000/categories`
    * Parameters: N/A
    * Response: 
    ```bash
    {
        'success': true,
        'categories': [
                        {
                            'id': int,
                            'type': str
                        },
                        ...
                      ]
    }
    ```
* `GET /questions`:
    * Description: Retrieves page-sized (10 by default) list of questions from the database
    * Usage: `curl -X GET http://localhost:5000/questions?page=var`
    * Example: `curl -X GET http://localhost:5000/questions?page=2`
    * Parameters:
        * `page`:
            * Usage: URL Argument
            * Type: int
            * Default: 1
    * Response:
    ``` bash
    {
        'success': true,
        'questions': [
                        {
                            'id': int,
                            'question': str,
                            'answer': str,
                            'category': int,
                            'difficulty': int
                        },
                        ...
                     ],
        'total_questions': int,
        'current_category': [int, int, ...],
        'categories': [
                        {
                            'id': int,
                            'type': str
                        },
                        ...
                      ]
    }
    ```
* `POST /questions`:
    * Add Question:
        * Description: Adds a question using the data in a JSON-formatted request body to the database
        * Usage: `curl -X POST -h "Content-Type:application/json" -d '{"question":str,"answer":str,"category":int,"difficulty":int}' http://localhost:5000/questions`
        * Example: `curl -X POST -h "Content-Type:application/json" -d '{"question":"How easy is this?","answer":"Very Easy","category":2,"difficulty":1}' http://localhost:5000/questions`
        * Parameters:
            * `question`:
                * Usage: JSON
                * Type: str
                * Default: N/A
            * `answer`:
                * Usage: JSON
                * Type: str
                * Default: N/A
            * `category`:
                * Usage: JSON
                * Type: int
                * Default: N/A
            * `difficulty`:
                * Usage: JSON
                * Type: int
                * Default: N/A
        * Response:
        ```bash
        {
            'success': true,
            'question': {
                            'id': int,
                            'question': str,
                            'answer': str,
                            'category': int,
                            'difficulty': int
                        }
        }
        ```
    * Search Questions:
        * Description: Searches for questions matching part or all of a JSON-formatted query in the database and returns the results (case insensitive)
        * Usage: `curl -X POST -h "Content-Type:application/json" -d '{"searchTerm":str}' http://localhost:5000/questions`
        * Example: `curl -X POST -h "Content-Type:application/json" -d '{"searchTerm":"What"}' http://localhost:5000/questions`
        * Parameters:
            * `searchTerm`:
                * Usage: JSON
                * Type: str
                * Default: N/A
        * Response:
        ```bash
        {
            'success': true,
            'questions': [
                            {
                            'id': int,
                            'question': str,
                            'answer': str,
                            'category': int,
                            'difficulty': int
                            },
                            ...
                         ],
            'total_questions': int,
            'current_category': [int, int, ...]
        }
        ```
* `DELETE /questions/<question_id>`:
    * Description: Deletes the question with the given question ID from the database
    * Usage: `curl -X DELETE http://localhost:5000/questions/int`
    * Example: `curl -X DELETE http://localhost:5000/questions/10`
    * Parameters:
        * `question_id`:
            * Usage: URL Parameter
            * Type: int
            * Default: N/A
    * Response:
    ```bash
    {
        'success': true,
        'question' int #question ID
    }
    ```
* `GET /categories/<category_id>/questions`:
    * Description: Retrieves all questions of a given category from the database
    * Usage: `curl -X GET http://localhost:5000/categories/int/questions`
    * Example: `curl -X GET http://localhost:5000/categories/2/questions`
    * Parameters:
        * `category_id`:
            * Usage: URL Parameter
            * Type: int
            * Default: N/A
    * Response:
    ```bash
    {
        'success': true,
        'questions': [
                        {
                        'id': int,
                        'question': str,
                        'answer': str,
                        'category': int,
                        'difficulty': int
                        },
                        ...
                     ],
        'total_questions': int,
        'current_category': int
    }
    ```
* `POST /quizzes`
    * Description: Returns random question in a given category from the database, excluding any previously returned questions
    * Usage: `curl -X POST -h "Content-Type:application/json" -d '{"previous_questions":[int,int,...],"quiz_category":{"id":int,"type":str}}' http://localhost:5000/quizzes`
    * Example: `curl -X POST -h "Content-Type:application/json" -d '{"previous_questions":[20,21,22],"quiz_category":{"id":1,"type":"Science"}}' http://localhost:5000/quizzes`
    * Parameters:
        * `previous_questions`:
            * Usage: JSON
            * Type: array of ints
            * Default: N/A
        * `quiz_category`:
            * Usage: JSON
            * Type: JSON in the following format:

                ```bash
                {
                    'id': int,
                    'type': str #category name
                }
                ```
            * Default: N/A
    * Response:
    ```bash
    {
        'success': true,
        'question': {
                        'id': int,
                        'question': str,
                        'answer': str,
                        'category': int,
                        'difficulty': int
                    }
    }
    ```

## Expected Responses

Aside from the response formats shown above which will return in the case of a successful request, there are a number of responses that return on erroneous responses with which you should be familiar:

* 400, Bad Request:
    * Description: You'll receive this response when the request you submit is invalid (has invalid parameters or malformed request)
    * Status Code: 400
    * Message: `Bad Request`
    * Response:
    ```bash
    {
        'success': false,
        'message': 'Bad Request'
    }
    ```
* 404, Not Found:
    * Description: You'll receive this response when the request you submit is requesting a resource that does not exist
    * Status Code: 404
    * Message: `Not Found`
    * Response:
    ```bash
    {
        'success': false,
        'message': 'Not Found'
    }
    ```
* 405, Method Not Allowed:
    * Description: You'll receive this response when the request you submit has an invalid HTTP method
    * Status Code: 405
    * Message: `Method Not Allowed`
    * Response:
    ```bash
    {
        'success': false,
        'message': 'Method Not Allowed'
    }
    ```
* 422, Unprocessable Entity:
    * Description: You'll receive this response when you try to process a resource in an invalid way 
    * Status Code: 422
    * Message: `Unprocessable Entity`
    * Response:
    ```bash
    {
        'success': false,
        'message': 'Unprocessable Entity'
    }
    ```
* 500, Internal Server Error:
    * Description: You'll receive this response when the server encounters an error (rare)
    * Status Code: 422
    * Message: `Internal Server Error`
    * Response:
    ```bash
    {
        'success': false,
        'message': 'Internal Server Error'
    }
    ```

## Testing

I have included a number of tests in the file `test_flaskr.py` inside the `backend` directory.

To run them simply navigate your terminal to the `backend` directory and execute `python test_flaskr.py` or `python3 test_flaskr.py`.

If you think there are any test cases I am missing please let me know!

## Authors

Your friendly neighborhood software developer, Nour A. Talaat.