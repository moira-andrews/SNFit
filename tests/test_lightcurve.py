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

if __name__=="__main__":
    test_nan_lightcurve_object()
    test_delim_lightcurve_object()