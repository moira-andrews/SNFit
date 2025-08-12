import numpy as np

def fitting_function(time, brightness, order, error=None):
    """
    Fit a polynomial to supernova lightcurve data and compute goodness-of-fit metrics.

    If measurement errors are provided, computes both the reduced chi-squared and R^2 metrics.
    If errors are not provided, computes only the R^2 metric.

    Args:
        time (array-like): Time values (e.g., days since peak or MJD) at which brightness is measured.
        brightness (array-like): Corresponding brightness measurements (e.g., flux, magnitude, or luminosity).
        order (int): Degree of the polynomial to fit.
        error (array-like, optional): Measurement uncertainties for brightness. Used as weights in fitting
            and for chi-squared calculation. Defaults to None.

    Returns:
        tuple:
            fit_data (numpy.ndarray): Polynomial evaluated at input times, representing the fitted brightness.
            coeffs (numpy.ndarray): Polynomial coefficients from highest degree to constant term.
            reduced_chi2 (float or None): Reduced chi-squared statistic indicating goodness-of-fit,
                or None if errors are not provided.
            r_squared (float): Coefficient of determination indicating fraction of variance explained by fit.
    """
    if error is not None:
        weights = 1.0 / np.array(error)
    else:
        weights = None

    coeffs = np.polyfit(time, brightness, order, w=weights)
    p = np.poly1d(coeffs)
    fit_data = p(time)

    ss_res = np.sum((brightness - fit_data) ** 2)
    ss_tot = np.sum((brightness - np.mean(brightness)) ** 2)
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan

    if error is not None:
        residuals = brightness - fit_data
        chi2 = np.sum((residuals / error) ** 2)
        dof = len(time) - (order + 1)
        reduced_chi2 = chi2 / dof if dof > 0 else np.nan
    else:
        reduced_chi2 = None

    return fit_data, coeffs, reduced_chi2, r_squared
