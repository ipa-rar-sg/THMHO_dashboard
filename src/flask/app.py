from flask import Flask, request, jsonify
import pymongo
import os
import time
import numpy as np
from scipy.sparse import csr_matrix
from datetime import datetime, timedelta

app = Flask(__name__)

config = {
    'collection' : os.getenv('MONGO_COLLECTION'),
    'dbname' : os.getenv('MONGO_INITDB_DATABASE'),
    'user' : os.getenv('MONGO_INITDB_ROOT_USERNAME'),
    'pass' : os.getenv('MONGO_INITDB_ROOT_PASSWORD'),
    'host' : 'mongo'
}

conn_str = f"mongodb://{config['user']}:{config['pass']}@{config['host']}:27018/{config['dbname']}"

conn = pymongo.MongoClient(conn_str, connect=False)
conn_db = conn[config['dbname']]
conn_col = conn_db[config['collection']]

mask = None

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
    return f'Inserted successfully registry with new id: {reg_id}'

@app.route('/select', methods=['GET'])
def select():
    '''
    Retrieves registry from database based on the following expected query params:
    - param date: string in the format: YYYY-MM-DD-HH-mm
    - param [optional] delta: Integer specifying a delta of second for the searched date
    Otherwise defaults to 30 seconds
    - returns: If registry found with provided data returns a JSON with it, otherwise
    a string mentioning that no data was found
    '''

    global mask

    if mask is None:
        cursor = conn_col.find({"name": "base_mask"})
        results = list(cursor)
        if results:
            mask = results[-1]
            csr = csr_matrix((
                np.full((len(mask['indices']),), 100),
                np.array(mask['indices']),
                np.array(mask['indptr'])
            ), shape = (mask['height'], mask['width']))
            mask = csr.toarray()
            mask = (~(mask.astype(bool))).astype(int)
        else:
            return "No base mask found, therefore no data present on data base"

    date = None
    delta = 30

    if 'date' not in request.args:
        return 'Date query parameter required and was not given'
    try:
        Y, M, D, H, m = map(int, request.args['date'].split('-'))
        date = datetime(Y, M, D, H, m)
    except:
        return "Date entered in invalid format, it should be: YYYY-MM-DD-HH-mm"

    if 'delta' in request.args:
        try:
            delta = int(request.args['delta'])
        except:
            return "delta query param must be an integer"

    low = (date - timedelta(0, delta)).isoformat()
    high = (date + timedelta(0, delta)).isoformat()

    cursor = conn_col.find({"date": {"$gte": low, "$lte": high}})
    results = list(cursor)
    if results:
        mid = results[len(results) // 2]
        date = mid['date']
        data = csr_matrix((
                np.array(mid['data']),
                np.array(mid['indices']),
                np.array(mid['indptr'])
            ), shape = mask.shape)
        data = (mask * 100) + data.toarray()
        return jsonify({"date": date,
                        "shape": mask.shape,
                        "data": data.tolist()})
    else:
        return f"No results found for entered date and delta of {delta} seconds"

