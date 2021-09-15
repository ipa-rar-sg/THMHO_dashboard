import pandas as pd
import numpy as np
import time
import os
import pymongo

config = {
    'collection' : os.getenv('MONGO_COLLECTION'),
    'dbname' : os.getenv('MONGO_INITDB_DATABASE'),
    'user' : os.getenv('MONGO_INITDB_ROOT_USERNAME'),
    'pass' : os.getenv('MONGO_INITDB_ROOT_PASSWORD'),
    'host' : 'mongo',
    'width': int(os.getenv('HEATMAP_WIDTH')),
    'height': int(os.getenv('HEATMAP_HEIGHT'))
}

conn_str = f"mongodb://{config['user']}:{config['pass']}@{config['host']}:27017/{config['dbname']}"

class DataHolder:
    def __init__(self):
        self.config = config
        self.set_connection()
        _init = False
        while not _init:
            try:
                self.df = self.read_df_from_query()
                _init = True
            except:
                time.sleep(2)
        while self.df.empty:
            time.sleep(2)
            self.df = self.read_df_from_query()
        self.last_time = self.df.iloc[-1].name

    def set_connection(self):
        self.conn = pymongo.MongoClient(conn_str)
        self.db = self.conn[self.config['dbname']]
        self.col = self.db[self.config['collection']]

    def read_df_from_query(self, query={}):
        cursor = self.col.find(query)
        return pd.DataFrame(list(cursor)).set_index('date')
        
    def update(self):
        _tmp = self.read_df_from_query({"date": {"$gte": self.last_time}})
        self.df = pd.concat([self.df, _tmp])
        self.last_time = self.df.iloc[-1].name

    def get_data_from_date(self, date):
        return self.df.loc[date].to_numpy()[-1][1:].reshape((self.config['width'], self.config['height']))

    def get_last_data(self):
        return np.array(self.df.iloc[-1]['data']).reshape((self.config['height'], self.config['width']))
