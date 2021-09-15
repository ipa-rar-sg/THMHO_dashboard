from flask import Flask, request
import pymongo
import os
import time

app = Flask(__name__)

config = {
    'collection' : os.getenv('MONGO_COLLECTION'),
    'dbname' : os.getenv('MONGO_INITDB_DATABASE'),
    'user' : os.getenv('MONGO_INITDB_ROOT_USERNAME'),
    'pass' : os.getenv('MONGO_INITDB_ROOT_PASSWORD'),
    'host' : 'mongo'
}

conn_str = f"mongodb://{config['user']}:{config['pass']}@{config['host']}:27017/{config['dbname']}"

@app.route('/')
def home():
    return "API for Managing the Database"

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
    conn = pymongo.MongoClient(conn_str, connect=False)
    conn_db = conn[config['dbname']]
    conn_col = conn_db[config['collection']]
    body = request.json
    reg_id = conn_col.insert_one(body).inserted_id
    return f'Inserted successfully registry with new id: {reg_id}'

@app.route('/select', methods=['GET'])
def select():
    '''
    Selects registries from the database.
    GET request with limit as query param.
    Send limit as 0 to obtain all entries.
    '''
    limit = int(request.args.get('limit'))
    return 'Hola'

