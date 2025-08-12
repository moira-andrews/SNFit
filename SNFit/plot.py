import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, State
from dash import dash_table
import webbrowser
from threading import Timer
from SNFit.load_file import load_dir
from SNFit.lightcurve import LightCurve
from SNFit.lc_analysis import fitting_function
import base64
import io

external_stylesheets = [
    "https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.4/css/bulma.min.css"
]
app = Dash(external_stylesheets=external_stylesheets)
file_dict = load_dir()

def main():
    """
    Set up the Dash app layout, including header, upload, slider, dropdown, and graph components.

    Returns:
        None
    """
    header_style = {
        'background': 'linear-gradient(135deg, #6e48aa 0%, #9d50bb 100%)',
        'color': 'white',
        'padding': '1.5rem',
    }
    app.layout = html.Div(children=[
        html.Div([
            html.Div([
                html.H1(
                    'SNFit: Supernova Lightcurve Fitting',
                    style={'margin': '0', 'font-family': 'Arial, sans-serif', 'font-weight': 'bold', 'font-size': '26px'}
                )
            ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'})
        ], style=header_style),

        html.Div([
            html.Div([
                dcc.Graph(id='example-graph'),
                html.Div(id='dd-output-container')
            ], style={'flex': '2', 'padding': '20px', 'minWidth': '400px'}),

            html.Div([
                dcc.Upload(
                    id='upload-data',
                    children=html.Button('Upload CSV or TXT File', style={'padding': '10px 20px', 'font-size': '16px'}),
                    multiple=False,
                style={'marginTop': '60px'} ),
                dcc.Store(id='store'),
                html.Div(id='output-data-upload'),
                html.Div(id='file-label', style={'marginTop': '20px'}),
                dcc.Dropdown(
                    id='dropdown-options',
                    options=[{'label': k, 'value': v} for k, v in file_dict.items()],
                    value=file_dict['SN 2011fe'] if 'SN 2011fe' in file_dict else list(file_dict.values())[0],
                    style={'marginTop': '5px','font-family': 'Arial, sans-serif', 'font-size': '16px'}
                ),
                html.Div([
                    html.Label("Select Time Column:"),
                    dcc.Dropdown(id='time-col-dropdown', clearable=False, style={'marginTop': '10px'}),
                ]),
                html.Div([
                    html.Label("Select Brightness Column:"),
                    dcc.Dropdown(id='value-col-dropdown', clearable=False, style={'marginTop': '10px'}),
                ]),
                html.Div([
                    html.Label("Polynomial Order"),
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
                ], style={'font-family': 'Arial, sans-serif', 'font-size': '20px','marginTop': '40px'}),
                html.Div([
                    html.Label("Phase Range"),
                    html.Div([
                        dcc.Input(
                            id='phase-min',
                            type='number',
                            placeholder='Min',
                            value=-100,
                            style={
                                'width': '120px',
                                'height': '40px',
                                'marginRight': '20px',
                                'fontSize': '1.2em',
                                'padding': '10px',
                                'borderRadius': '8px',
                                'border': '1px solid #aaa',
                                'backgroundColor': '#f8f8ff',
                            }
                        ),
                        dcc.Input(
                            id='phase-max',
                            type='number',
                            placeholder='Max',
                            value=100,
                            style={
                                'width': '120px',
                                'height': '40px',
                                'fontSize': '1.2em',
                                'padding': '10px',
                                'borderRadius': '8px',
                                'border': '1px solid #aaa',
                                'backgroundColor': '#f8f8ff',
                            }
                        ),
                    ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center'})
                ], style={'font-family': 'Arial, sans-serif', 'font-size': '20px','marginTop': '20px'}),
            ], style={'flex': '1', 'padding': '20px', 'minWidth': '300px'}),
        ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'flex-start', 'width': '100%'})
    ])
            

def parse_contents(contents, filename):
    """
    Parse uploaded file contents into a pandas DataFrame.

    Args:
        contents (str): The base64-encoded file contents from the upload component.
        filename (str): The name of the uploaded file.

    Returns:
        pd.DataFrame: The parsed data as a DataFrame.

    Raises:
        ValueError: If the file type is not supported.
    """
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if filename.lower().endswith('.csv'):
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    elif filename.lower().endswith('.txt'):
        # Try whitespace or tab delimited
        try:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), delim_whitespace=True)
        except Exception:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    else:
        raise ValueError(f"Unsupported file type: {filename}")
    return df


@app.callback(
    Output('dropdown-options', 'options'),
    Output('dropdown-options', 'value'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('dropdown-options', 'options'),
    State('dropdown-options', 'value')
)
def update_dropdown_options(upload_contents, upload_filename, options, current_value):
    """
    Update the dropdown options and value when a new file is uploaded.

    Args:
        upload_contents (str): The base64-encoded contents of the uploaded file.
        upload_filename (str): The name of the uploaded file.
        options (list): The current dropdown options.
        current_value (str): The current selected value in the dropdown.

    Returns:
        tuple: Updated options list and selected value.
    """
    if upload_contents and upload_filename:
        # Add uploaded file to dropdown
        new_option = {'label': upload_filename, 'value': upload_filename}
        # Avoid duplicates
        if new_option not in options:
            options = options + [new_option]
        return options, upload_filename
    return options, current_value

@app.callback(
    Output('time-col-dropdown', 'options'),
    Output('time-col-dropdown', 'value'),
    Output('value-col-dropdown', 'options'),
    Output('value-col-dropdown', 'value'),
    Input('dropdown-options', 'value'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
)
def update_column_dropdowns(selected_file, upload_contents, upload_filename):
    """
    Update the time and brightness column dropdowns options and values based on the selected file.

    Args:
        selected_file (str): Selected filename or path from the dropdown.
        upload_contents (str): Base64 encoded contents of uploaded file.
        upload_filename (str): Name of the uploaded file.

    Returns:
        tuple: (time_col_options, time_col_value, value_col_options, value_col_value)
    """
    if upload_contents and upload_filename and selected_file == upload_filename:
        df = parse_contents(upload_contents, upload_filename)
    else:
        lc = LightCurve(selected_file)
        df = lc.df

    time_cols = [c for c in df.columns if c.lower() in LightCurve.time_colnames]
    value_cols = [c for c in df.columns if c.lower() in LightCurve.value_colnames]

    time_options = [{'label': c, 'value': c} for c in time_cols] if time_cols else []
    value_options = [{'label': c, 'value': c} for c in value_cols] if value_cols else []

    time_val = time_cols[0] if time_cols else None
    value_val = value_cols[0] if value_cols else None

    return time_options, time_val, value_options, value_val


@app.callback(
    Output('example-graph', 'figure'),
    Output('dd-output-container', 'children'),
    Output('file-label', 'children'),
    Input('dropdown-options', 'value'),
    Input('time-col-dropdown', 'value'),
    Input('value-col-dropdown', 'value'),
    Input('variable-slider', 'value'),
    Input('phase-min', 'value'),
    Input('phase-max', 'value'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    Input('example-graph', 'relayoutData')
)
def update_figure(file, time_col, value_col, order, phase_min, phase_max, upload_contents, upload_filename, relayoutData):
    """
    Update the plot and label based on the selected file, selected columns, slider value, and uploaded file.

    Args:
        file (str): The selected file from the dropdown.
        time_col (str): Selected time column.
        value_col (str): Selected brightness/value column.
        order (int): The polynomial order from the slider.
        phase_min (float): Minimum phase value for fitting.
        phase_max (float): Maximum phase value for fitting.
        upload_contents (str): The base64-encoded contents of the uploaded file.
        upload_filename (str): The name of the uploaded file.
        relayoutData (dict): Plotly relayoutData for preserving zoom/pan.

    Returns:
        tuple: (plotly Figure, fit results Div, file label Div)
    """
    if upload_contents and upload_filename and file == upload_filename:
        df = parse_contents(upload_contents, upload_filename)
        lc = LightCurve.__new__(LightCurve)
        lc.df = df
        file_label = f"Loaded uploaded file: {upload_filename}"
    else:
        lc = LightCurve(file)
        file_label = f"Loaded file: {file}"

    df = lc.df

    if time_col not in df.columns or value_col not in df.columns:
        time_col = next((c for c in df.columns if c.lower() in lc.time_colnames), df.columns[0])
        value_col = next((c for c in df.columns if c.lower() in lc.value_colnames), df.columns[1])

    fig = go.Figure()

    offset = 0
    xaxis_title = f'{time_col} [days]'
    if time_col.lower() == 'mjd':
        offset = min(df[time_col])
        xaxis_title = f'{time_col} - {offset} [days]'

    phase = df[time_col] - offset
    if phase_min is None:
        phase_min = float(np.min(phase))
    if phase_max is None:
        phase_max = float(np.max(phase))
    mask = (phase >= phase_min) & (phase <= phase_max)
    phase_fit = phase[mask]
    value_fit = df[value_col][mask]
    fit_data, coeffs = fitting_function(phase_fit, value_fit, order)

    fig.add_trace(go.Scatter(x=phase, y=df[value_col], mode='markers'))
    fig.add_trace(go.Scatter(x=phase_fit, y=fit_data, mode='lines'))

    fig.update_layout(title='Supernova Lightcurve Fitting',
                      xaxis_title=xaxis_title,
                      yaxis_title=f'{value_col}',
                      showlegend=False)

    if value_col.lower() == 'mag':
        fig.update_yaxes(autorange="reversed")

    if relayoutData is not None:
        x_range = None
        y_range = None
        if 'xaxis.range[0]' in relayoutData and 'xaxis.range[1]' in relayoutData:
            x_range = [relayoutData['xaxis.range[0]'], relayoutData['xaxis.range[1]']]
        if 'yaxis.range[0]' in relayoutData and 'yaxis.range[1]' in relayoutData:
            y_range = [relayoutData['yaxis.range[0]'], relayoutData['yaxis.range[1]']]
        if x_range:
            fig.update_xaxes(range=x_range)
        if y_range:
            fig.update_yaxes(range=y_range)

    coeff_data = [{"Order": i, "Coefficient": f"{c:.4g}"} for i, c in enumerate(coeffs[::-1])]
    coeff_table = html.Div([
        html.H4("Fit Results"),
        dash_table.DataTable(
            columns=[{"name": "Order", "id": "Order"}, {"name": "Coefficient", "id": "Coefficient"}],
            data=coeff_data,
            style_cell={"textAlign": "center", "padding": "5px"},
            style_header={"fontWeight": "bold"},
            style_table={"width": "50%", "margin": "auto"}
        )
    ])
    output_div = html.Div([
        coeff_table
    ])
    return fig, output_div, file_label

@app.callback(
    Output('phase-min', 'value'),
    Output('phase-max', 'value'),
    Input('dropdown-options', 'value'),
    Input('time-col-dropdown', 'value'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_phase_range(file, time_col, upload_contents, upload_filename):
    """
    Set the default values for phase-min and phase-max input boxes based on the selected time column.

    Args:
        file (str): The selected file from the dropdown.
        time_col (str): Selected time column.
        upload_contents (str): Base64 encoded contents of uploaded file.
        upload_filename (str): Name of the uploaded file.

    Returns:
        tuple: (float, float) Minimum and maximum phase values.
    """
    if upload_contents and upload_filename and file == upload_filename:
        df = parse_contents(upload_contents, upload_filename)
    else:
        lc = LightCurve(file)
        df = lc.df

    if time_col not in df.columns:
        time_col = next((c for c in df.columns if c.lower() in LightCurve.time_colnames), df.columns[0])

    offset = 0
    if time_col.lower() == 'mjd':
        offset = min(df[time_col])

    phase = df[time_col] - offset
    return float(np.min(phase)), float(np.max(phase))

def open_browser():
    """
    Open the default web browser to the Dash app URL.

    Returns:
        None
    """
    webbrowser.open_new("http://127.0.0.1:8050/")

def run_plot():
    """
    Start the Dash app and open the browser after a short delay.

    Returns:
        None
    """
    main()
    Timer(1, open_browser).start()
    app.run()

if __name__ == "__main__":
    """
    Entry point for running the Dash app.

    Returns:
        None
    """
    run_plot()