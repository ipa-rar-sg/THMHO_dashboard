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
    'host_no_csr' : 'mongo',
    'host_csr': 'mongocsr'
}

conn_str = f"mongodb://{config['user']}:{config['pass']}@{config['host_no_csr']}:27017/{config['dbname']}"
conn_str_csr = f"mongodb://{config['user']}:{config['pass']}@{config['host_csr']}:27018/{config['dbname']}"

conn = pymongo.MongoClient(conn_str, connect=False)
conn_db = conn[config['dbname']]
conn_col = conn_db[config['collection']]

conn_csr = pymongo.MongoClient(conn_str_csr, connect=False)
conn_db_csr = conn_csr[config['dbname']]
conn_col_csr = conn_db_csr[config['collection']]

@app.route('/')
def home():
    return "API for Managing the Database"

@app.route('/insert', methods=['POST'])
def insert():
    '''
    Inserts registry in the database.
    POST request must have a json body, possible content of body:
    - name: string identificator for the mask
    - width: int
    - height: int
    - date: string containing valid timestamp
    - indices: list of int stating the indices of the sparse (csr) matrix
    - indptr: list of int stating the indptr of the sparse (csr) matrix
    '''
    body = request.json
    reg_id = conn_col.insert_one(body).inserted_id
    reg_id2 = conn_col_csr.insert_one(body).inserted_id
    return f'Inserted successfully registry with new id: Mongo: {reg_id} & {reg_id2}'

@app.route('/select', methods=['GET'])
def select():
    '''
    '''
    pass

