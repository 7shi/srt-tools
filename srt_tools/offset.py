"""Shift all SRT subtitle timestamps by a fixed time offset."""

import argparse
import sys

from .core import Srt
from .insert import parse_time


def parse_offset(s):
    """Parse a signed time string to milliseconds. Accepts +/- prefix."""
    s = s.strip()
    if s.startswith('+'):
        sign, s = 1, s[1:]
    elif s.startswith('-'):
        sign, s = -1, s[1:]
    else:
        sign = 1
    return sign * parse_time(s)


def apply_offset(srt, offset_ms):
    """Shift all entries by offset_ms. Raises ValueError if any start goes negative."""
    for e in srt.entries:
        if e.start + offset_ms < 0:
            raise ValueError(
                f"Offset would make timestamp negative: {Srt.ms_to_str(e.start)}"
            )
    for e in srt.entries:
        e.start += offset_ms
        e.end = max(0, e.end + offset_ms)


def setup_parser(subparsers):
    p = subparsers.add_parser('offset', help='Shift all timestamps by a time offset')
    # Use REMAINDER so that -0:02 isn't treated as an unknown flag by argparse
    p.add_argument('args', nargs=argparse.REMAINDER,
                   metavar='file... offset',
                   help='SRT file(s) followed by time offset (e.g. 0:02, -0:02, +0:02)')
    p.set_defaults(func=do_command)


def do_command(args):
    items = args.args
    if len(items) < 2:
        print("Usage: srt-tools offset <file> [file ...] <offset>", file=sys.stderr)
        sys.exit(1)
    offset_str = items[-1]
    files = items[:-1]

    try:
        offset_ms = parse_offset(offset_str)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    sign = '+' if offset_ms >= 0 else ''
    print(f"Offset: {sign}{offset_ms} ms")
    for path in files:
        try:
            srt = Srt.read(path)
            apply_offset(srt, offset_ms)
            srt.write(path)
            print(f"  {path}: {len(srt.entries)} entries updated")
        except ValueError as e:
            print(f"  {path}: Error - {e}", file=sys.stderr)
            sys.exit(1)
