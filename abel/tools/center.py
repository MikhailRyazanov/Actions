# -*- coding: utf-8 -*-
from __future__ import absolute_import

import numpy as np
from scipy.ndimage import center_of_mass

def find_origin(IM):
    return list(center_of_mass(IM))
