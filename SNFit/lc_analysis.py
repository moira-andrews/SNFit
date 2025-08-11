import numpy as np

def fitting_function(time, L, order):
    """
    Fit supernova lightcurves using a polynomial of up to 20th degree.

    Args:
        time (array-like): Days of observation, usually as mean Julian dates. Units can be days or phase with respect to the time of peak brightness.
        L (array-like): Bolometric magnitudes in mag or ergs per second.
        order (int): Degree of the fitting polynomial.

    Returns:
        tuple: (fitted values as numpy.ndarray, coefficients as numpy.ndarray)
    """
    coeffs = np.polyfit(time, L, order)
    p = np.poly1d(coeffs)
    fit_data = p(time)
    return fit_data, coeffs
