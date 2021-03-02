#!/usr/bin/env python3

from autoinstall_generator.merging import convert_file
# from .merging import convert_file

import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    # input - d-i preseed
    parser.add_argument("inpath")
    # output - subiquity autoinstall
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout)
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    infile = None

    if args.inpath == "-":
        infile_needs_close = False
        infile = sys.stdin
    else:
        infile_needs_close = True
        infile = open(args.inpath, 'r')

    out = convert_file(infile, args.debug)
    args.outfile.write(out)
    if infile_needs_close and infile:
        infile.close()

    sys.exit(0)


if __name__ == '__main__':
    main()
