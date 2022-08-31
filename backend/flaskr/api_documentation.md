## API Reference

### Getting Started
- At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- This application does not require authentication or API keys at the moment. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
In this app, depending on a request failure, this API will return five different error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: method not allowed
- 422: Not Processable 
- 500: Internal server error

### Endpoints 
#### GET /questions
- General:
    - Returns a list of questions, including pagination (every 10 questions), number of total questions, current category, categories. 
- URI: `curl http://127.0.0.1:5000/questions`

``` {
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
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
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        }
    ],
    "totalQuestions": 20
}
```

#### GET /categories
- General:
    - Returns a list of categories of subject as a value pair. 
- Example: `curl http://127.0.0.1:5000/categories`

```{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true,
    "total_category": 6
}
```

#### GET /categories/<int:cat>/questions
- General:
    - This endpoint returns a list of questions based on category id supplied. 
- Example: `curl http://127.0.0.1:5000/categories/3/questions`

```
{
  "currentCategory": "Sports",
  "questions": [
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
    }
  ],
  "success": true,
  "totalQuestions": 2
}
```

#### POST /questions
- General:
    - Allows a user to create a new question, which will require the question and answer text, category, and difficulty score
- Example: `curl -X POST -H "Content-Type: application/json" -d '{"question":"How many Oceans are in the world", "answer":"Five 5", "difficulty":"2", "category":"3"}' http://127.0.0.1:5000/questions`

```
{
  "question": {
    "answer": "Five 5",
    "category": 3,
    "difficulty": 2,
    "id": 39,
    "question": "How many Oceans are in the world"
  },
  "success": true,
  "total_questions": 22
}
```

#### POST /questions/search
- General:
    - Returns questions based on a search term. It returns questions for whom the search term is a substring of the question
- Example: `curl -X POST -H "Content-Type: application/json" -d '{"searchTerm":"What is an API"}' http://127.0.0.1:5000/questions/search`

```
{
  "currentCategory": "History",
  "questions": [
    {
      "answer": "Application Programming Interface",
      "category": 1,
      "difficulty": 3,
      "id": 24,
      "question": "What is an API"
    }
  ],
  "success": true,
  "totalQuestions": 1
}
```

#### POST /quizzes
- General:
    - This endpoint returns a question to play the quiz. It takes a category and previous question as parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
- Example: `curl -X POST 'http://127.0.0.1:5000/quizzes' -H 'Content-Type: application/json' -d '{"previous_questions": [1, 4, 20, 15], "quiz_category":{"id":"1", "type":"Science"}}`

```
{
  "question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  },
  "success": true
}
```

#### DELETE /questions/<int:question_id>
- General:
    - Deletes a question using a question `ID` supplied by the user. 
- URI: `curl -X DELETE http://127.0.0.1:5000/questions/2`

```
{
  "id": 2,
  "message": "Delete completed",
  "success": true
}
```

