#!/usr/bin/env python3
import os
import sys
import json
import gzip
import logging

from argparse import ArgumentParser

from gs.dataserver.model.product import Product
from gs.dataserver.model.product import product_exists

from gs.dataserver.model.review import Review
from gs.dataserver.model.review import add_reviews
from gs.dataserver.model.review import review_exists

from gs.dataserver.model.user import ReviewUser
from gs.dataserver.model.user import user_exists
from gs.dataserver.model.user import add_reviewusers


def parse_file(path):
    g = gzip.open(path, 'r')
    for line in g:
        yield eval(line)


def process_args(args=None):
    parser = ArgumentParser()
    parser.add_argument('-f', '--file', help="File containing review data")

    args = parser.parse_args()
    assert args.file is not None, "Must provide file to upload"
    _file = os.path.expanduser(args.file)
    assert os.path.exists(_file), "Input file not found."

    return _file


def main(args=None):
    """
    Upload review objects from a file
    """
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    _file = process_args(args=args)
    items = []
    total = 0
    # For every item 
    for item in parse_file(_file):
        for key, value in item.items():
            item[key] = str(value)
        # Create from dictionary
        r = Review(**item)
        # If the user doesn't exist, add it
        if not user_exists(r.reviewerID):
            u = ReviewUser(id=r.reviewerID, name=getattr(r, "reviewerName", ""))
            add_reviewusers([u])
            logging.info("User {} added.".format(u.name))
        # If the review doesn't exist, add it
        if not review_exists(r.reviewerID, r.asin) and product_exists(r.asin):
            items.append(r)
        # Upload cached reviews
        if len(items) > 0 and len(items) % 50 == 0:
            add_reviews(items)
            total += 50
            logging.info("{} reviews uploaded.".format(total))
            items = []
    # Upload the rest of the products
    add_reviews(items)
    logging.info("Done.")

if __name__ == '__main__':
    main(sys.argv)
