import os.path

import numpy as np
from numpy.testing import assert_array_equal


DATA_DIR = os.path.join(os.path.split(__file__)[0], 'data')


def test_datadir():
    path = os.path.join(DATA_DIR , 'test.npy')

    saved = np.random.randn(10, 10)
    np.save(path, saved)

    loaded = np.load(path)
    assert_array_equal(loaded, saved, err_msg='Loaded != saved')

    os.remove(path)


if __name__ == '__main__':
    test_datadir()
