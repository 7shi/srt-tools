"""Adjust SRT subtitle timing by tempo factor."""

from .core import Srt


def convert(infile, outfile, tempo):
    srt = Srt.read(infile)
    for e in srt.entries:
        e.start = int(e.start / tempo)
        e.end = int(e.end / tempo)
    srt.write(outfile)
    print(f"{infile} -> {outfile} (tempo={tempo})")


def setup_parser(subparsers):
    p = subparsers.add_parser('atempo', help='Adjust SRT timing by tempo factor')
    p.add_argument('input', help='Input SRT file')
    p.add_argument('-o', '--output', required=True, help='Output SRT file')
    p.add_argument('-t', '--tempo', type=float, required=True, help='Tempo factor (e.g. 1.25)')
    p.set_defaults(func=do_command)


def do_command(args):
    convert(args.input, args.output, args.tempo)
