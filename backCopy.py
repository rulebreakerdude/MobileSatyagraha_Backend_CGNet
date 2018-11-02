import os

from flask import Flask
from flask import request


app = Flask(__name__)



@app.route('/hello', methods=['GET'])
def hello():
	if request.method == 'GET':
		return 'Hello beta'
		
@app.route('/helloji', methods=['GET'])
def helloji():
	if request.method == 'GET':
		return 'Hello betaji'
	
if __name__=="__main__":
	app.run(host="0.0.0.0")