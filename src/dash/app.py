import dash
import os
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import utils
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from datetime import datetime

data = utils.DataHolder()

resolution = (1920, 1080)
cell_max_size = resolution[1] // data.config['width']

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

@app.callback(Output('heatmap', 'figure'), Input('interval', 'n_intervals'))
def update_last_heatmap(n):
    data.update()
    fig = go.Figure(data = go.Heatmap(
        z = data.get_last_data(),
        x = list(range(0, data.config['width'])),
        y = list(range(0, data.config['height'])),
        colorscale = 'thermal'
        # [[0, 'rgb(63,0,145)'], [0.5, 'rgb(219,107,2)'], [1, 'rgb(255,229,143)']],
    ))
    fig.update_layout(
        autosize = False,
        width = cell_max_size * data.config['width'],
        height = cell_max_size * data.config['height'],
        title = f'<b>Showing heatmap: {data.last_time}</b>',
        title_x = 0.5,
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
