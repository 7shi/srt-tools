"""SRT file parsing and read/write."""

import re
from dataclasses import dataclass
from .bom import read_text, write_text


@dataclass
class SrtEntry:
    num: int
    start: int  # milliseconds
    end: int    # milliseconds
    text: str


class Srt:
    def __init__(self, entries=None):
        self.entries = list(entries) if entries else []

    @staticmethod
    def ms_to_str(ms):
        h = ms // 3600000
        ms %= 3600000
        m = ms // 60000
        ms %= 60000
        s = ms // 1000
        ms %= 1000
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    @staticmethod
    def str_to_ms(s):
        m = re.match(r"(\d+):(\d+):(\d+),(\d+)", s)
        if not m:
            raise ValueError(f"Invalid SRT timestamp: {s}")
        h, mn, sc, ms = int(m[1]), int(m[2]), int(m[3]), int(m[4])
        return ((h * 60 + mn) * 60 + sc) * 1000 + ms

    @staticmethod
    def read(path):
        text = read_text(path)
        entries = []
        for block in re.split(r"\n\n+", text.strip()):
            lines = block.strip().split("\n")
            if len(lines) < 2:
                continue
            num = int(lines[0].strip())
            m = re.match(
                r"(\d+:\d+:\d+,\d+)\s*-->\s*(\d+:\d+:\d+,\d+)",
                lines[1].strip(),
            )
            if not m:
                continue
            start = Srt.str_to_ms(m[1])
            end = Srt.str_to_ms(m[2])
            content = "\n".join(lines[2:])
            entries.append(SrtEntry(num=num, start=start, end=end, text=content))
        return Srt(entries)

    def write(self, path):
        write_text(path, str(self))

    def __str__(self):
        blocks = []
        for i, e in enumerate(self.entries):
            ts = f"{Srt.ms_to_str(e.start)} --> {Srt.ms_to_str(e.end)}"
            blocks.append(f"{i + 1}\n{ts}\n{e.text}")
        return "\n\n".join(blocks) + "\n"
