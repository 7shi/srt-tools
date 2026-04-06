"""Merge SRT files into a single Markdown file."""

import os
import sys
from .core import Srt


def merge_files(files, output="-"):
    files = sorted(files)

    if output == "-":
        out = sys.stdout
    else:
        out = open(output, "w", encoding="utf-8")

    try:
        for i, fpath in enumerate(files):
            base = os.path.basename(fpath)
            name = base[: base.rfind(".")] if "." in base else base
            srt = Srt.read(fpath)
            lines = []
            for e in srt.entries:
                m = (e.start // 60000) % 60
                s = e.start // 1000 % 60
                lines.append(f"{m}:{s:02d} {e.text}")
            content = "\n".join(lines)
            if i > 0:
                out.write("\n")
            out.write(f"# {name}\n\n{content}\n")
    finally:
        if out is not sys.stdout:
            out.close()


def setup_parser(subparsers):
    p = subparsers.add_parser('merge', help='Merge SRT files into a single Markdown file')
    p.add_argument('files', nargs='+', help='Input SRT files')
    p.add_argument('-o', '--output', default='-', help='Output file (default: stdout)')
    p.set_defaults(func=do_command)


def do_command(args):
    merge_files(args.files, args.output)
