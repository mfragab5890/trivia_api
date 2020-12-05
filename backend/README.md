# Full Stack Trivia API Backend

## Project Description
This is a web application where clients can display various questions by a certain category or all available categories, Add/Delete questions, search questions by desired string and take a quiz for certain category or all categories as desired.


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

- [Flask-SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 
- [Flask-SQLAlchemy](https://pypi.org/project/Flask-SQLAlchemy/) is an extension for Flask that adds support for SQLAlchemy to your application. It aims to simplify using SQLAlchemy with Flask by providing useful defaults and extra helpers that make it easier to accomplish common tasks.

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
export FLASK_CONFIG=instance
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

Setting the `FLASK_CONFIG` variable to `instance` directs flask to use the `instance` directory and the `config.py` file to find the application configration.

## Done Tasks

1. Used Flask-CORS to enable cross-domain requests and set response headers. 
2. Created an endpoint to handle GET requests for questions, including pagination (every 10 questions),you can select a category as argument with page. This endpoint returns a list of questions, number of total questions, current category(if not selected will return all), categories. 
3. Created an endpoint to handle GET requests for all available categories. 
4. Created an endpoint to DELETE question using a question ID. 
5. Created an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It returns any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint takes category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422, 405 and 500. 

## API References

### Getting Started

##### Base URL: 
Currently hosted locally at http://127.0.0.1:5000/.

##### Authentication: 
Currently no authentication or API keys required.

### Error Handling:

Errors are returned as JSON objects in the following format:
```bash
{
    "success": False,
    "error": 400,
    "message": "Bad Request!!!! Please make sure the data you entered is correct"
}
```
The API will return three error types when requests fail:
```bash
400: Bad Request
404: Resource Not Found
422: Not Processable
405: Method Not Allowed
```
### Endpoints

#### GET '/questions'

##### function:
######Fetches all available questions with pagination currently 10 per page (default page =1) and a certain if requested (default All).

##### Request Arguments:
######page(number:int), category(id:int) both are optional.

##### Response body:
######Returns an object with categories (names), success (state:bool), total_questions (total number of questions),current_category (if sent as query argument) and questions (question, answer, difficulty, category & id). 
######sample: 
curl -x GET http://127.0.0.1:5000/questions?category=4&page=1
######results:
```bash
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports", 
    "technology", 
    "Not Assigned"
  ], 
  "current_category": "History", 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ], 
  "success": true, 
  "total_questions": 4
}
```

#### GET '/categories'

##### function:
######Fetches all available categories.

##### Request Arguments:
######None.

##### Response body:
######Returns an object with categories (id:int & type:string), success (state:bool) and total_categories (total number of categories). 
######sample: 
curl -x GET http://127.0.0.1:5000/categories
######results:

```bash
{
    "categories": [
        {
          "id": 1, 
          "type": "Science"
        }, 
        {
          "id": 2, 
          "type": "Art"
        }, 
        {
          "id": 3, 
          "type": "Geography"
        }, 
        {
          "id": 4, 
          "type": "History"
        }, 
        {
          "id": 5, 
          "type": "Entertainment"
        }, 
        {
          "id": 6, 
          "type": "Sports"
        }
      ], 
  "success": true, 
  "total_categories": 8
}

```

#### DELETE '/questions/<int:question_id>'

##### function:
######Delete a certain question with a sent id.

##### Request Parameters:
######id(question_id:int).

##### Response body:
######Returns an object with current_questions (question, answer, difficulty, category & id), success (state:bool), deleted_question(id of deleted question) and total_questions (total number of questions after delete). 
######sample: 
curl -X DELETE http://127.0.0.1:5000/questions/2 -H "Content-Type: application/json"
######results:

```bash
{
  "current_questions": [
    {
      "answer": "what about it!",
      "category": 7,
      "difficulty": 0,
      "id": 3,
      "question": "what about technology"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "what about it!",
      "category": 7,
      "difficulty": 0,
      "id": 7,
      "question": "what about technology"
    },
    {
      "answer": "what about it!",
      "category": 7,
      "difficulty": 0,
      "id": 8,
      "question": "what about technology"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    }
  ],
  "deleted_question": 2,
  "success": true,
  "total_questions": 23
}

```

#### POST '/questions'

##### function:
######Add a new question.

##### Request Parameters:
######question (string), answer (string), difficulty (int), category (category_id:int).

##### Response body:
######Returns an object with created (question_id:int), success (state:bool), total_questions (total number of questions) and questions (question, answer, difficulty, category & id). 
######sample: 
curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d "{\"
question\": \"the question\", \"answer\": \"the answer\", \"difficulty\": 5, \"category\": 7}"
######results:
```bash
{
  "created": 26,
  "questions": [
    {
      "answer": "what about it!",
      "category": 7,
      "difficulty": 0,
      "id": 3,
      "question": "what about technology"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "what about it!",
      "category": 7,
      "difficulty": 0,
      "id": 7,
      "question": "what about technology"
    },
    {
      "answer": "what about it!",
      "category": 7,
      "difficulty": 0,
      "id": 8,
      "question": "what about technology"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    }
  ],
  "success": true,
  "total_questions": 24
}

```

#### POST '/questions/search'

##### function:
######Search any questions for whom the search term is a substring of the question.

##### Request Parameters:
######searchTerm(string).

##### Response body:
######Returns an object with search_term (searchTerm:string), success (state:bool), total_questions (total number of questions) and questions (question, answer, difficulty, category & id). 
######sample: 
curl -X POST http://127.0.0.1:5000/questions/search -H "Content-Type: application/json"
-d "{\"searchTerm\": \"a\"}"
######results:
```bash
{
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist?initials M C was a creator of optical illusions?"
    }
  ],
  "search_term": "a",
  "success": true,
  "total_questions": 21
}

```

#### POST '/category/questions'

##### function:
######Fetches all available questions of a certain category with pagination currently 10 per page (default page =1).

##### Request Parameters:
######category(id:int).

##### Response body:
######Returns an object with categories (names), success (state:bool), total_questions (total number of questions),current_category (type) and questions (question, answer, difficulty, category & id). 
######sample: 
curl -x GET http://127.0.0.1:5000/questions?category=4&page=1
######results:
```bash
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports", 
    "technology", 
    "Not Assigned"
  ], 
  "current_category": "History", 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ], 
  "success": true, 
  "total_questions": 4
}
```


#### POST '/category/quiz/questions'

##### function:
######send a question to client based on a certain categories or All categories on condition that a question is not repeated based on previous questions.

##### Request Parameters:
######category(id:int),previuosQuestions(array).

##### Response body:
######Returns an object with success (state:bool), total_category_questions (total number of questions on selected category),current_category (type) and question (question, answer, difficulty, category & id). 
######sample: 
curl -X POST http://127.0.0.1:5000/category/quiz/questions -H "Content-Type: application
/json" -d "{\"category\":1, \"previous_questions\":\"[20,21]\"}"
######results:
```bash
{
  "current_category": "Science",
  "question": {
    "answer": "Blood",
    "category": 1,
    "difficulty": 4,
    "id": 22,
    "question": "Hematology is a branch of medicine involving the study of what?"
  },
  "success": true,
  "total_category_questions": 3
}

```

## Testing
To run the tests, run
```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia_test.psql
python test_flaskr.py
```