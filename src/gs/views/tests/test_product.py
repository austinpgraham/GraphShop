#!/usr/bin/env python3
from gs.views.tests import WebTest

from gs.views.product import *


class TestProducts(WebTest):

    def test_product_get(self):
        result = self.app.get('/products/123')
        from pdb import set_trace; set_trace()