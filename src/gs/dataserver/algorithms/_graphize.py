#!/usr/bin/env python3
# THIS FILE IRRELEVANT TO CS 5593
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
import operator

from gs.dataserver.model.product import get_products
from gs.dataserver.model.product import product_exists


_PRODUCT_LIMIT = 200

class _Edge():

    def __init__(self, source, dest):
        self.source = source
        self.dest = dest
    
    def to_json(self):
        data = {
            'source': self.source,
            'dest': self.dest,
        }
        return data


class ProductGraph():

    def __init__(self, start_asin):
        if not product_exists(start_asin):
            raise ValueError("Product {} does not exist.".format(start_asin))
        self.products = [start_asin]
        self.categories = []
        self.edges = {}
        self._breadth_first(start_asin)
    
    def _breadth_first(self, node):
        to_visit = [node]
        all_cats = {}
        while to_visit:
            _next = to_visit.pop()
            product = get_products([_next])[0]
            cats = product.categories[0] if len(product.categories) > 0 else []
            for c in cats:
                if c not in self.categories:
                    self.categories.append(c)
                    all_cats[c] = []
                    self.edges[c] = []
            cat_idx = self.categories.index(cats[0]) if len(cats) > 0 else -1
            p_idx = self.products.index(_next)
            if len(cats)  > 0:
                all_cats[self.categories[cat_idx]].append((cat_idx, p_idx))
            else:
                continue
            if 'also_bought' in product.related and len(self.products) < _PRODUCT_LIMIT:
                count = 0
                for p in product.related['also_bought']:
                    if p not in self.products and product_exists(p):
                        if count > 5:
                            break
                        to_visit.append(p)
                        self.products.append(p)
                        logging.info('Current product count: {}.'.format(len(self.products)))
                        self.edges[self.categories[cat_idx]].append(_Edge(p_idx, self.products.index(p)).to_json())
                        count += 1
        self.cats = all_cats

    def to_json(self):
        product_id_list = [sorted(value) for _, value in self.cats.items()]
        data = {
            'products': [["_{}_{}".format(t[0], t[1]) for t in v] for v in product_id_list],
            'categories': [key for key, _ in self.cats.items()],
            'edges': [value for _, value in self.edges.items()],
            'asins': self.products
        }
        return data
