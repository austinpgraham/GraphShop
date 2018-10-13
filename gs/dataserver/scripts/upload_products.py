#!/usr/bin/env python3
import os
import sys
import json
import gzip
import logging

from argparse import ArgumentParser

from gs.dataserver.model.product import Product
from gs.dataserver.model.product import add_products


def parse_file(path):
    g = gzip.open(path, 'r')
    for line in g:
        yield eval(line)


def process_args(args=None):
    parser = ArgumentParser()
    parser.add_argument('-f', '--file', help="File containing product data")

    args = parser.parse_args()
    assert args.file is not None, "Must provide file to upload"
    _file = os.path.expanduser(args.file)
    assert os.path.exists(_file), "Input file not found."

    return _file


def main(args=None):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    _file = process_args(args=args)
    items = []
    total = 0
    for item in parse_file(_file):
        p = Product(**item)
        items.append(p)
        if len(items) > 0 and len(items) % 50:
            add_products(items)
            total += 50
            logging.info('{} products uploaded.'.format(total))
    add_products(items)
    logging.info('Done.')


if __name__ == '__main__':
    main(sys.argv)
