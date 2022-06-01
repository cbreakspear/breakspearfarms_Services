#!flask/bin/python
from cProfile import run
import pyodbc
import sys
import json
import random
from flask import Flask, jsonify, request, abort, render_template
from flask_cors import CORS
from datetime import datetime



servicesVersion = {

            'version': "1.3",
            'author': "Craig Breakspear",
            'lastupdate': "02-14-2022"
        }

app = Flask(__name__)
CORS(app)
''' JUST A ROUTE TO TEST FOR SUCCESSFUL DEPLOY'''
@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

''' SENDS AN EMAIL TO DATATBASE FOR SUBSCRIPTION ENTRY'''
@app.route('/requestforSubscription', methods=['POST'])
def create_subscription():
    task =""

    if not request.json or not 'email' in request.json:
            abort(400)
    else:
        now = datetime.now() # current date and time
        sql = "INSERT INTO dbo.subscription (emailaddress, entry_date, insert_type) VALUES ('" + request.json['email'] + \
            "','" + str(now) + "','" + request.json['inserttype'] + "')"
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};Server=tcp:breakspearfarms.database.windows.net;Database=breakspearfarmsDB;Port=1433;uid=cbreakspear;pwd=Destination2060')
        cursor = cnxn.cursor()
        cursor.execute(sql)
        cnxn.commit()
        cnxn.close()
        print("Subscription Successfully Inserted") 
        task = {

            'customername': request.json['customername'],
            'email': request.json['email'],
            'inserttype': request.json['inserttype']
        }
        return jsonify({'STATUS': "SUCCESSFUL INSERTION OF: " + task["email"] + " for " + task["inserttype"]}), 201

''' RETURNS THE VERSION OF THE SERVICES IT IS CURRENTLY WORKING UNDER'''
@app.route('/bfsVersion', methods=['GET'])
def get_servicesversion():
    
    return jsonify(servicesVersion), 200

''' RETURNS THE A QUOTE OF THE DAY. RANDOM REALLY :)'''
@app.route('/QOTD', methods=['GET'])
def get_QOTD():
    quotes_list = ['Life is what happens when you’re busy making other plans.”', 
    'Get busy living or get busy dying.', 
    'You only live once, but if you do it right, once is enough.', 
    'Many of life’s failures are people who did not realize how close they were to success when they gave up.', 
    'If you want to live a happy life, tie it to a goal, not to people or things.',
    'Not how long, but how well you have lived is the main thing.',
    'Self-praise is for losers. Be a winner. Stand for something. Always have class, and be humble.',
    'Stay true in the dark & humble in the spotlight.',
    'Keep putting out good. It will come back to you tenfold in unexpected ways.',
    'Here is to the nights we\'ll never remember and to the friends we\'ll never forget ',
    'Tequila may not be the answer but it\s worth a shot ',
    'ashes to ashes dust to dust when life is a bitch, beer is a must ',
    'Life is not a fairytail... If you lose your shoe at midnight...You\'re drunk  ',
    'Here is to quitting driking for good and start drinking for evil',
    'Yesterday is history. Tomorrow is a mystery.',
    'The only thing and old man can say to a young man is that life goes fast so fast. The tragedy is the young man will never believe him',
    'Luck is the residue of hard work.'
    ]
    quote = {'quote': random.choice(quotes_list)}
    print('Request for index page received')
    return jsonify(quote), 200

#HANDLE ERRORS    
@app.errorhandler(Exception)
def server_error(err):
    app.logger.exception(err)
    return jsonify("{exception: "  + str(err) + "}"), 500

if __name__ == '__main__':
    app.run()