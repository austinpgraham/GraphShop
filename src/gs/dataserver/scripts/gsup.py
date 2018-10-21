#!/usr/bin/env python3
import argparse

from gs.views import base_app


def process_args(args=None):
    parser = argparse.ArgumentParser(description="Arguments to start kernel operations")
    parser.add_argument('-s', '--host', help='Host to run kernel', dest='host')
    parser.add_argument('-p', '--port', help='Port to run kernel', dest='port')
    parser.add_argument('-d', '--debug', help='Turn on debugged kernel', action='store_true')
    args = parser.parse_args()

    host = '0.0.0.0' if args.host is None else args.host
    port = 5052 if args.port is None else args.port
    return host, port, args.debug


def main(args=None):
    host, port, debug = process_args(args)
    base_app.run(host=host, port=port, threaded=True, debug=debug)

if __name__ == '__main__':
    main()
