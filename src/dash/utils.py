import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
import time
import os
import pymongo
from datetime import datetime, timedelta

config = {
    'collection' : os.getenv('MONGO_COLLECTION'),
    'dbname' : os.getenv('MONGO_INITDB_DATABASE'),
    'user' : os.getenv('MONGO_INITDB_ROOT_USERNAME'),
    'pass' : os.getenv('MONGO_INITDB_ROOT_PASSWORD'),
    'host' : 'localhost',
    'width': int(os.getenv('HEATMAP_WIDTH')),
    'height': int(os.getenv('HEATMAP_HEIGHT'))
}

conn_str = f"mongodb://{config['user']}:{config['pass']}@{config['host']}:27017/{config['dbname']}"

class DataHolder:
    def __init__(self):
        self.config = config
        self.shape = (self.config['height'], self.config['width'])
        self.timed_data = None
        self.last_data = []
        self.set_connection()
        self.read_mask()
        self.last_time = (datetime.now() - timedelta(0, 60)).isoformat()
        self.update()
        while not self.last_data:
            self.update()

    def set_connection(self):
        self.conn = pymongo.MongoClient(conn_str)
        self.db = self.conn[self.config['dbname']]
        self.col = self.db[self.config['collection']]

    def read_from_query(self, query={}):
        cursor = self.col.find(query)
        data = list(cursor)
        return data
        # df = True
        # if df:
        #     return pd.DataFrame(data)

    def generate_csr(self, dbentry):
        return csr_matrix((
            np.full((len(dbentry['indices']),), 100),
            np.array(dbentry['indices']),
            np.array(dbentry['indptr'])
        ), shape = self.shape)

    def read_mask(self):
        result = self.read_from_query({"name": "base_mask"})
        while not result:
            result = self.read_from_query({"name": "base_mask"})
        mask = result[0]
        csr = self.generate_csr(mask)
        self.mask = csr.toarray()
        self.mask = (~(self.mask.astype(bool))).astype(int)

    def decode(self, csr):
        return (self.mask*100) + csr.toarray()
        
    def update(self):
        _tmp = self.read_from_query({"date": {"$gte": self.last_time}})
        if _tmp:
            self.last_data = _tmp[-1]
            self.last_time = self.last_data['date']

    def get_data_from_date(self, date, delta=1):
        low = (date - timedelta(0, delta)).isoformat()
        high = (date + timedelta(0, delta)).isoformat()
        _tmp = self.read_df_from_query({"date": {"$gte": low, "$lte": high}})
        if _tmp.empty:
            return np.zeros(self.shape), f'{date.isoformat()} NOT FOUND'
        _tmp = _tmp.set_index('date').iloc[-1]
        _tmp = generate_csr(_tmp)
        _tmp = decode(_tmp)
        return _tmp, date.isoformat()

    def get_data_from_date_bunch(self, date, delta=60):
        low = (date - timedelta(0, delta)).isoformat()
        high = (date + timedelta(0, delta)).isoformat()
        _tmp = self.read_df_from_query({"date": {"$gte": low, "$lte": high}})
        if not _tmp.empty:
            _tmp = _tmp.set_index('date')
        self.timed_data = _tmp.iloc[-10:]

    def get_last_data(self):
        _tmp = generate_csr(self.last_data)
        return decode(_tmp)

