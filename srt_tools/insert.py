"""Insert a subtitle entry at a specified time in an SRT file."""

import re
from .core import Srt, SrtEntry


def parse_time(s):
    """Convert a time string to milliseconds."""
    s = s.strip()
    # SRT format: HH:MM:SS,mmm
    m = re.match(r"(\d+):(\d+):(\d+),(\d+)$", s)
    if m:
        h, mn, sc, ms = int(m[1]), int(m[2]), int(m[3]), int(m[4])
        return ((h * 60 + mn) * 60 + sc) * 1000 + ms
    # M:SS, MM:SS, or H:MM:SS (short form)
    m = re.match(r"(\d+):(\d+)(?::(\d+))?(?:\.(\d+))?$", s)
    if m:
        if m[3] is not None:
            h, mn, sc = int(m[1]), int(m[2]), int(m[3])
        else:
            h, mn, sc = 0, int(m[1]), int(m[2])
        ms = int(m[4]) if m[4] else 0
        return ((h * 60 + mn) * 60 + sc) * 1000 + ms
    # Seconds only
    m = re.match(r"(\d+)(?:\.(\d+))?$", s)
    if m:
        sc = int(m[1])
        ms = int(m[2]) if m[2] else 0
        return sc * 1000 + ms
    raise ValueError(f"Cannot parse time: {s}")


def insert_subtitle(srt, insert_ms, text):
    """Insert a subtitle at the specified time."""
    entries = srt.entries
    fmt = Srt.ms_to_str

    # Find the entry containing the insertion time
    target = None
    for i, e in enumerate(entries):
        if e.start < insert_ms < e.end:
            target = i
            break

    if target is None:
        # Insert between entries
        for i in range(len(entries) - 1):
            if entries[i].end <= insert_ms <= entries[i + 1].start:
                new_entry = SrtEntry(
                    num=0, start=insert_ms, end=entries[i + 1].start, text=text
                )
                entries.insert(i + 1, new_entry)
                print(f"  #{i + 2}: {fmt(insert_ms)} --> {fmt(new_entry.end)}")
                return
        raise ValueError(
            f"No entry found containing time {fmt(insert_ms)}."
        )

    e = entries[target]
    old_end = e.end
    e.end = insert_ms

    new_entry = SrtEntry(num=0, start=insert_ms, end=old_end, text=text)
    entries.insert(target + 1, new_entry)

    print(f"  #{target + 1}: {fmt(e.start)} --> {fmt(insert_ms)} (shortened)")
    print(f"  #{target + 2}: {fmt(insert_ms)} --> {fmt(old_end)} (inserted)")


def setup_parser(subparsers):
    p = subparsers.add_parser('insert', help='Insert subtitle at specified time')
    p.add_argument('file', help='SRT file')
    p.add_argument('time', help='Time (M:SS, H:MM:SS, or HH:MM:SS,mmm)')
    p.add_argument('text', help='Subtitle text')
    p.set_defaults(func=do_command)


def do_command(args):
    insert_ms = parse_time(args.time)
    print(f"Insert time: {Srt.ms_to_str(insert_ms)}")
    print(f"Insert text: {args.text}")
    print()
    srt = Srt.read(args.file)
    print(f"{args.file}:")
    insert_subtitle(srt, insert_ms, args.text)
    srt.write(args.file)
    print(f"\nDone: {len(srt.entries)} entries total")
