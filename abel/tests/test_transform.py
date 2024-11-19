from __future__ import absolute_import

import numpy as np

from abel.transform import Transform

def test_transform():
    N = 5
    IM = np.zeros((N, N))

    assert Transform(IM).transform == 'INVERSE'
    assert Transform(IM, 'inverse').transform == 'INVERSE'
    assert Transform(IM, 'forward').transform == 'FORWARD'


if __name__ == "__main__":
    test_transform()
