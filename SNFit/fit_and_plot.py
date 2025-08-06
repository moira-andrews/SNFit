import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output
import plotly.express as px


df = pd.read_csv("https://raw.githubusercontent.com/moira-andrews/codeastro_project/refs/heads/main/bolometric_11fe.txt", header=0, sep='\s+')
df = df[['Phase', 'L']]

def fitting_function(time,L,order):
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