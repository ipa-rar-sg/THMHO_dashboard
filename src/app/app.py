from flask import Flask
from utils import psql, MSG
import queries

app = Flask(__name__)

@app.route('/')
def home():
    return "<p> Home is somewhere we don't know <p>"

@app.route('/insert')
def insert():
    msg = MSG('/src/test.yaml')
    query = queries.insert_into_table('factory', msg)
    ans = psql.exec_query(query, msg.date, *msg.data)
    return f"<p> {ans} <p>"

@app.route('/select')
def select():
    query = queries.select_from_table('factory')
    ans = psql.exec_query(query)
    return f"<p> {ans} <p>"

@app.route('/create')
def create():
    msg = MSG('/src/test.yaml')
    query = queries.create_table('factory', msg)
    ans = psql.exec_query(query)
    return f"<p> {ans} <p>"

