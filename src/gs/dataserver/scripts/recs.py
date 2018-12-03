#!/usr/bin/env python3
import sys
import logging
import argparse

from gs.dataserver.model.review import compute_recommendations


def process_args(args=None):
    pass


def main(args=None):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.info('Beginning recommendation compute...')
    compute_recommendations(components=140)
    logging.info('Done.')


if __name__ == '__main__':
    main(sys.argv)
