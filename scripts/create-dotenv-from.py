#!/usr/bin/env python3

import os
import sys
from io import StringIO


def main(in_file):
    out = StringIO()
    for line in open(in_file, 'rt'):
        if 'BOGUS' in line:
            env_var = line.split('=')[0].replace('export ', '').strip()
            env_value = os.getenv(env_var)
            if not env_value:
                raise RuntimeError(f'{env_var} is blank')
            line = line.replace('BOGUS', env_value)

        out.write(line)

    sys.stdout.write(out.getvalue())


if __name__ == '__main__':
    main(in_file=sys.argv[1])
