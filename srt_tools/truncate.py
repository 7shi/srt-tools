"""Truncate SRT timestamps to whole seconds (floor milliseconds to 000)."""

import sys
from .core import Srt


def process_file(path, output=None):
    srt = Srt.read(path)
    for e in srt.entries:
        e.start = e.start // 1000 * 1000
        e.end = e.end // 1000 * 1000
    srt.write(output or path)
    print(f"Done: {output or path}")


def setup_parser(subparsers):
    p = subparsers.add_parser('truncate', help='Truncate SRT timestamps to whole seconds')
    p.add_argument('files', nargs='+', help='SRT files to process')
    p.add_argument('-o', '--output', help='Output file (only with single input)')
    p.set_defaults(func=do_command)


def do_command(args):
    if args.output and len(args.files) > 1:
        print("error: -o/--output can only be used with a single input file", file=sys.stderr)
        sys.exit(1)

    for path in args.files:
        process_file(path, args.output)
