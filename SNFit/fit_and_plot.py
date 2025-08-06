import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import os
import glob

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

app.layout = html.Div(children=[
    html.H1(children='Lightcurve Fitting'),

    dcc.Slider(
        id='variable-slider',
        min=0,
        max=20,
        step=1,
        value=3,
    ),

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

    return fig

if __name__ == '__main__':
    app.run(debug=True)