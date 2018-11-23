#!/usr/bin/env python3
import numpy as np

from hamcrest import is_
from hamcrest import assert_that

from gs.dataserver.algorithms.tests import AlgorithmsTest

from gs.dataserver.algorithms import GraphSVD


class TestAlgorithms(AlgorithmsTest):

    def test_svd(self):
        test_matrix = np.array(
            [
                [5, 3, 4],
                [6, 8, 7],
                [1, 4, 6]
            ]
        )

        svd = GraphSVD(test_matrix, 3, epsilon=1e-6)
        assert_that(np.allclose(svd.predictions, test_matrix), is_(True))


