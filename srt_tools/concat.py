"""Concatenate multiple SRT files with video duration offsets."""

import argparse
import sys

from .core import Srt, SrtEntry
from .insert import parse_time


def concat_files(files, durations_ms):
    """Concatenate SRT files, shifting each by cumulative video durations.

    files: list of file paths
    durations_ms: list of video durations in ms (len == len(files) - 1)
    Returns a new Srt with all entries combined and renumbered.
    """
    entries = []
    cumulative = 0
    for i, path in enumerate(files):
        srt = Srt.read(path)
        for e in srt.entries:
            entries.append(SrtEntry(
                num=0,
                start=e.start + cumulative,
                end=e.end + cumulative,
                text=e.text,
            ))
        if i < len(durations_ms):
            cumulative += durations_ms[i]
    for i, e in enumerate(entries):
        e.num = i + 1
    return Srt(entries)


def setup_parser(subparsers):
    p = subparsers.add_parser(
        'concat',
        help='Concatenate multiple SRT files with video duration offsets',
    )
    p.add_argument(
        'args', nargs=argparse.REMAINDER,
        metavar='file [duration file] ...',
        help='SRT files interleaved with video durations (e.g. a.srt 10:00 b.srt 8:30 c.srt)',
    )
    p.add_argument('-o', '--output', metavar='FILE',
                   help='Output file (default: stdout)')
    p.set_defaults(func=do_command)


def do_command(args):
    items = args.args
    if len(items) < 1 or len(items) % 2 == 0:
        print(
            "Usage: srt-tools concat file [duration file] ...\n"
            "  e.g. srt-tools concat a.srt 10:00 b.srt 8:30 c.srt",
            file=sys.stderr,
        )
        sys.exit(1)

    files = items[0::2]
    duration_strs = items[1::2]

    durations_ms = []
    for s in duration_strs:
        try:
            durations_ms.append(parse_time(s))
        except ValueError as e:
            print(f"Error: invalid duration '{s}': {e}", file=sys.stderr)
            sys.exit(1)

    try:
        result = concat_files(files, durations_ms)
    except (ValueError, FileNotFoundError, OSError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    output = str(result)
    if args.output:
        from .bom import write_text
        write_text(args.output, output)
    else:
        print(output, end='')
