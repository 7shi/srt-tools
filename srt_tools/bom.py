#!/usr/bin/env python3

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
