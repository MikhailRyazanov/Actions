from warnings import simplefilter
simplefilter('always')

import numpy as np
from numpy.testing import assert_allclose
import scipy
from scipy.optimize import curve_fit

print(f'NumPy {np.version.full_version}, SciPy {scipy.version.full_version}')

print('\nTest optimize:')
np.set_printoptions(formatter=None)
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
