import numpy as np
from scipy.special import legendre

print('Test legendre:')

def ang_legendre(c):
    print(f'{c=}')
    C = np.zeros_like(c, dtype=float)
    for n, a in enumerate(c):
        print(f'{n=}: {a} *', legendre(n).c[::2])
        C[n::-2] += a * legendre(n).c[::2]
        # (SciPy's legendre() has backwards order and produces noise in
        #  coefficients that must be zero, so indexing takes care of this)
    print(f'{C=}')
    return C

ang_legendre([1, 0, +2])
