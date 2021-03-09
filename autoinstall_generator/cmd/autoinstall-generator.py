#!/usr/bin/env python3

from autoinstall_generator.merging import convert_file

from argparse import ArgumentParser, FileType
import sys


helptext = {
    'inpath': 'Debian install preseed file, or a dash to read stdin',
    'outfile': 'Subiquity autoinstall yaml',
    'debug': 'include commented out debug output explaining the conversions'
              + ' performed',
    'cloud': 'output in cloud-config format',
}


def add(parser, name, *args, **kwargs):
    if len(args) > 0:
        parser.add_argument(*args, help=helptext[name], **kwargs)
    else:
        parser.add_argument(name, help=helptext[name], **kwargs)


def main():
    parser = ArgumentParser()
    add(parser, 'inpath', metavar='infile')
    add(parser, 'outfile', nargs='?', type=FileType('w'), default=sys.stdout)
    add(parser, 'debug', '-d', '--debug', action='store_true')
    add(parser, 'cloud', '-c', '--cloud', action='store_true')
    args = parser.parse_args()

    infile = None

    if args.inpath == "-":
        infile_needs_close = False
        infile = sys.stdin
    else:
        infile_needs_close = True
        infile = open(args.inpath, 'r')

    out = convert_file(infile, args)
    args.outfile.write(out)
    if infile_needs_close and infile:
        infile.close()

    sys.exit(0)


if __name__ == '__main__':
    main()
