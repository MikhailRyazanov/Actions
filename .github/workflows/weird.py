from warnings import simplefilter
simplefilter('always')

from warnings import simplefilter
simplefilter('always')

import itertools

import numpy as np
from numpy.testing import assert_equal, assert_allclose
import scipy
from scipy.ndimage import shift
from scipy.optimize import curve_fit, brentq
from scipy.interpolate import interp1d

print(f'NumPy {np.version.full_version}, SciPy {scipy.version.full_version}')

print('\nTest optimize:')
r'''
GitHub:
macos-latest, 3.13:
tests/test_tools_center.py::test_find_origin
tests/test_tools_center.py::test_set_center_float
  /Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/abel/tools/math.py:142: OptimizeWarning: Covariance of the parameters could not be estimated
    res = curve_fit(gaussian, np.arange(x.size), x, p0=guess_gaussian(x))

Travis:
jammy, 3.8:
tests/test_tools_center.py::test_set_center_float
  /home/travis/virtualenv/python3.8.18/lib/python3.8/site-packages/scipy/optimize/_minpack_py.py:906: OptimizeWarning: Covariance of the parameters could not be estimated
    warnings.warn('Covariance of the parameters could not be estimated',

AppVeyor:
2.7, 32:
tests/test_tools_center.py::test_find_origin
  c:\miniconda\envs\abel-env\lib\site-packages\scipy\optimize\minpack.py:787: OptimizeWarning: Covariance of the parameters could not be estimated
    category=OptimizeWarning)
'''
def find_origin(IM, method='image_center', axes=(0, 1), verbose=False,
                **kwargs):
    return func_method[method](IM, axes, verbose=verbose, **kwargs)


def gaussian(x, a, mu, sigma, c):
    return a * np.exp(-((x - mu) ** 2) / 2 / sigma ** 2) + c


def guess_gaussian(x):
    c_guess = (x[0] + x[-1]) / 2
    a_guess = x.max() - c_guess
    mu_guess = x.argmax()
    x_inter = interp1d(range(len(x)), x)

    def _(i):
        return x_inter(i) - a_guess / 2 - c_guess

    try:
        sigma_l_guess = brentq(_, 0, mu_guess)
    except ValueError:
        sigma_l_guess = len(x) / 4
    try:
        sigma_r_guess = brentq(_, mu_guess, len(x) - 1)
    except ValueError:
        sigma_r_guess = 3 * len(x) / 4
    return a_guess, mu_guess, (sigma_r_guess -
                               sigma_l_guess) / 2.35482, c_guess


def fit_gaussian(x):
    res = curve_fit(gaussian, np.arange(x.size), x, p0=guess_gaussian(x))
    return res[0]  # extract optimal values


