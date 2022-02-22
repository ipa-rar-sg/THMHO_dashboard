import dash
import os
import numpy as np
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import utils
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from datetime import datetime

data = utils.DataHolder()

'''
        colorscale = [
                        [0, "rgb(249, 237, 230)"],
                        [0.1, "rgb(249, 237, 230)"],

                        [0.1, "rgb(251, 227, 213)"],
                        [0.2, "rgb(251, 227, 213)"],

                        [0.2, "rgb(252, 215, 194)"],
                        [0.3, "rgb(252, 215, 194)"],

                        [0.3, "rgb(249, 196, 169)"],
                        [0.4, "rgb(249, 196, 169)"],

                        [0.4, "rgb(246, 177, 145)"],
                        [0.5, "rgb(246, 177, 145)"],

                        [0.5, "rgb(240, 155, 122)"],
                        [0.6, "rgb(240, 155, 122)"],

                        [0.6, "rgb(229, 130, 103)"],
                        [0.7, "rgb(229, 130, 103)"],

                        [0.7, "rgb(218, 106, 85)"],
                        [0.8, "rgb(218, 106, 85)"],

                        [0.8, "rgb(206, 81, 70)"],
                        [0.9, "rgb(206, 81, 70)"],

                        [0.9, "rgb(255, 255, 255)"],
                        [1.0, "rgb(255, 255, 255)"]
        ]
'''

resolution = (1920, 1080)
cell_max_size = resolution[1] // data.config['width']
default_marks = {i: {'label': f'{i}'} for i in range(1,1)}

TOLERANCE = 40
# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}
# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10p'
}
TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}

controls = dbc.FormGroup(
    [
        html.Div([
        html.H5('Show'),
        html.P(),
        dcc.RadioItems(
            id = 'mode',
            options = [
                {'label': ' Last heatmap (Auto update)', 'value': 'auto'},
                {'label': ' Heatmap by selected date', 'value': 'date'},
                {'label': ' Slider of last searched date', 'value': 'slide'}
            ],
            value = 'auto',
            labelStyle={'display': 'block'}
        ),
        html.H5('Select Date'),
        dcc.DatePickerSingle(id='date_picker'),
        html.P(),
        html.H5('Select Time'),
        html.P(),
        html.H6('Hour'),
        dcc.Dropdown(
            id = 'hour',
            options = [{'label': str(i), 'value': i} for i in range(24)]
        ),
        html.H6('Minute'),
        dcc.Dropdown(
            id = 'minute',
            options = [{'label': str(i), 'value': i} for i in range(60)]
        ),
        html.H6('Second'),
        dcc.Dropdown(
            id = 'second',
            options = [{'label': str(i), 'value': i} for i in range(60)]
        ),
        html.P(),
        html.H5('Last heatmaps'),
        html.P(),
        dcc.Slider(
            id = 'slider',
            marks = default_marks,
            min = 1,
            max = 10,
            value = 1,
            step = None,
            updatemode = 'drag',
            included = False
        )
    ]   )
    ]
)

sidebar = html.Div(
    [
        html.H2('Parameters', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)

content_first_row = dbc.Row(
    [
        dcc.Graph(id='heatmap'),
        dcc.Interval(
            id = 'interval',
            interval = 3 * 1000, # Milliseconds
            n_intervals = 0
        ),
    ]
)

content = html.Div(
    [
        html.H2('Temporal Heat Map of Human Occupancy Dashboard', style=TEXT_STYLE),
        html.Hr(),
        content_first_row
    ],
    style=CONTENT_STYLE
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([sidebar, content])

@app.callback(Output('heatmap', 'figure'),
              Output('slider', 'marks'),
              Input('interval', 'n_intervals'),
              Input('mode', 'value'),
              Input('date_picker', 'date'),
              Input('hour', 'value'),
              Input('minute', 'value'),
              Input('second', 'value'),
              Input('slider', 'value'),
              )
def update_last_heatmap(n, _mode, _date, _hour, _min, _sec, _nheat):
    data.update()
    _tmp_data = None
    _tmp_title = None
    marks = default_marks

    if _mode == 'date' and _date and _hour and _min and _sec:
        _y, _m, _d = map(int, _date.split('-'))
        _tmp_date = datetime(_y, _m, _d, _hour, _min, _sec)
        _tmp_data, _tmp_title = data.get_data_from_date(_tmp_date, TOLERANCE)

    elif _mode == 'slide' and _date and _hour and _min and _sec:
        _y, _m, _d = map(int, _date.split('-'))
        _tmp_date = datetime(_y, _m, _d, _hour, _min, _sec)
        data.get_data_from_date_bunch(_tmp_date, TOLERANCE)
        if not data.timed_data:
            _tmp_data = np.zeros(data.shape)
            _tmp_title = "Previously searched date NOT FOUND"

        else:
            _tmp_len = len(data.timed_data)
            marks = {i: {'label': f'{i}'} for i in range(1, _tmp_len + 1)}
            _tmp_data = data.generate_csr(data.timed_data[_nheat - 1])
            _tmp_data = data.decode(_tmp_data)
            _tmp_title = f'Showing heatmap: {data.timed_data[_nheat - 1]["date"]}'

    else:
        _tmp_data = data.get_last_data()
        _tmp_title = f'Showing heatmap: {data.last_time}'

    fig = go.Figure(data = go.Heatmap(
        z = _tmp_data,
        x = list(range(0, data.config['width'])),
        y = list(range(0, data.config['height'])),
        colorscale = "thermal",
        )
    )
    fig.update_layout(
        autosize = False,
        width = 1.5*cell_max_size * data.config['width'],
        height = 1.5*cell_max_size * data.config['height'],
        title = f'<b>{_tmp_title}</b>',
        title_x = 0.5,
    )
    return fig, marks

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
