#!/usr/bin/env python3
from math import sqrt
from random import gauss

import numpy as np


class GraphSVD():

        def __init__(self, M, components, epsilon=0.0001):
                self.s, self.u, self.v = self._rank_svd(M, components=components, epsilon=epsilon)
                self.predictions = np.dot(np.matmul(self.u,np.diag(self.s)), self.v)

        def _norm(self, v):
                norm = sqrt(sum([x*x for x in v]))
                return [x/norm for x in v], norm

        def _init_vector(self, length):
                """
                Get initial random vector and normalize
                """
                result = [gauss(0, 1) for _ in range(length)] 
                return self._norm(result)[0]

        def _base_svd(self, M, epsilon=0.0001):
                rows, columns = M.shape
                current = self._init_vector(columns)
                Minter = np.dot(M.T, M)
                error = 1
                prev = None
                while error > epsilon:
                        prev = current
                        current = self._norm(np.dot(Minter, current))[0]
                        error = 1 - abs(np.dot(current, prev))
                return current

        def _rank_svd(self, M, epsilon=0.0001, components=3):
                M = np.array(M, dtype='float64')
                rows, columns = M.shape
                prev = []
                if components > columns: # pragma: no cover
                        raise ValueError("Cannot have more components than columns in matrix.")
                for i in range(components):
                        remove = M.copy()
                        for s, u, v in prev[:i]:
                                remove -= s*np.outer(u, v)
                        new_val = self._base_svd(remove, epsilon=epsilon)
                        u, s = self._norm(np.dot(M, new_val))
                        prev.append((s, u, new_val))

                s, u, v = [np.array(x) for x in zip(*prev)]
                return s, u.T, v
