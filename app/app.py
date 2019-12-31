# Import Flask class
from flask import Flask
# The request object holds all incoming data from the request (referrer, IP, data, etc)
from flask import request

from flask import render_template
import mysql.connector

app = Flask(__name__) # create an instance of the Flask class called app


#https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
@app.route('/query-example')
def query_example():
    query_key = request.args.get('query') #if key doesn't exist, returns None
    return '''<h1>The query is: {}</h1>'''.format(query_key)

#https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
@app.route('/form-example', methods=['GET', 'POST']) #allow both GET and POST requests
def form_example():
    # When the form is submitted, do the following:
    if request.method == 'POST': #this block is only entered when the form is submitted
        firstName = request.form.get('firstName')
        lastName = request.form['lastName']
        return '''<h1>Inputs: {}, {}</h1>'''.format(firstName, lastName)

    # For 'GET' (no submit), display the form:
    return '''<form method="POST">
                  First Name: <input type="text" name="firstName"><br>
                  Last Name: <input type="text" name="lastName"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''

#https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
@app.route('/json-example', methods=['POST']) #GET requests will be blocked
def json_example():
    req_data = request.get_json()

    language = req_data['language']
    framework = req_data['framework']
    python_version = req_data['version_info']['python'] #two keys are needed because of the nested object
    example = req_data['examples'][0] #an index is needed because of the array
    boolean_test = req_data['boolean_test']

    return '''
           The language value is: {}
           The framework value is: {}
           The Python version is: {}
           The item at index 0 in the example list is: {}
           The boolean value is: {}'''.format(language, framework, python_version, example, boolean_test)



@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    config = {'user': 'devuser',
              'password': 'devpass',
              'host': 'db',
              'port': '3306',
              'database': 'tianxiang_db'
             }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # When the form is submitted, do the following:
    if request.method == 'POST': #this block is only entered when the form is submitted
        answer = request.form.get('answer')

        # First find the number of sentences in the table
        sql_select_Query = "SELECT COUNT(*) FROM vocabulary"
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        numSentences = int(records[0][0])

        # Get the sentence that is: (1) recent; (2) not tested much and (3) wrong many times
        sql_select_Query = "SELECT * FROM vocabulary"
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()

        sentenceID = int(records[0][0])
        scoreRecent = numSentences-int(records[0][0])
        scoreTestTimes = int(records[0][3])
        scoreCorrectTimes = int(records[0][3]) - int(records[0][4])
        score = scoreRecent + scoreTestTimes + scoreCorrectTimes
        for loopID in range(1,len(records)):
            scoreRecent = numSentences-int(records[loopID][0])
            scoreTestTimes = int(records[loopID][3])
            scoreCorrectTimes = int(records[loopID][3]) - int(records[loopID][4])
            if (scoreRecent + scoreTestTimes + scoreCorrectTimes) <= score:
                score = scoreRecent + scoreTestTimes + scoreCorrectTimes
                sentenceID = int(records[loopID][0])

        sql_select_Query = "SELECT * FROM vocabulary WHERE ID = {}".format(sentenceID)
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        quiz_answer = records[0][2]

        updateTestTimes = "UPDATE vocabulary SET test_times = {} WHERE ID = {}".format(int(records[0][3])+1, sentenceID)
        cursor.execute(updateTestTimes)
        connection.commit()
        if answer != quiz_answer:
            updateWrongTimes = "UPDATE vocabulary SET wrong_times = {} WHERE ID = {}".format(int(records[0][4])+1, sentenceID)
            cursor.execute(updateWrongTimes)
            connection.commit()
            cursor.close()
            connection.close()
            return '''<h1>Incorrect.<br>Get: {}<br>Correct Answer: {}<br>Tested Times: {}<br>Correct Times: {}<br><a href="http://localhost:5000/quiz">continue</a></h1>'''.format(answer, quiz_answer, int(records[0][3])+1, int(records[0][3])-int(records[0][4]))
        else:
            cursor.close()
            connection.close()
            return '''<h1>Correct.<br>Get: {}<br>Correct Answer: {}<br>Tested Times: {}<br>Correct Times: {}<br><a href="http://localhost:5000/quiz">continue</a></h1>'''.format(answer, quiz_answer, int(records[0][3])+1, int(records[0][3])-int(records[0][4])+1)





    # For 'GET' method (before submit/POST), display the form:
    # First find the number of sentences in the table
    sql_select_Query = "SELECT COUNT(*) FROM vocabulary"
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    numSentences = int(records[0][0])

    # Get the sentence that is: (1) recent; (2) not tested much and (3) wrong many times
    sql_select_Query = "SELECT * FROM vocabulary"
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()

    sentenceID = int(records[0][0])
    scoreRecent = numSentences-int(records[0][0])
    scoreTestTimes = int(records[0][3])
    scoreCorrectTimes = int(records[0][3]) - int(records[0][4])
    score = scoreRecent + scoreTestTimes + scoreCorrectTimes
    for loopID in range(1,len(records)):
        scoreRecent = numSentences-int(records[loopID][0])
        scoreTestTimes = int(records[loopID][3])
        scoreCorrectTimes = int(records[loopID][3]) - int(records[loopID][4])
        if (scoreRecent + scoreTestTimes + scoreCorrectTimes) <= score:
            score = scoreRecent + scoreTestTimes + scoreCorrectTimes
            sentenceID = int(records[loopID][0])

    sql_select_Query = "SELECT * FROM vocabulary WHERE ID = {}".format(sentenceID)
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    quiz_sentence = records[0][1]

    cursor.close()
    connection.close()

    return render_template('quiz.html', quiz_sentence=quiz_sentence)


@app.route('/') # use the route() decorator to tell Flask what URL should trigger our function.
def hello_world():
    config = {
            'user': 'devuser',
            'password': 'devpass',
            'host': 'db',
            'port': '3306',
            'database': 'tianxiang_db'
        }
    connection = mysql.connector.connect(**config)

    sql_select_Query = "select * from vocabulary"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    #print("Total number of rows in Laptop is: ", cursor.rowcount)

    return "Records:{}\nType:{}".format(records,records[0][1]) #format(cursor.rowcount) #'Flask Dockerized'

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
