# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```
## Error Handling

Errors are returned as JSON objects in the below format:
```
{
  'success': False,
  'error': 400,
  'message': "bad request"
}
```
The API will return four error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Proccessable

## End Points

GET '/categoires'
- General:
	- Input:
		+ Method type : 'GET'
		+ Arguments : None
	- Returns:
		+ Dictionary with available categories.
		+ Intergar for total number of available categories.
		+ Success MSG.
- Sample request:
	- curl -X GET http://127.0.0.1:5000/categories.
- Result:
```
{
  "all_categories": 6, 
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

GET  '/questions'
- General:
	- Input:
		+ Method type : 'GET'
		+ Arguments : None
	- Returns:
		+ List of pagenated dictionaries of questions object, each containing the question, the answer, diffcuilty and category
		+ List of dictioneries of categories.
		+ Intergar for total number of available questions.
		+ Success MSG.
- Sample:
	- curl -X GET http://127.0.0.1:5000/questions
- Result:
```
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "current_category": "All", 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    .............., 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 22
}

```

DELETE '/questions/<int:question_id>'  
- General:
	- Input:
		+ Method type : 'DELETE'
		+ Arguments : <int:question ID>
	- Returns:
		+ Used to delete a question frm database by its ID
		+ Integer ID for deleted question.
		+ Success MSG.
- Sample:
	- curl -X DELETE http://127.0.0.1:5000/questions/1
- Result:
```{
  "answer": "this is answer 0.", 
  "question": "this is question 0?", 
  "success": true, 
  "total_number_of_questions": 24
}

{
  "deleted": 10, 
  "success": true
}

```

POST '/questions'  
- General:
	- Input:
		+ Method type : POST
		+ Arguments : dictionary with question, answer, category, difficulty
	- Returns:
		+ Added question, added answer.
		+ Total number of question after addition.
		+ Success MSG
- Sample:
	- curl -X POST -H "Content-Type: application/json" -d '{"question":"this is question 0?","answer":"this is answer 0.","difficulty":1,"category":1}' http://127.0.0.1:5000/books
- Result:
```
{
  "answer": "this is answer 0.", 
  "question": "this is question 0?", 
  "success": true, 
  "total_number_of_questions": 24
}
```

GET  '/categories/<int:category_id>/questions'
- General:
	- Input:
		+ Method type : GET
		+ Arguments : Category ID
	- Returns:
		+ List of dictionaries of questions.
		+ Success MSG
- Sample:
	- curl -X GET http://127.0.0.1:5000/categories/1/questions
- Result:
```
{
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    ............................
    {
      "answer": "this is answer 0.", 
      "category": 1, 
      "difficulty": 1, 
      "id": 29, 
      "question": "this is question 0?"
    }
  ], 
  "success": true
}

```

POST '/quizzes'  
- General:
	- Input:
		+ Method type : POST
		+ Arguments : 
			- List of previous questions in current hand.
			- Specific category for current hand.
	- Returns:
		+ Question to be played, (not present in previous questions list)
		+ Success MSG.
- Sample:
	- curl -X POST -H "Content-Type: application/json" -d '{"previous_questions":[],"quiz_category":{"type":"Science","id":"1"}}' http://127.0.0.1:5000/quizzes
- Result:
```
{
  "question": {
    "answer": "The Liver", 
    "category": 1, 
    "difficulty": 4, 
    "id": 20, 
    "question": "What is the heaviest organ in the human body?"
  }, 
  "success": true
}
```
## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```