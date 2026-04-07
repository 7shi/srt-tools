# Changelog

## [0.1.4] - 2026-04-07

### Added

- `offset` subcommand to shift all SRT timestamps by a fixed time offset
- `concat` subcommand to concatenate SRT files with video duration offsets

## [0.1.3] - 2026-04-07

### Added

- `merge` subcommand to combine SRT files into a single Markdown file

## [0.1.2] - 2026-04-07

### Changed

- `fix` subcommand now removes empty entries by default
- Added `--empty` flag to remove empty entries only

## [0.1.1] - 2026-04-06

### Added

- `bom` subcommand to add or remove BOM from files

## [0.1.0] - 2026-04-06

Initial release.

### Features

- `insert` — insert a subtitle entry at a specified time
- `sync` — copy timestamps from a source SRT file to target files
- `convert` — convert SRT files to aligned text
- `atempo` — adjust timestamps by a tempo factor
- `fix` — merge consecutive duplicate phrases and fill gaps
- `truncate` — truncate timestamps to whole seconds
- Library API: `Srt`, `SrtEntry`, `read_text`, `write_text`
