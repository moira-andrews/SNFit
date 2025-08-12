import pandas as pd
from SNFit.load_file import load_and_format

class LightCurve:
    """
    Loads and formats a supernova lightcurve file into a pandas DataFrame for plotting,
    including detection of associated error columns for multiple brightness columns.
    """
    time_colnames = ['phase', 'mjd', 'time', 'date']
    value_colnames = ['l', 'mag', 'luminosity', 'f', 'flux']

    def __init__(self, filepath, upload_df=None):
        self.filepath = filepath
        
        if upload_df is not None:
            self.df = upload_df
        else:
            try:
                self.df = load_and_format(filepath=filepath)
            except Exception as e:
                print(e)
                self.df = pd.DataFrame()

        self.time_col = self._find_column(self.df.columns, self.time_colnames)
        self.value_cols = self._find_all_columns(self.df.columns, self.value_colnames)

        self.error_cols = {
            val_col: self._find_error_column(val_col)
            for val_col in self.value_cols
        }

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
        
        if value_col is None or self.df.empty:
            return None

        value_lower = value_col.lower()
        abbreviations = {
            'flux': ['f'],
            'magnitude': ['mag'],
            'mag': [],
            'luminosity': ['l']
        }

        suffixes = ['err', 'error', '_err', '_error']
        prefixes = ['d', 'derr', 'd_err']

        cols_lower = [c.lower() for c in self.df.columns]
        cols_original = list(self.df.columns)

        def find_col(name_lower):
            if name_lower in cols_lower:
                return cols_original[cols_lower.index(name_lower)]
            return None

        for suf in suffixes:
            col = find_col(value_lower + suf)
            if col:
                return col

        for pre in prefixes:
            col = find_col(pre + value_lower)
            if col:
                return col

        for abbr in abbreviations.get(value_lower, []):
            for pre in prefixes:
                col = find_col(pre + abbr)
                if col:
                    return col

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
