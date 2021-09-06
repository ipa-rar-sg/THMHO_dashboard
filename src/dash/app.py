import dash
import os
import dash_core_components as dcc
import dash_html_components as html
import utils
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from datetime import datetime

data = utils.DataHolder()

fig = go.Figure(data = go.Heatmap(
    z = data.get_last_data(),
    x = list(range(0, data.config['width'])),
    y = list(range(0, data.config['height'])),
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

# @app.callback(Output('heatmap', 'figure'), Input('interval', 'n_intervals'))
# def last_heatmap():
#     data.update()

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
