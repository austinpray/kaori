#!/usr/bin/env python

from argparse import ArgumentParser
import json

if __name__ == "__main__":
    parser = ArgumentParser(description='Generates a dev info file')

    parser.add_argument('--revision', dest='revision', help='git revision', required=True)

    args = parser.parse_args()

    info = {'revision': args.revision}
    print(json.dumps(info, sort_keys=True, indent=4))
