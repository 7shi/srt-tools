"""SRT files to aligned text."""

import os
import re
import sys
from .core import Srt


def setup_parser(subparsers):
    p = subparsers.add_parser('convert', help='Convert SRT to text')
    p.add_argument('input', help='Source .XX.srt file (e.g. .kn.srt)')
    p.add_argument('-l', '--lang', help='Translation language (e.g. ja)')
    p.add_argument('-o', '--output', help='Output file')
    p.set_defaults(func=do_command)


def do_command(args):
    src_path = args.input
    m = re.search(r"\.([a-z]{2,3})\.srt$", src_path)
    if not m:
        print("error: input must be a .XX.srt file (e.g. .kn.srt)", file=sys.stderr)
        sys.exit(1)
    src_lang = m.group(1)
    suffix = f".{src_lang}.srt"
    base = src_path[:-len(suffix)]
    latin_path = f"{base}.{src_lang}-latin.srt"

    src = Srt.read(src_path)
    latin = Srt.read(latin_path) if os.path.exists(latin_path) else None

    if args.lang:
        lang_path = f"{base}.{args.lang}.srt"
        trans = Srt.read(lang_path)
    else:
        trans = None

    lines = []
    for i, e in enumerate(src.entries):
        h = e.start // 3600000
        m_val = (e.start % 3600000) // 60000
        s_val = (e.start % 60000) // 1000
        time_str = f"{h * 60 + m_val}:{s_val:02d}"
        parts = [f"{time_str} {e.text}"]
        if latin and i < len(latin.entries):
            parts.append(f"({latin.entries[i].text})")
        if trans and i < len(trans.entries):
            parts.append(trans.entries[i].text)
        lines.append(" ".join(parts))

    if args.output:
        output_path = args.output
    elif args.lang:
        output_path = f"{base}.{args.lang}.txt"
    else:
        output_path = f"{base}.{src_lang}.txt"

    ext = os.path.splitext(output_path)[1].lower()
    if ext == '.txt':
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines) + "\n")
        print(output_path)
    else:
        print(f"error: unsupported format: {ext}", file=sys.stderr)
        sys.exit(1)
