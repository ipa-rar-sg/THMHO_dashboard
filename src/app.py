from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<p> Home is here <p>"

@app.route('/init')
def init():
    return "<p> Initialization completed <p>"

@app.route('/massive')
def massive():
    return "<p> Massive <p>"

@app.route('/poll')
def poll():
    return "<p> Polling ... <p>"
