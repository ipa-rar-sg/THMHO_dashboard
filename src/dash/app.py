import dash
import os
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import time
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from sqlalchemy import create_engine
from datetime import datetime

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

conn = create_engine(conn_url)

def get_date(date):
    return df.loc[date].to_numpy()[-1][1:].reshape((config['width'], config['height']))

df = pd.read_sql(config['table'], conn, index_col='date')

while df.empty:
    time.sleep(5)
    df = pd.read_sql(config['table'], conn, index_col='date')

data = df.iloc[-1]
last_time = data.name
data = data.to_numpy()[1:].reshape((config['width'], config['height']))

# df = pd.read_sql("SELECT * FROM factory WHERE date < '2021-08-16 13:56:43.028817';", conn, index_col='date')


fig = go.Figure(data = go.Heatmap(
    z = data,
    x = list(range(0, config['width'])),
    y = list(range(0, config['height'])),
    colorscale = 'thermal'
    # [[0, 'rgb(63,0,145)'], [0.5, 'rgb(219,107,2)'], [1, 'rgb(255,229,143)']],
))

fig.update_layout(
    autosize = False,
    width = 800,
    height = 800,
)

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='heatmap', figure = fig),
    # dcc.Checklist(id='check_live',
    #               options=[{'label': 'Live Update', 'value' : 'live'}])
    # dcc.Interval(
    #     id = 'interval',
    #     interval = 30 * 1000, # Milliseconds
    #     n_intervals = 0
    # )
])

# @app.callback(Output('heatmap', 'children'), Input('interval', 'n_intervals'))
# def last_heatmap

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
