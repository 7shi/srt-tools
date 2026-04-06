# srt-tools

SRT subtitle file manipulation tools. Reads and writes UTF-8 with BOM.

## Installation

### As a tool (recommended)

```bash
uv tool install https://github.com/7shi/srt-tools.git
```

### From source

```bash
git clone https://github.com/7shi/srt-tools
cd srt-tools
uv sync
```

**Note**: When using source installation, prefix all commands with `uv run` (e.g., `uv run srt-tools insert ...`).

## Commands

```
uv run srt-tools <subcommand> [options]
```

### bom

Add or remove BOM from files.

```
uv run srt-tools bom a.txt b.txt
uv run srt-tools bom --remove a.txt b.txt
```

### insert

Insert a subtitle entry at a specified time in an SRT file.

```
uv run srt-tools insert song.kn.srt 1:02 "ಇದು ಮಾಡಿದೆ!"
```

Time formats: `M:SS`, `MM:SS`, `H:MM:SS`, `HH:MM:SS,mmm`

### sync

Copy timestamps from a source SRT file to one or more target SRT files.

```
uv run srt-tools sync source.kn.srt target.ja.srt target.en.srt
```

### convert

Convert SRT files to aligned text. Output format is determined by the file extension (currently only `.txt` is supported).

```
uv run srt-tools convert song.kn.srt -l ja
uv run srt-tools convert song.kn.srt -l ja -o output.txt
```

The language code is detected from the input filename. If a `-latin.srt` (romanized) file exists, it is included in the output.

### atempo

Adjust SRT timestamps by a tempo factor.

```
uv run srt-tools atempo input.srt -o output.srt -t 1.25
```

### fix

Merge consecutive duplicate phrases and/or fill gaps between entries.

```
uv run srt-tools fix *.srt
uv run srt-tools fix *.srt --merge       # merge only
uv run srt-tools fix *.srt --fill        # fill gaps only
uv run srt-tools fix *.srt --dry-run     # preview changes without writing
uv run srt-tools fix *.srt --max-gap 500 # set maximum gap in ms
```

### truncate

Truncate SRT timestamps to whole seconds (floor milliseconds to 000).

```
uv run srt-tools truncate *.srt
uv run srt-tools truncate input.srt -o output.srt
```

## Library

```python
from srt_tools import Srt, SrtEntry, read_text, write_text
```

- `SrtEntry` — subtitle entry (`num`, `start`, `end` in milliseconds, `text`)
- `Srt.read(path)` — read an SRT file (BOM stripped automatically)
- `Srt.write(path)` — write an SRT file (BOM added automatically)
- `Srt.ms_to_str(ms)` / `Srt.str_to_ms(s)` — convert between milliseconds and SRT timestamps
- `read_text(path)` — read a UTF-8 file, stripping BOM if present
- `write_text(path, text)` — write a UTF-8 file with BOM
