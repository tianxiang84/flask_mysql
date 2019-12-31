# flask_mysql

This is a simple web service with mySQL database to test vocabulary. The quiz is generated from the database considering: (1) How recent the sentence was entered into the database; (2) How many times the sentence was tested, and (3) How many times it was answered correctly.

I. Enter quiz with phpmyadmin:
(1) docker-compose up --build
(2) localhost:8000
(3) Enter your quiz in the database table

II. Do the quiz with the flask app
(1) docker-compose up --build
(2) localhost:5000/quiz
(3) Do the quiz
