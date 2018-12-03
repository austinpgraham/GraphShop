#!/usr/bin/env python3
import sys
import logging
import argparse

from gs.dataserver.model.product import get_all_ids
from gs.dataserver.model.product import get_products
from gs.dataserver.model.product import update_product
from gs.dataserver.model.product import product_exists


def process_args(args=None):
    pass


def main(args=None):
    """
    Perform filtering of products in the also_bought attribute of a
    product if it does not exist in the database.
    """
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.info('Getting list of product ids...')
    # Get all product IDs
    asins = get_all_ids()
    logging.info('Got {} products!'.format(len(asins)))
    product_count = len(asins)
    process_count = 0
    logging.info('Beginning filter...')
    for _id in asins:
        # Get the product object
        prods = get_products([_id])
        if len(prods) == 1:
            p = prods.pop()
            # Get all related values
            for key, value in p.related.items():
                to_remove = []
                for v in value:
                    # If the product doesn't exist, 
                    # mark to remove
                    if not product_exists(v):
                        to_remove.append(v)
                # Perform the final filtering
                p.related[key] = [x for x in value if x not in to_remove]
            # Update the product object
            update_product(_id, 'related', p.related)
        process_count += 1
        logging.info("{} of {} products processed.".format(process_count, product_count))
    logging.info('Done.')


if __name__ == '__main__':
    main(sys.argv)