def find_origin_by_gaussian_fit(IM, axes=(0, 1), verbose=False,
                                round_output=False, **kwargs):
    if isinstance(axes, int):
        axes = [axes]

    origin = [IM.shape[0] // 2, IM.shape[1] // 2]
    for a in axes:
        # sum along the other axis
        proj = np.sum(IM, axis=1 - a)
        # find gaussian center
        origin[a] = fit_gaussian(proj)[1]
    origin = tuple(origin)

    if verbose:
        to_print = "Gaussian origin at {}".format(origin)

    if round_output:
        origin = (round(origin[0]), round(origin[1]))
        if verbose:
            to_print += " ... round to {}".format(origin)

    if verbose:
        print(to_print)

    return origin


func_method = {
    "gaussian": find_origin_by_gaussian_fit,
    #"slice": find_origin_by_slice
}

######################################################################

def test_find_origin():
    """
    Test find_origin methods.
    """
    size = [12, 13]
    row, col = 5.4, 6.6  # origin
    w = 3.0  # gaussian width parameter (sqrt(2) * sigma)
    for rows in size:
        y2 = ((np.arange(rows) - row) / w)**2
        for cols in size:
            x2 = ((np.arange(cols) - col) / w)**2
            data = np.exp(-(x2 + y2[:, None]))
            axes = (1, 0)
            # (not testing trivial 'image_center', which does not find origin)
            for method in ['gaussian']:#, 'slice']:
                print(f'{rows = }, {cols = }, {method = }:')
                origin = find_origin(data, method, axes)
                ref = (row if 0 in axes else rows // 2,
                       col if 1 in axes else cols // 2)
                tol = 0.2  # 'convolution' rounds to 0.5 pixels
                assert_allclose(origin, ref, atol=tol, verbose=False,
                                err_msg='-> {} x {}, method = {}, axes = {}: '
                                        'origin = {} not equal {}'.
                                        format(rows, cols, method, axes,
                                               origin, ref))

'''
def test_set_center_float():
    """
    Test fractional shifts.
    """
    # input sizes
    size = [10, 11]
    # default origin coordinate (substituting None)
    default = 5.0
    # input size, origin, crop -> output size, non-zero range
    param = {10: [(None, {'maintain_size': [10, (0, 10)],
                          'valid_region':  [10, (0, 10)],
                          'maintain_data': [10, (0, 10)]}),
                  (2.5,  {'maintain_size': [10, (2, 10)],
                          'valid_region':  [5,  (0,  5)],
                          'maintain_data': [15, (4, 15)]}),
                  (3.5,  {'maintain_size': [10, (1, 10)],
                          'valid_region':  [7,  (0,  7)],
                          'maintain_data': [13, (2, 13)]}),
                  (4.5,  {'maintain_size': [10, (0, 10)],
                          'valid_region':  [9,  (0,  9)],
                          'maintain_data': [11, (0, 11)]}),
                  (5.5,  {'maintain_size': [10, (0, 10)],
                          'valid_region':  [7,  (0,  7)],
                          'maintain_data': [13, (0, 11)]}),
                  (6.5,  {'maintain_size': [10, (0,  9)],
                          'valid_region':  [5,  (0,  5)],
                          'maintain_data': [15, (0, 11)]})],
             11: [(None, {'maintain_size': [11, (0, 11)],
                          'valid_region':  [11, (0, 11)],
                          'maintain_data': [11, (0, 11)]}),
                  (3.5,  {'maintain_size': [11, (1, 11)],
                          'valid_region':  [7,  (0,  7)],
                          'maintain_data': [15, (3, 15)]}),
                  (4.5,  {'maintain_size': [11, (0, 11)],
                          'valid_region':  [9,  (0,  9)],
                          'maintain_data': [13, (1, 13)]}),
                  (5.5,  {'maintain_size': [11, (0, 11)],
                          'valid_region':  [9,  (0,  9)],
                          'maintain_data': [13, (0, 12)]}),
                  (6.5,  {'maintain_size': [11, (0, 10)],
                          'valid_region':  [7,  (0,  7)],
                          'maintain_data': [15, (0, 12)]})]}
    w = 2.0  # gaussian width parameter (sqrt(2) * sigma)
    # all size combinations
    for rows, cols in itertools.product(size, repeat=2):
        # all origin "rows"
        for row, rparam in param[rows]:
            y2 = ((np.arange(rows) - (row or default)) / w)**2
            # all origin "columns"
            for col, cparam in param[cols]:
                x2 = ((np.arange(cols) - (col or default)) / w)**2
                # test data: gaussian centered at (row, col)
                data = np.exp(-(x2 + y2[:, None]))
                # all crop options
                for crop in ['maintain_size', 'valid_region', 'maintain_data']:
                    # check set_center() result
                    result = set_center(data, (row, col), crop=crop)
                    refrows, rrange = rparam[crop]
                    refcols, crange = cparam[crop]
                    refshape = (refrows, refcols)
                    refrange = (slice(*rrange), slice(*crange))
                    reforigin = (refrows // 2 if row else default,
                                 refcols // 2 if col else default)
                    msg = '-> {} x {}, origin = {}, crop = {}: '.\
                          format(rows, cols, (row, col), crop)
                    # shape
                    assert_equal(result.shape, refshape, verbose=False,
                                 err_msg=msg + 'shape {} not equal {}'.
                                               format(result.shape, refshape))
                    # non-zero data
                    assert_equal(result[refrange] != 0, True,
                                 err_msg=msg + 'zeros in non-zero range')
                    # zero padding
                    tmp = result.copy()
                    tmp[refrange] = 0
                    assert_equal(tmp, 0, err_msg=msg +
                                 'non-zeros outside non-zero range')
                    # gaussian center
                    origin = find_origin(result, 'gaussian')
                    assert_allclose(origin, reforigin, atol=0.01,
                                    verbose=False, err_msg=msg +
                                    'shifted center {} not equal {}'.
                                    format(origin, reforigin))
'''


test_find_origin()
#test_set_center_float()
