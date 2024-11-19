#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

class Transform(object):
    def __init__(self, IM, direction='inverse'):
        self.IM = IM
        self.direction = direction

        self.transform = direction.upper()
