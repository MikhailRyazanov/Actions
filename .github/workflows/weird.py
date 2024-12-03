import numpy as np
from numpy.testing import assert_allclose
import scipy
from scipy.special import legendre
from scipy.optimize import curve_fit

print(f'NumPy {np.version.full_version}, SciPy {scipy.version.full_version}')

print('\nTest legendre:')
np.set_printoptions(formatter={'float': lambda x: f'{x:.18g}'})
print(legendre(2).c)

print('\nTest optimize:')
r'''
GitHub:

macos-13, 3.7:
tests/test_tools_vmi.py::test_anisotropy_parameter
  /Users/runner/hostedtoolcache/Python/3.7.17/x64/lib/python3.7/site-packages/scipy/optimize/minpack.py:834: OptimizeWarning: Covariance of the parameters could not be estimated
    category=OptimizeWarning)

macos-latest, 3.13:
tests/test_tools_center.py::test_find_origin
tests/test_tools_center.py::test_set_center_float
  /Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/abel/tools/math.py:142: OptimizeWarning: Covariance of the parameters could not be estimated
    res = curve_fit(gaussian, np.arange(x.size), x, p0=guess_gaussian(x))

tests/test_tools_vmi.py::test_anisotropy_parameter
  /Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/abel/tools/vmi.py:397: OptimizeWarning: Covariance of the parameters could not be estimated
    popt, pcov = curve_fit(PAD, theta, intensity)


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
def anisotropy_parameter(theta, intensity, theta_ranges=None):
    def P2(x):  # 2nd-order Legendre polynomial
        return (3 * x * x - 1) / 2

    def PAD(theta, beta, amplitude):
        return amplitude * (1 + beta * P2(np.cos(theta)))  # Eq. (1) as above

    # angular range of data to be included in the fit
    if theta_ranges is not None:
        subtheta = np.ones(len(theta), dtype=bool)
        for rt in theta_ranges:
            subtheta = np.logical_and(
                subtheta, np.logical_and(theta >= rt[0], theta <= rt[1]))
        theta = theta[subtheta]
        intensity = intensity[subtheta]

    # fit angular intensity distribution
    try:
        popt, pcov = curve_fit(PAD, theta, intensity)
        beta, amplitude = popt
        error_beta, error_amplitude = np.sqrt(np.diag(pcov))
        # physical range
        if beta > 2 or beta < -1:
            beta, error_beta = np.nan, np.nan
    except:
        beta, error_beta = np.nan, np.nan
        amplitude, error_amplitude = np.nan, np.nan

    return (beta, error_beta), (amplitude, error_amplitude)


n = 100
theta = np.linspace(-np.pi, np.pi, n, endpoint=False)

ones = np.ones_like(theta)
cos2 = np.cos(theta)**2
sin2 = np.sin(theta)**2

def check(name, ref, theta, intensity):
    print(name)
    beta, amplitude = anisotropy_parameter(theta, intensity)
    assert_allclose((beta[0], amplitude[0]), ref, atol=1e-8,
                    err_msg='-> ' + name)

check('ones', (0, 1), theta, ones)
check('cos2', (2, 1/3), theta, cos2)
check('sin2', (-1, 2/3), theta, sin2)
check('cos2sin2', (0, 1/8), theta, cos2 * sin2)
