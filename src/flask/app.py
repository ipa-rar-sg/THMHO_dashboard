from flask import Flask, request
from utils import psql, MSG
import queries
import os

app = Flask(__name__)

table = os.getenv('POSTGRES_TABLE')


@app.route('/')
def home():
    return "API for Managing the Postgres Database"


@app.route('/insert', methods=['POST'])
def insert():
    '''
    Inserts registry in the database.
    POST request must have a json body with the following keys:
    - width: int
    - height: int
    - date: string containing valid timestamp
    - data: list of int containing the heatmap data
    '''
    body = request.json
    query = queries.insert_into_table(table, body)
    return psql.exec_query(query, body['date'], *body['data'])


@app.route('/select', methods=['GET'])
def select():
    '''
    Selects registries from the database.
    GET request with limit as query param.
    Send limit as 0 to obtain all entries.
    '''
    limit = int(request.args.get('limit'))
    query = queries.select_from_table(table, limit)
    return psql.exec_query(query)


@app.route('/create_table', methods=['POST'])
def create():
    '''
    Creates the table in the database.
    POST request must have a json body with the following keys:
    - width: int
    - height: int
    '''
    query = queries.create_table(table, request.json)
    return psql.exec_query(query)
