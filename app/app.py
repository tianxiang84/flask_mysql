import mysql.connector
import flask
from flask import Flask, request, render_template

app = flask.Flask(__name__)

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
    return "OK."




@app.route('/')
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
