from scipy.optimize import curve_fit

# pytest warning
def test_optimize_warning():
    curve_fit(lambda x, a: a, [0.0, 1.0], [-1.0, 1.0])

# pytest error
#def test_error():
#    not

# pytest failure
#def test_fail():
#    assert 0 != 0

# pytest skipped
#import pytest
#@pytest.mark.skip()
#def test_skip():
#    pass

if __name__ == "__main__":
    test_optimize_warning()
