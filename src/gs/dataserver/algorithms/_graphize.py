#!/usr/bin/env python3
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from gs.dataserver.model.product import get_products
from gs.dataserver.model.product import product_exists


_PRODUCT_LIMIT = 30


class _Vertex():

    def __init__(self, pid, cid):
        self.id = "_{}_{}".format(cid, pid)
    
    def to_json(self):
        data = {
            'id': self.id,
            'vis': {
                'left': 0,
                'right': 0,
                'width': 50,
                'height': 50
            },
            'attr': {
                'onclick': "clickedNode(this)"
            }
        }
        return data

class _Edge():

    def __init__(self, source, dest):
        self.source = source
        self.dest = dest
    
    def to_json(self):
        data = {
            'source': self.source,
            'dest': self.dest,
            'vis': {
                'stroke': '#ddd',
                'stroke_width': '2px'
            }
        }
        return data


class ProductGraph():

    def __init__(self, start_asin):
        if not product_exists(start_asin):
            raise ValueError("Product {} does not exist.".format(start_asin))
        self.products = [start_asin]
        self.categories = []
        self.vertices = []
        self.edges = []
        self._breadth_first(start_asin)
    
    def _breadth_first(self, node):
        to_visit = [node]
        while to_visit:
            _next = to_visit.pop()
            product = get_products([_next])[0]
            cats = product.categories[0] if len(product.categories) > 0 else []
            for c in cats:
                if c not in self.categories:
                    self.categories.append(c)
            cat_idx = self.categories.index(cats[0]) if len(cats) > 0 else -1
            p_idx = self.products.index(_next)
            self.vertices.append(_Vertex(p_idx, cat_idx))
            if 'also_bought' in product.related and len(self.products) < _PRODUCT_LIMIT:
                for p in product.related['also_bought']:
                    if p not in self.products and product_exists(p):
                        to_visit.append(p)
                        self.products.append(p)
                        logging.info('Current product count: {}.'.format(len(self.products)))
                        self.edges.append(_Edge(p_idx, self.products.index(p)))

    def to_json(self):
        data = {
            'products': self.products,
            'categories': self.categories,
            'vertices': [v.to_json() for v in self.vertices],
            'edges': [e.to_json() for e in self.edges]
        }
        return data
