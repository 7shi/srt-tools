"""srt-tools: SRT subtitle tools"""

import argparse
from . import __version__, bom, insert, sync, converter, atempo, fix, truncate


def main():
    parser = argparse.ArgumentParser(prog='srt-tools', description='SRT subtitle tools')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    subparsers = parser.add_subparsers(dest='command', required=True)

    for mod in [bom, insert, sync, converter, atempo, fix, truncate]:
        mod.setup_parser(subparsers)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
