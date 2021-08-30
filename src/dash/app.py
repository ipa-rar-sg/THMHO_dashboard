import dash
import os
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from sqlalchemy import create_engine

config = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'table': os.getenv('POSTGRES_TABLE'),
    'host': 'postgres'
}

conn_url = f"postgresql+psycopg2://{config['user']}:{config['password']}@{config['host']}:5432/{config['dbname']}"

conn = create_engine(conn_url)

df = pd.read_sql("factory", conn, index_col='date')

data = df.loc['2021-08-16'].to_numpy()[0][1:].reshape((20,20))

fig = go.Figure(data = go.Heatmap(
    z = data,
    x = list(range(0,20)),
    y = list(range(0,20)),
    colorscale = 'bluered',
))

fig.update_layout(
    autosize = False,
    width = 800,
    height = 800,
)

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id='heatmap', figure = fig),
    dcc.Checklist(id='check_live',
                  options=[{'label': 'Live Update', 'value' : 'live'}])
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
