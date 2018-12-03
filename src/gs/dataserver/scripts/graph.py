#!/usr/bin/env python3
# THIS FILE IS IRRELEVANT TO CS 5593
import json

from gs.dataserver.algorithms import ProductGraph

START_ASIN = '048640871X'

def main():
    graph = ProductGraph(START_ASIN)
    json.dump(graph.to_json(), open('graph.json', 'w'))

if __name__ == '__main__':
    main()
