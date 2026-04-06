"""Sync timestamps from a source SRT file to target SRT files."""

import sys
from .core import Srt


def setup_parser(subparsers):
    p = subparsers.add_parser('sync', help='Sync timestamps from source to target SRT files')
    p.add_argument('source', help='Source SRT file (e.g. XX-title.kn.srt)')
    p.add_argument('targets', nargs='+', help='Target SRT files to update')
    p.set_defaults(func=do_command)


def do_command(args):
    source = Srt.read(args.source)

    for target_path in args.targets:
        target = Srt.read(target_path)
        if len(source.entries) != len(target.entries):
            print(f"Error: {args.source} has {len(source.entries)} entries, "
                  f"but {target_path} has {len(target.entries)} entries",
                  file=sys.stderr)
            sys.exit(1)
        changed = False
        for s, t in zip(source.entries, target.entries):
            if t.start != s.start or t.end != s.end:
                t.start = s.start
                t.end = s.end
                changed = True
        if changed:
            target.write(target_path)
            print(f"Updated: {target_path}")
        else:
            print(f"No change: {target_path}")
