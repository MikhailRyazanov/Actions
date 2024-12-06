from warnings import simplefilter
simplefilter('always')

from scipy.optimize import curve_fit

print(curve_fit(lambda x, a: a, [0.0, 1.0], [-1.0, 1.0]))
print(curve_fit(lambda x, a: a + 1, [0.0, 1.0], [-1.0, 1.0]))
print(curve_fit(lambda x, a: a + 1, [0.0, 1.0], [0.0, 2.0]))
print(curve_fit(lambda x, a: a, [0.0, 1.0], [-1.0, 1.0], method='trf'))
