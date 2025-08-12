import pandas as pd

class LightCurve:
    """
    Loads and formats a supernova lightcurve file into a pandas DataFrame for plotting,
    including detection of associated error columns.
    """
    time_colnames = ['phase', 'mjd', 'time', 'date']
    value_colnames = ['l', 'mag', 'luminosity', 'f', 'flux']

    def __init__(self, filepath):
        self.filepath = filepath
        try:
            self.df = self._load_and_format(filepath)
        except Exception:
            self.df = pd.DataFrame()

        self.time_col = self._find_column(self.df.columns, self.time_colnames)
        self.value_col = self._find_column(self.df.columns, self.value_colnames)

        self.error_col = self._find_error_column(self.value_col)
        self.errors = self.df[self.error_col] if self.error_col else None

    def _load_and_format(self, file):
        """
        Load a file and format it to only include the time and value columns.

        Tries standard CSV first, then falls back to regex delimiter parsing.

        Args:
            file (str): Path to the file to open.

        Returns:
            pandas.DataFrame: DataFrame with only the time and value columns.
        """
        try:
            df = pd.read_csv(file)
            if df.shape[1] == 1:
                raise ValueError("Only one column detected, likely wrong delim")
        except Exception:
            try:
                df = pd.read_csv(file, delim_whitespace=True)
                if df.shape[1] == 1:
                    raise ValueError("Only one column detected with whitespace delim")
            except Exception:
                try:
                    df = pd.read_csv(file, sep=r'[,\s;|]+', engine='python')
                except Exception as e:
                    raise RuntimeError(f"Failed to parse file '{file}': {e}")

        cols = [c.lower() for c in df.columns]

        time_col = next((c for c in cols if c in self.time_colnames), df.columns[0])
        value_col = next((c for c in cols if c in self.value_colnames), df.columns[1])

        if time_col and value_col:
            df = df[[df.columns[cols.index(time_col)], df.columns[cols.index(value_col)]]]

        df = df.dropna(subset=[df.columns[0], df.columns[1]])

        return df

    def _find_column(self, columns, target_names):
        cols_lower = [c.lower() for c in columns]
        for target in target_names:
            if target in cols_lower:
                return columns[cols_lower.index(target)]
        return None

    def _find_error_column(self, value_col):
        if value_col is None or self.df.empty:
            return None

        suffixes = ['err', 'error', '_err', '_error']
        prefixes = ['d', 'derr', 'd_err']

        candidates = [value_col + suf for suf in suffixes] + [pre + value_col for pre in prefixes]

        cols_lower = [c.lower() for c in self.df.columns]

        for candidate in candidates:
            cand_lower = candidate.lower()
            if cand_lower in cols_lower:
                return self.df.columns[cols_lower.index(cand_lower)]
        return None