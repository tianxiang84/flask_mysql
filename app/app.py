from flask import Flask, request, render_template # Import Flask class
import mysql.connector

app = Flask(__name__) # create an instance of the Flask class called app


@app.route('/quiz')
def quiz():
    config = {
                'user': 'devuser',
                'password': 'devpass',
                'host': 'db',
                'port': '3306',
                'database': 'tianxiang_db'
             }
    connection = mysql.connector.connect(**config)

    cursor = connection.cursor()
    sql_select_Query = "select * from vocabulary"
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()

    quiz_sentence = records[0][1]

    return render_template('quiz.html', quiz_sentence=quiz_sentence)



###########################################################
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('index.html')
##########################################################################



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
    app.run(debug=True,host='0.0.0.0')
