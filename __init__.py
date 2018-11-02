import os

from flask import Flask
from flask import request
import hashlib
from db_repo import *



mydb=database_flaskr()



app = Flask(__name__)



@app.route('/hello', methods=['GET'])
def hello():
	if request.method == 'GET':
		return 'Hello beta'
	
@app.route('/plist')
def plist():
	return str(mydb.fetchAll())
	
@app.route('/pblock/<int:s>/<int:e>')
def pblock(s,e):
	e=e-s
	return str(mydb.fetchBlock(s,e))
	
@app.route('/pitem/<problem_id>')
def pitem(problem_id):
	return str(mydb.fetchOne(problem_id))
	
@app.route('/signup', methods=['POST'])
def signup():
	if request.form['inviteCode']=="swara":
		if mydb.userExists(request.form['username']):
			return 'User Exists'
		else:
			mydb.insertUser(request.form['username'],hashlib.sha256(request.form['password']).hexdigest(),request.form['name'],request.form['email'])
			return 'Successful Signup'
	else:
		return 'Retry'
	
@app.route('/login', methods=['POST'])
def login():
	if not mydb.userExists(request.form['username']):
		return str({"reply":'User does not exist'})
	elif mydb.authenticateUser(request.form['username'],hashlib.sha256(request.form['password']).hexdigest())=="incorrect password":
		return str({"reply":'Login Unsuccessful'})
	else:
		return str({"reply":'Successful Login',"name":mydb.authenticateUser(request.form['username'],hashlib.sha256(request.form['password']).hexdigest())})

@app.route('/getSession', methods=['GET'])
def getSession():
	return str(mydb.getSessionID())

@app.route('/userCount/<problem_id>')
def userCount(problem_id):
	return str(mydb.userCount(problem_id))	

@app.route('/canAdoptProblem/<username>')
def canAdoptProblem(username):
	if(mydb.canAdoptProblem(username)=="Yes"):
		return "Yes"
	else:
		return "No"

@app.route('/adoptProblem/<username>/<problem_id>')
def adoptProblem(username,problem_id):
	return mydb.adoptProblem(username,problem_id)
	
@app.route('/unAdoptProblem/<username>/<problem_id>')
def unAdoptProblem(username,problem_id):
	return mydb.unAdoptProblem(username,problem_id)

@app.route('/problemAgainstUser/<username>')
def problemAgainstUser(username):
	return str(mydb.fetchProblemAgainstUser(username))
	
@app.route('/registerComment', methods=['POST'])
def registerComment():
	return mydb.registerComment(request.form['username'],request.form['problem_id'],request.form['comment'])

if __name__=="__main__":
	app.run(host="0.0.0.0")
	
	
	
	