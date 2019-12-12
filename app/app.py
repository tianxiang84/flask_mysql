import mysql.connector

config = {
        'user': 'devuser',
        'password': 'devpass',
        'host': 'db',
        'port': '3306'
    }
connection = mysql.connector.connect(**config)
