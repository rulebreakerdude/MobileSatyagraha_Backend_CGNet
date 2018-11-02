from flask import Flask
api = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'