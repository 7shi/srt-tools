import sys
from pathlib import Path

BOM = b"\xef\xbb\xbf"


def read_text(path, encoding="utf-8"):
    data = Path(path).read_bytes()
    if data.startswith(BOM):
        data = data[len(BOM):]
    return data.decode(encoding)


def write_text(path, text, encoding="utf-8"):
    Path(path).write_bytes(BOM + text.encode(encoding))


def add_bom(files):
    for f in files:
        data = f.read_bytes()
        if data.startswith(BOM):
            print(f"BOM exists: {f}")
        else:
            f.write_bytes(BOM + data)
            print(f"BOM added: {f}")


def remove_bom(files):
    for f in files:
        data = f.read_bytes()
        if data.startswith(BOM):
            f.write_bytes(data[len(BOM):])
            print(f"BOM removed: {f}")
        else:
            print(f"No BOM: {f}")


def setup_parser(subparsers):
    parser = subparsers.add_parser('bom', help='Add or remove BOM from files')
    parser.add_argument('files', nargs='+', type=Path, metavar='FILE')
    parser.add_argument('--remove', action='store_true', help='Remove BOM instead of adding')
    parser.set_defaults(func=do_command)


def do_command(args):
    (remove_bom if args.remove else add_bom)(args.files)
