#!/usr/bin/env python3
from math import sqrt
from random import gauss

import numpy as np


class GraphSVD():

        def __init__(self, M, components):
                self.s = self._base_svd(self._M)

        def _norm(self, v):
                norm = sqrt(sum([x*x for x in v]))
                return [x/norm for x in v]

        def _init_vector(self, length):
                """
                Get initial random vector and normalize
                """
                result = [guass(0, 1) for _ in range(length)]
                return self._norm(result)

        def _base_svd(self, M, epsilon=0.0001):
                rows, columns = M.shape
                current = self._init_vector(columns)
                Minter = np.dot(M.T, M)
                error = 1
                prev = None
                while error > epsilon:
                        prev = current
                        current = np.dot(Minter, current)
                        current = current / self._norm(current)
                        error = 1 - abs(np.dot(current, prev))
                return current
