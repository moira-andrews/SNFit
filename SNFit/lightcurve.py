import pandas as pd

class LightCurve:
    """
    Loads and formats a supernova lightcurve file into a pandas DataFrame for plotting,
    including detection of associated error columns for multiple brightness columns.
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
        self.value_cols = self._find_all_columns(self.df.columns, self.value_colnames)

        self.error_cols = {
            val_col: self._find_error_column(val_col)
            for val_col in self.value_cols
        }

    def _load_and_format(self, file):
        """
        Load the full file with all columns intact.

        Args:
            file (str): Path to the file.

        Returns:
            pd.DataFrame: Loaded DataFrame.
        """
        try:
            df = pd.read_csv(file)
            if df.shape[1] == 1:
                raise ValueError("Only one column detected, likely wrong delim")
        except Exception:
            try:
                df = pd.read_csv(file, sep='\s+')
                if df.shape[1] == 1:
                    raise ValueError("Only one column detected with whitespace delim")
            except Exception:
                try:
                    df = pd.read_csv(file, sep=r'[,\s;|]+', engine='python')
                except Exception as e:
                    raise RuntimeError(f"Failed to parse file '{file}': {e}")

        return df.dropna()

    def _find_column(self, columns, target_names):
        cols_lower = [c.lower() for c in columns]
        for target in target_names:
            if target in cols_lower:
                return columns[cols_lower.index(target)]
        return None

    def _find_all_columns(self, columns, target_names):
        cols_lower = [c.lower() for c in columns]
        found = []
        for target in target_names:
            found += [columns[i] for i, c in enumerate(cols_lower) if c == target]
        return found

    def _find_error_column(self, value_col):
        """
        Find an error column related to a given brightness column by checking common
        suffixes and prefixes.

        Args:
            value_col (str): Name of the brightness column.

        Returns:
            str or None: Corresponding error column name or None if not found.
        """
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

    def get_error_column(self, brightness_col):
        """
        Public method to get the error column corresponding to a brightness column.

        Args:
            brightness_col (str): Name of brightness column.

        Returns:
            str or None: Name of error column or None if not found.
        """
        return self.error_cols.get(brightness_col, None)
