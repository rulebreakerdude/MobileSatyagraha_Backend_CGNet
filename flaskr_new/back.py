import os

from flask import Flask
from flask import request
from db_repo import *



mydb=database_flaskr()



application = Flask(__name__)



@application.route('/hello', methods=['GET'])
def hello():
	if request.method == 'GET':
		return 'Hello beta'
	
	
	
@application.route('/plist')
def plist():
	return str(mydb.fetchAll())
	
	
	
@application.route('/pitem/<problem_id>')
def pitem(problem_id):
	return str(mydb.fetchOne(problem_id))
	
	
	
@application.route('/signup', methods=['POST'])
def signup():
	if request.form['inviteCode']=="swara":
		if mydb.userExists(request.form['username']):
			return 'User Exists'
		else:
			mydb.insertUser(request.form['username'],request.form['password'],request.form['name'],request.form['email'])
			return 'Successful Signup'
	else:
		return 'Retry'
	
	
	
@application.route('/login', methods=['POST'])
def login():
	if not mydb.userExists(request.form['username']):
		return str({"reply":'User does not exist'})
	elif mydb.authenticateUser(request.form['username'],request.form['password'])=="incorrect password":
		return str({"reply":'Login Unsuccessful'})
	else:
		return str({"reply":'Successful Login',"name":mydb.authenticateUser(request.form['username'],request.form['password'])})

		
		
@application.route('/userCount/<problem_id>')
def userCount(problem_id):
	return str(mydb.userCount(problem_id))	



	
@application.route('/canAdoptProblem/<username>')
def canAdoptProblem(username):
	if(mydb.canAdoptProblem(username)):
		return "Yes"
	else:
		return "No"


		
@application.route('/adoptProblem/<username>/<problem_id>')
def adoptProblem(username,problem_id):
	return mydb.adoptProblem(username,problem_id)

	
	
if __name__=="__main__":
	application.run()