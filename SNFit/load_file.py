import os
import glob
import pandas as pd

def load_dir(filepath=None):
    """
    Scan the data directory and build a dictionary mapping user-friendly labels to file paths.
    Optionally adds an extra file via the filepath argument. Default is the files included in the data_dir directory.

    Args:
        filepath (str, optional): Filepath input of location of file on disk to plot. Defaults to None.

    Returns:
        dict: Dictionary mapping user-friendly labels to file paths.
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

