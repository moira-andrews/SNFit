import pandas as pd

class LightCurve:
    """
    Loads and formats a supernova lightcurve file into a pandas DataFrame for plotting.
    """
    time_colnames = ['phase', 'mjd', 'time', 'date']
    value_colnames = ['l', 'mag', 'luminosity','f','flux']

    def __init__(self, filepath):
        """
        Initialize the LightCurve object, loading and formatting the data.

        Args:
            filepath (str): The filepath to the data.
        """
        self.filepath = filepath
        try:
            self.df = self._load_and_format(filepath)
        except Exception as e:
            self.df = pd.DataFrame()

    def _load_and_format(self, file):
        """
        Load a file and format it to only include the time and value columns.

        Args:
            file (str): Path to the file to open.

        Returns:
            pandas.DataFrame: DataFrame with only the time and value columns.
        """
        delimiters = [',', '\t', ';', '|', ' ']
        errors = []

        for delim in delimiters:
            try:
                df = pd.read_csv(file, sep=delim)
                if df.shape[1] > 1:
                    break
            except (pd.errors.ParserError, pd.errors.EmptyDataError, UnicodeDecodeError) as e:
                errors.append(f"Delimiter '{delim}': {e}")
                continue
        else:
            try:
                df = pd.read_csv(file, sep='\s+', engine='python')
            except Exception as e:
                errors.append(f"Fallback with whitespace failed: {e}")
                raise RuntimeError(
                    f"Failed to parse file '{file}' with any delimiter. Errors:\n" +
                    "\n".join(errors)
                ) from e

        cols = [c.lower() for c in df.columns]

        time_col = next((c for c in cols if c in self.time_colnames), df.columns[0])
        value_col = next((c for c in cols if c in self.value_colnames), df.columns[1])

        if time_col and value_col:
            df = df[[df.columns[cols.index(time_col)], df.columns[cols.index(value_col)]]]

        df = df.dropna(subset=[df.columns[0], df.columns[1]])

        return df
