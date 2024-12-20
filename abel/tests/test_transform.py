from __future__ import absolute_import

import os

import numpy as np
from numpy.testing import assert_array_equal

from abel.transform import Transform, get_basis_dir, set_basis_dir


def test_transform():
    N = 5
    IM = np.zeros((N, N))

    assert Transform(IM).transform == 'INVERSE'
    assert Transform(IM, 'inverse').transform == 'INVERSE'
    assert Transform(IM, 'forward').transform == 'FORWARD'


def test_basis_dir():
    """
    Test basic functionality of basis_dir tools.
    """
    # check that default directory is not '' or None and can be created
    basis_dir = get_basis_dir(make=True)
    assert basis_dir, 'basis_dir = {}'.format(repr(basis_dir))

    # check saving to default directory
    path = os.path.join(basis_dir, 'test.npy')
    saved = np.random.randn(10, 10)
    np.save(path, saved)

    # check that default directory can be set to None
    set_basis_dir(None)
    tmp = get_basis_dir()
    assert tmp is None, \
           'basis_dir = {} after set_basis_dir(None)'.format(repr(tmp))

    # check that default directory can be reset to system default
    set_basis_dir('', make=False)
    tmp = get_basis_dir()
    assert tmp == basis_dir, \
           'basis_dir = {} after set_basis_dir("")'.format(repr(tmp))

    # check loading from default directory
    loaded = np.load(path)
    assert_array_equal(loaded, saved, err_msg='Loaded != saved')

    # remove temporary file
    os.remove(path)


if __name__ == "__main__":
    test_transform()
    test_basis_dir()
