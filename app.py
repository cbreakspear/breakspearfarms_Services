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
    quotes_list = ['Life is what happens when you???re busy making other plans.:John Lennon', 
    'Get busy living or get busy dying.:Stephen King', 
    'You only live once, but if you do it right, once is enough.:Mae West', 
    'Many of life???s failures are people who did not realize how close they were to success when they gave up.:Thomas Edison', 
    'If you want to live a happy life, tie it to a goal, not to people or things.:Albert Einstein',
    'Not how long, but how well you have lived is the main thing.:Lucius Annaeus Seneca',
    'Self-praise is for losers. Be a winner. Stand for something. Always have class, and be humble.:John Madden',
    'Stay true in the dark & humble in the spotlight.:Harold B. Lee',
    'Keep putting out good. It will come back to you tenfold in unexpected ways.:Farrah Gray',
    'Here is to the nights we\'ll never remember and to the friends we\'ll never forget.',
    'Tequila may not be the answer but it\s worth a shot.',
    'ashes to ashes dust to dust when life is a bitch, beer is a must .',
    'Life is not a fairytail... If you lose your shoe at midnight...You\'re drunk. ',
    'Here is to quitting driking for good and start drinking for evil.',
    'Yesterday is history. Tomorrow is a mystery.:Bill Keane',
    'The only thing and old man can say to a young man is that life goes fast so fast. The tragedy is the young man will never believe him.',
    'Luck is the residue of hard work.:Melissa Pine',
    'Here is to those that wish us well....and those who don\'t...can go to hell:Elaine ',
    'Here is to father time...time flies when you\'re having rum.:Donna Aylor ',
    'To those that know me. Never take advice from me...you\'ll end up drunk:Rusafu ',
    'You can\'t drink all day if you don\'t start in the morning:Celia Rivenbark ',
    'I feel sorry for those that don\'t drink because when they wake up in the morning that\'s the best they are going to feel all day: Frank Sinatra ',
    'Alcohol may be man\'s worst enemy, but the bible says love your enemy.:Frank Sinatra',
    'Age is just a number. It\'s totally irrelevant unless, of course, you happen to be a bottle of wine.:Joan Collins',
    'Time is never wasted when you\'re wasted all the time:Catherine Zandonella',
    'Here\'s to alcohol, the rose colored glasses of life:F. Scott Fitzgerald',
    'REMEBER. You are braver than you believe, stronger than you seem, and smarter than you think. But most important of all, even if we\'re apart, I\'ll always be with you.:AA Milne',
    'I\'m sober enough to know what I\'m doing.....But drunk enough to enjoy doing it:John Dunsworth',
    'Here is to Cheating, Stealing, Fighting and drinking. If you cheat, May you cheat death. If it\'s stealing, may you steal a womans heart. if you fight, may you fight for a brother. If you drink, may you drink with me:Irish Quote',
    'Here is to the people that follow the masses but don\'t forget, sometimes the M is silent. ',
    'May you die in bed at 95, shot by a jealous spouse. ',
    'Here???s to a long life and a merry one. A quick death and an easy one. A pretty girl and an honest one. A cold pint??? and another one! ',
    'May the best day of the past together be the worst day of your future. ',
    'May your home always be too small to hold all your friends. ',
    'There are good ships, and there are wood ships, The ships that sail the sea. But the best ships, are friendships, And may they always be. ',
    'Here???s to the man with woman so fair, And here???s to the woman with man so rare!',
    'If the destination in life is death. Why not take the scenic route?:Kalvin John Barry JR.'
    ]
    quote = {'quote': random.choice(quotes_list)}
    print('Request for Quote Received')
    return jsonify(quote), 200

#HANDLE ERRORS    
@app.errorhandler(Exception)
def server_error(err):
    app.logger.exception(err)
    return jsonify("{exception: "  + str(err) + "}"), 500

if __name__ == '__main__':
    app.run()