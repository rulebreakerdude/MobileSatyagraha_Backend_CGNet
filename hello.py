from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/<int:chacha>')
def hello(chacha):
    return '%d' % (int)(2*chacha)