# Folder File Sorter

## Overview
Folder File Sorter is a Windows-ready utility that organizes files from a source directory into categorized subfolders inside a destination directory. It supports both a Tkinter GUI for everyday use and a CLI for automation-friendly workflows. The tool runs entirely offline and relies only on the Python standard library.

## GUI Usage
1. Launch the application without command-line arguments (double-click `main.py` or the packaged EXE).
2. Click **Select Source Folder** and choose the directory with files to organize.
3. Click **Select Destination Folder** for the output location. The sorter will create category subfolders as needed.
4. Optional: enable **Dry-run** to preview actions without moving files.
5. Press **Run Sorter**. When complete, a dialog reports the absolute destination path and the CSV log location under `exports/`.

The GUI window is fixed at approximately 400×220 pixels to remain compact on screen.

## CLI Usage
Run `python` with arguments to operate headless:

```bash
python src/main.py --src "C:\path\to\source" --dst "C:\path\to\sorted" [--dry-run]
```

- `--src`: source directory containing the files to organize (**required**)
- `--dst`: destination directory that will receive the categorized subfolders (**required**)
- `--dry-run`: optional flag that reports planned moves without touching the filesystem

The CLI prints each action, the working directory, source and destination paths, and a per-category summary. On success it reports the absolute path to the CSV log.

## Dry-run Mode
Dry-run mode leaves the filesystem untouched while still producing a full CSV log. Each log entry records the original file path, the proposed destination, and the planned action. Destinations and summaries reflect the names that would be used, including duplicate suffix handling.

## Logs
Every run writes a CSV log to `exports/sort_log_<timestamp>.csv`. Columns include:

- `original_path`
- `dest_path`
- `category`
- `action`
- `status`
- `message`

The log is useful for auditing, undo steps, or rerunning planned actions later.

## Build (PyInstaller)
Create a standalone Windows executable with:

```bash
pyinstaller --onefile src/main.py --noconsole --name Folder_File_Sorter
```

The resulting `Folder_File_Sorter.exe` is emitted to the `dist/` directory by PyInstaller. Copy it into the project's `build/` folder for distribution.

## Test / Sample Run
Perform a dry-run from the CLI as a quick confidence check:

```bash
python src/main.py --src "C:\path\to\source" --dst "C:\path\to\sorted" --dry-run
```

Review the console output and the generated log under `exports/` before conducting a live move.

## Support Policy
This release includes 7 days of bugfix and setup assistance beginning from the delivery date. Reach out within that window for help reproducing or resolving issues encountered during installation or use.
