import os
import glob
from SNFit.lightcurve import LightCurve

def test_nan_lightcurve_object():
    '''
    Make Lightcurve object from the nan_test.txt file in the test directory.
    Should remove the nan rows, leaving a df table of length 12.
    '''
    test_file = os.path.join(os.path.dirname(__file__), "test_files/nan_test.txt")
    lc = LightCurve(test_file)
    assert len(lc.df) == 12

def test_delim_lightcurve_object():
    '''
    Make lightcurve object from the different_delim_test.txt file in test directory.
    DF made should handle the different delimeters and spacing.
    '''
    test_file = os.path.join(os.path.dirname(__file__), "test_files/different_delim_test.txt")
    lc = LightCurve(test_file)
    assert not lc.df.empty #df is made
    assert len(lc.df)==30 #no rows are lost

def test_multicol_with_error():
    """
    Make LightCurve object with multiple_columns_test.txt file in test directory.
    DF should keep all columns, detect all brightness columns,
    and detect error columns for Mag, but not Flux, since flux error is titled dF.
    """
    test_file = os.path.join(os.path.dirname(__file__), "test_files/multiple_columns_test.txt")
    lc = LightCurve(test_file)

    mag_error_col = lc.error_cols.get('Mag')
    flux_error_col = lc.error_cols.get('Flux')

    assert mag_error_col is not None, "Mag should have an error column"
    assert flux_error_col is None, "Flux shoudln't have an error column from dF"

    other_errors = {k: v for k, v in lc.error_cols.items() if k not in ['Mag', 'Flux'] and v is not None}
    assert not other_errors, f"Unexpected error columns detected: {other_errors}"

if __name__=="__main__":
    test_nan_lightcurve_object()
    test_delim_lightcurve_object()
    test_multicol_with_error()