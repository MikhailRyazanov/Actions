import numpy as np
import scipy
from scipy.special import legendre

print(f'NumPy {np.version.full_version}, SciPy {scipy.version.full_version}')

print('\nTest legendre:')

np.set_printoptions(formatter={'float': lambda x: f'{x:.18g}'})

def ang_legendre(c):
    print(f'{c=}')
    C = np.zeros_like(c, dtype=float)
    for n, a in enumerate(c):
        print(f'{n=}: {a} *', legendre(n).c[::2])
        C[n::-2] += a * legendre(n).c[::2]
        print(f'  l({n}).c = {legendre(n).c}')
    print(f'{C=}')
    return C

ang_legendre([1, 0, +2])
