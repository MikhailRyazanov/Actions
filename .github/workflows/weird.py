import numpy as np
np.set_printoptions(formatter={'float': lambda x: f'{x:.18g}'})
from scipy.special import legendre
print(legendre(2).c)
