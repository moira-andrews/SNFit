import numpy as np
import pandas as pd
import os
import glob

def file_formatting(filepath=None):
    """
    Scans the data directory and builds a dictionary mapping user-friendly labels to file paths.
    Optionally adds an extra file via filepath argument.
    
    Args:
        filepath (str): filepath input of location of file on disk to plot
    """
    data_dir = os.path.join(os.path.dirname(__file__), "data_dir/")
    data_files = glob.glob(os.path.join(data_dir, '*'))
    if filepath is not None:
        if isinstance(filepath, list):
            data_files.extend(filepath)
        else:
            data_files.append(filepath)
    data_files = list(set(data_files))

    file_labels = {
        "11fe": "SN 2011fe",
        "17eaw_b": "SN 2017eaw B-band",
        "17eaw_i": "SN 2017eaw I-band",
        "17eaw_r": "SN 2017eaw R-band",
        "17eaw_u": "SN 2017eaw U-band",
        "17eaw_v": "SN 2017eaw V-band",
    }

    file_dict = {}
    for file in data_files:
        fname = os.path.basename(file).lower()
        label = None
        for key, readable in file_labels.items():
            if key in fname:
                label = readable
                break
        if not label:
            label = fname
        file_dict[label] = file
    return file_dict


class LightCurve:
    """
    Class that loads and formats a supernova lightcurve file into a pandas DataFrame.
    """

    time_colnames = ['phase', 'mjd', 'time', 'date']
    value_colnames = ['l', 'mag', 'luminosity','f','flux']

    def __init__(self, filepath):
        """
        Args:
            filepath (str): the filepath to the data
        """
        self.filepath = filepath
        self.df = self.open_and_format_file(filepath)

    def open_and_format_file(self, file):
        df = pd.read_csv(file)
        if df.shape[-1] == 1:
            df = pd.read_csv(file,header=0,sep='\s+')

        cols = [c.lower() for c in df.columns]
        time_col = next((c for c in cols if c in self.time_colnames), None)
        value_col = next((c for c in cols if c in self.value_colnames), None)

        if time_col and value_col:
            df = df[[df.columns[cols.index(time_col)], df.columns[cols.index(value_col)]]]

        return df


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