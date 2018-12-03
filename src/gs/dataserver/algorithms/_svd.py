#!/usr/bin/env python3
from math import sqrt
from random import gauss

import numpy as np


class GraphSVD():
        """
        Implement an object that performs and
        return the SVD recommendation model.
        """

        def __init__(self, M, components, epsilon=0.0001):
                # Compute the matrices for SVD
                self.s, self.u, self.v = self._rank_svd(M, components=components, epsilon=epsilon)
                # Estimate the matrices and attach to predictions attributes
                self.predictions = np.dot(np.matmul(self.u,np.diag(self.s)), self.v)

        def _norm(self, v):
                """
                Normalize a vector
                """
                norm = sqrt(sum([x*x for x in v]))
                return [x/norm for x in v], norm

        def _init_vector(self, length):
                """
                Get initial random vector and normalize
                """
                result = [gauss(0, 1) for _ in range(length)] 
                return self._norm(result)[0]

        def _base_svd(self, M, epsilon=0.0001):
                """
                Perform a 1D SVD
                """
                rows, columns = M.shape
                # Get a random vector
                current = self._init_vector(columns)
                Minter = np.dot(M.T, M)
                error = 1
                prev = None
                # Optimize the vector until the
                # dot product is close to one
                while error > epsilon:
                        prev = current
                        current = self._norm(np.dot(Minter, current))[0]
                        error = 1 - abs(np.dot(current, prev))
                return current

        def _rank_svd(self, M, epsilon=0.0001, components=3):
                """
                Perform SVD for all singular values.
                """
                M = np.array(M, dtype='float64')
                rows, columns = M.shape
                prev = []
                if components > columns: # pragma: no cover
                        raise ValueError("Cannot have more components than columns in matrix.")
                # 1D SVD for each singular value
                for i in range(components):
                        remove = M.copy()
                        # Remove previously computed values
                        for s, u, v in prev[:i]:
                                remove -= s*np.outer(u, v)
                        # Get new value and normalize
                        new_val = self._base_svd(remove, epsilon=epsilon)
                        u, s = self._norm(np.dot(M, new_val))
                        prev.append((s, u, new_val))
                # Get the pieces of SVD out of the resulting vectors
                s, u, v = [np.array(x) for x in zip(*prev)]
                return s, u.T, v
