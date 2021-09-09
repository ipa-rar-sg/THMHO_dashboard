import pandas as pd
import numpy as np
import time
import os
from sqlalchemy import create_engine

config = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'table': os.getenv('POSTGRES_TABLE'),
    'width': int(os.getenv('HEATMAP_WIDTH')),
    'height': int(os.getenv('HEATMAP_HEIGHT')),
    'host': 'postgres'
}

conn_url = f"postgresql+psycopg2://{config['user']}:{config['password']}@{config['host']}:5432/{config['dbname']}"

def get_date(date):
    return df.loc[date].to_numpy()[-1][1:].reshape((config['width'], config['height']))

class DataHolder:
    def __init__(self):
        self.config = config
        self.conn = create_engine(conn_url)
        _init = False
        while not _init:
            try:
                self.df = pd.read_sql(self.config['table'], self.conn, index_col='date')
                _init = True
            except:
                time.sleep(2)
        while self.df.empty:
            time.sleep(3)
            self.df = pd.read_sql(self.config['table'], self.conn, index_col='date')
        self.last_time = self.df.iloc[-1].name

    def update(self):
        _tmp = pd.read_sql(f"SELECT * FROM {self.config['table']} WHERE date > '{self.last_time}';", self.conn, index_col='date')
        self.df = pd.concat([self.df, _tmp])
        self.last_time = self.df.iloc[-1].name

    def get_data_from_date(self, date):
        return self.df.loc[date].to_numpy()[-1][1:].reshape((self.config['width'], self.config['height']))

    def get_last_data(self):
        return self.df.iloc[-1].to_numpy()[1:].reshape((self.config['height'], self.config['width']))
