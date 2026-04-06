"""Fix SRT files: merge consecutive duplicate phrases and fill gaps."""

from .core import Srt


def remove_empty(srt):
    filtered = [e for e in srt.entries if e.text.strip()]
    return Srt(filtered)


def merge_repeats(srt):
    if not srt.entries:
        return srt
    merged = [srt.entries[0]]
    for e in srt.entries[1:]:
        prev = merged[-1]
        if e.text == prev.text:
            prev.end = e.end
        else:
            merged.append(e)
    return Srt(merged)


def fill_gaps(srt, max_gap_ms=1000):
    count = 0
    for i in range(len(srt.entries) - 1):
        gap = srt.entries[i + 1].start - srt.entries[i].end
        if 0 < gap <= max_gap_ms:
            srt.entries[i].end = srt.entries[i + 1].start
            count += 1
    return count


def setup_parser(subparsers):
    p = subparsers.add_parser('fix', help='Fix SRT files: merge repeats and fill gaps')
    p.add_argument('files', nargs='+', help='SRT files to process')
    p.add_argument('--merge', action='store_true', help='Only merge repeated phrases')
    p.add_argument('--fill', action='store_true', help='Only fill gaps')
    p.add_argument('--empty', action='store_true', help='Only remove empty entries')
    p.add_argument('--max-gap', type=int, default=1000, help='Max gap in ms (default: 1000)')
    p.add_argument('--dry-run', action='store_true', help='Show changes without writing')
    p.set_defaults(func=do_command)


def do_command(args):
    any_flag = args.merge or args.fill or args.empty
    do_empty = args.empty or not any_flag
    do_merge = args.merge or not any_flag
    do_fill = args.fill or not any_flag

    for path in args.files:
        srt = Srt.read(path)
        changes = []

        if do_empty:
            before = len(srt.entries)
            srt = remove_empty(srt)
            after = len(srt.entries)
            if before != after:
                changes.append(f"removed {before - after} empty")

        if do_merge:
            before = len(srt.entries)
            srt = merge_repeats(srt)
            after = len(srt.entries)
            if before != after:
                changes.append(f"merged {before} -> {after}")

        if do_fill:
            count = fill_gaps(srt, args.max_gap)
            if count:
                changes.append(f"filled {count} gaps")

        if not changes:
            print(f"{path}: no change")
            continue
        if args.dry_run:
            print(f"{path}: would {', '.join(changes)}")
        else:
            srt.write(path)
            print(f"{path}: {', '.join(changes)}")
