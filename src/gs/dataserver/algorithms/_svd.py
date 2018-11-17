#!/usr/bin/env python3
import numpy as np

def svd(M, error=None):
    M = np.array(M, dtype=float)
    m, n = M.shape
    if error is None:
        error = 1e-6
    
