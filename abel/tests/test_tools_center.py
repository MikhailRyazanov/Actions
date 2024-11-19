from __future__ import absolute_import

import numpy as np
from numpy.testing import assert_allclose

import abel
from abel.tools.center import find_origin


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
            origin = find_origin(data)
            ref = (row, col)
            tol = 0.1
            assert_allclose(origin, ref, atol=tol, verbose=False,
                            err_msg='-> {} x {}, origin = {} not equal {}'.
                                    format(rows, cols, origin, ref))


if __name__ == "__main__":
    test_find_origin()
