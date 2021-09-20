import dash
import os
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import utils
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from datetime import datetime

data = utils.DataHolder()

resolution = (1920, 1080)
cell_max_size = resolution[1] // data.config['width']

TOLERANCE = 5
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
                {'label': ' Heatmap by selected date', 'value': 'date'}
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
              Input('interval', 'n_intervals'),
              Input('mode', 'value'),
              Input('date_picker', 'date'),
              Input('hour', 'value'),
              Input('minute', 'value'),
              Input('second', 'value'),
              )
def update_last_heatmap(n, _mode, _date, _hour, _min, _sec):
    data.update()
    _tmp_data = None
    _tmp_title = None
    if _mode == 'date' and _date and _hour and _min and _sec:
        _y, _m, _d = map(int, _date.split('-'))
        _tmp_date = datetime(_y, _m, _d, _hour, _min, _sec)
        _tmp_data, _tmp_title = data.get_data_from_date(_tmp_date, TOLERANCE)
    else:
        _tmp_data = data.get_last_data()
        _tmp_title = data.last_time

    fig = go.Figure(data = go.Heatmap(
        z = _tmp_data,
        x = list(range(0, data.config['width'])),
        y = list(range(0, data.config['height'])),
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
    ))
    fig.update_layout(
        autosize = False,
        width = 1.5*cell_max_size * data.config['width'],
        height = 1.5*cell_max_size * data.config['height'],
        title = f'<b>Showing heatmap: {_tmp_title}</b>',
        title_x = 0.5,
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
