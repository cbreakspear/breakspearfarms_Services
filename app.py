#!flask/bin/python
from cProfile import run
import pyodbc
import sys
from flask import Flask, jsonify, request, abort, render_template
from flask_cors import CORS
from datetime import datetime



servicesVersion = {

            'version': "1.2",
            'author': "Craig Breakspear",
            'lastupdate': "02-08-2022"
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
        sql = "INSERT INTO dbo.subscription (emailaddress, entry_date) VALUES ('" + request.json['email'] + \
            "','" + str(now) + "')"
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};Server=tcp:breakspearfarms.database.windows.net;Database=breakspearfarmsDB;Port=1433;uid=cbreakspear;pwd=Destination2060')
        cursor = cnxn.cursor()
        cursor.execute(sql)
        cnxn.commit()
        cnxn.close()
        print("Subscription Successfully Inserted") 
        task = {

            'customername': request.json['customername'],
            'email': request.json['email']
        }
        return jsonify({'STATUS': "SUCCESSFUL INSERTION OF: " + task["email"]}), 201

''' RETURNS THE VERSION OF THE SERVICES IT IS CURRENTLY WORKING UNDER'''
@app.route('/bfsVersion', methods=['GET'])
def get_servicesversion():
    
    return jsonify(servicesVersion), 200



#HANDLE ERRORS    
@app.errorhandler(Exception)
def server_error(err):
    app.logger.exception(err)
    return jsonify("{exception: "  + str(err) + "}"), 500

if __name__ == '__main__':
    app.run()