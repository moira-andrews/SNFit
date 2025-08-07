import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import os
import glob

import webbrowser
from threading import Timer


data_dir = os.path.join(os.path.dirname(__file__), "data_dir/")
test_files = glob.glob(data_dir + '*')
print(test_files)

df = pd.read_csv("https://raw.githubusercontent.com/moira-andrews/codeastro_project/refs/heads/main/bolometric_11fe.txt", header=0, sep='\s+')
df = df[['Phase', 'L']]

def fitting_function(time,L,order):
    """_Fitting Supernova Lightcurves_
        Fits supernova lightcurves using polynomials of up to 20th degree.

    Args:
        time (array): Gives the days of observation, usually as mean Julian dates. Units can be days or phase with respect to the time of peak brightness.
        L (array): Can accepts bolometric magnitudes in mag or ergs per second.
        order (Int): Specifies the degree of the fitting polynomial

    Returns:
        array: Fitted light curve parameters
    """
    coeffs = np.polyfit(time,L,order)
    p = np.poly1d(coeffs)
    fit_data = p(time)
    return fit_data


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
    ])

    html.Div([
        dcc.Slider(
        id='variable-slider',
        min=0,
        max=20,
        step=1,
        value=3,
        ),
    ], style={'width': '50%', 'padding': '20px'}),
        

    dcc.Graph(
        id='example-graph'
    )
]) 

@app.callback(
    Output('example-graph', 'figure'),
    Input('variable-slider', 'value')
)
def update_graph(order):
    fig = go.Figure()
    fit_data = fitting_function(df['Phase'],df['L'],order)

    fig.add_trace(go.Scatter(x=df['Phase'], y=df['L'], mode='markers'))
    fig.add_trace(go.Scatter(x=df['Phase'], y=fit_data, mode='lines'))

    fig.update_layout(title='Supernova Lightcurve Fitting',
                      xaxis_title='Phase [days]',
                      yaxis_title='Luminosity [erg/s]',
                      showlegend=False)

    return fig

if __name__ == '__main__':

    def open_browser():
        webbrowser.open_new("http://127.0.0.1:8050/")
    Timer(1, open_browser).start()

    app.run(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter