import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import webbrowser
from threading import Timer
from SNFit.format_data import *

app = Dash()

header_style = {
    'background': 'linear-gradient(135deg, #6e48aa 0%, #9d50bb 100%)',
    'color': 'white',
    'padding': '1.5rem',
    'text-align': 'center',
    'border-radius': '0 0 10px 10px',
    'box-shadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
    'margin-bottom': '2rem'
}

file_dict = file_formatting()

app.layout = html.Div(children=[
    # Header moderno con imagen
    html.Div([
        html.Div([
            html.Img(
                src='https://raw.githubusercontent.com/plotly/dash-sample-apps/main/apps/dash-astronomy/supernova.png',  # Reemplaza con tu URL
                style={'height': '60px', 'margin-right': '15px'}
            ),
            html.H1(
                'SNFit: Supernova Lightcurve Fitting',
                style={'margin': '0', 'font-family': 'Arial, sans-serif', 'font-weight': 'bold'}
            )
        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'})
    ], style=header_style),

    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Button('Upload CSV File', style={'padding': '10px 20px', 'font-size': '16px'}),
            multiple=False,
        )
    ]),

    html.Div([
        dcc.Slider(
        id='variable-slider',
        min=0,
        max=20,
        step=1,
        value=3,
        marks=None,
        tooltip={
            "always_visible": True,
            "template": "{value}"
        },
        ),
    ], style={'width': '50%', 'padding': '20px'}),
    
    html.Div([
        dcc.Dropdown(options=[{'label': k, 'value': v} for k, v in file_dict.items()],
            value=file_dict['SN 2011fe'],
            id='dropdown-options'
            ),
        
        html.Div(id='dd-output-container')
        ], style={'width': '50%', 'padding': '20px'}),
        

    dcc.Graph(
        id='example-graph'
    )
]) 

@app.callback(
    Output('dd-output-container', 'children'),
    Output('example-graph', 'figure'),
    Input('dropdown-options', 'value'),
    Input('variable-slider', 'value')
)
def update_figure(file, order):
    lc = LightCurve(file)
    df = lc.df
    fig = go.Figure()

    time_col = next((c for c in df.columns if c.lower() in LightCurve.time_colnames), df.columns[0])
    value_col = next((c for c in df.columns if c.lower() in LightCurve.value_colnames), df.columns[1])
    
    offset = 0
    if time_col.lower() == 'mjd':
        offset = min(df[time_col])
    fit_data = fitting_function(df[time_col] - offset, df[value_col], order)

    fig.add_trace(go.Scatter(x=df[time_col] - offset, y=df[value_col], mode='markers'))
    fig.add_trace(go.Scatter(x=df[time_col] - offset, y=fit_data, mode='lines'))

    fig.update_layout(title='Supernova Lightcurve Fitting',
                     xaxis_title=f'{time_col} - {offset} [days]',
                     yaxis_title=f'{value_col}',
                     showlegend=False)
    
    if value_col == 'Mag':
        fig.update_yaxes(autorange="reversed")
        
    return f"Loaded file: {file}", fig

if __name__ == '__main__':

    def open_browser():
        webbrowser.open_new("http://127.0.0.1:8050/")
    Timer(1, open_browser).start()

    app.run()