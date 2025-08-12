import os
import glob
import pandas as pd
import base64
import io

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

def load_and_format(filepath=None, contents=None, upload_filename=None, df=None):
    """
    Load or parse data into a pandas DataFrame, handling file paths,
    uploaded base64 contents, or directly passed DataFrames.

    Tries multiple parsing strategies in order until one works.

    Args:
        file (str or file-like, optional): Path to a local file or StringIO.
        contents (str, optional): Base64-encoded uploaded file content.
        upload_filename (str, optional): Name of the uploaded file (for parsing).
        df (pd.DataFrame, optional): DataFrame already loaded.

    Returns:
        pd.DataFrame: Loaded and cleaned DataFrame.

    Raises:
        ValueError: If unsupported file type or invalid input.
        RuntimeError: If file parsing fails.
    """

    if df is not None:
        return df.dropna()

    if contents is not None and upload_filename is not None:
        content_type, content_string = contents.split(',')
        decoded_bytes = base64.b64decode(content_string)
        decoded_str = decoded_bytes.decode('utf-8')
        file_like = io.StringIO(decoded_str)
    elif filepath is not None:
        file_like = filepath
    else:
        raise ValueError("Must provide either 'filepath', or 'contents' and 'upload_filename', or 'df'.")

    parse_attempts = [
        lambda f: pd.read_csv(f),
        lambda f: pd.read_csv(f, sep=r'\s+'),
        lambda f: pd.read_csv(f, sep=r'[,\s;|]+', engine='python'),
    ]

    for parse_func in parse_attempts:
        try:
            if hasattr(file_like, 'seek'):
                file_like.seek(0)
            df = parse_func(file_like)
            if df.shape[1] == 1:
                continue
            return df.dropna()
        except Exception:
            continue

    raise RuntimeError(f"Failed to parse data with provided inputs.")