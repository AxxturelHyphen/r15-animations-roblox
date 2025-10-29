import argparse
import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path
import shutil
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Dict, List


CATEGORIES: Dict[str, List[str]] = {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".md", ".rtf"],
    "Sheets": [".xls", ".xlsx", ".csv"],
    "Audio": [".mp3", ".wav", ".flac"],
    "Video": [".mp4", ".mkv", ".mov"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
}

EXTENSION_MAP: Dict[str, str] = {
    ext.lower(): category for category, extensions in CATEGORIES.items() for ext in extensions
}

LOG_COLUMNS = ["original_path", "dest_path", "category", "action", "status", "message"]


def categorize(ext: str) -> str:
    """Return the category name for a given file extension."""
    if not ext:
        return "Other"
    return EXTENSION_MAP.get(ext.lower(), "Other")


def _resolve_destination(src: Path, dest_dir: Path) -> Path:
    """Compute the destination path, appending suffixes when a file already exists."""
    target = dest_dir / src.name
    if not target.exists():
        return target

    stem = src.stem
    suffix = src.suffix
    counter = 1
    while True:
        candidate = dest_dir / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def safe_move(src: Path, dest_dir: Path) -> Path:
    """Move src into dest_dir, adding a numeric suffix to avoid overwriting existing files."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    target = _resolve_destination(src, dest_dir)
    shutil.move(str(src), str(target))
    return target


def sort_files(src_dir: Path, dst_dir: Path, dry_run: bool) -> Dict[str, object]:
    """
    Sort files from src_dir into categorized subdirectories under dst_dir.

    Returns a summary dictionary containing counts, per-category totals, and log rows.
    """
    if not src_dir.exists():
        raise FileNotFoundError(f"Source directory does not exist: {src_dir}")
    if not src_dir.is_dir():
        raise NotADirectoryError(f"Source path is not a directory: {src_dir}")

    summary = {
        "total": 0,
        "moved": 0,
        "planned": 0,
        "skipped": 0,
        "errors": 0,
        "categories": defaultdict(int),
        "rows": [],
    }
    rows: List[Dict[str, str]] = summary["rows"]

    src_dir = src_dir.resolve()
    dst_dir = dst_dir.resolve(strict=False)

    items = sorted(src_dir.iterdir(), key=lambda p: p.name.lower())
    if not dry_run:
        dst_dir.mkdir(parents=True, exist_ok=True)

    for item in items:
        if not item.is_file():
            continue

        summary["total"] += 1
        category = categorize(item.suffix)
        category_dir = dst_dir / category
        action = "plan" if dry_run else "move"
        final_dest: Path | None = None
        status = "ok"
        message = ""

        try:
            if dry_run:
                final_dest = _resolve_destination(item, category_dir)
                summary["planned"] += 1
            else:
                final_dest = safe_move(item, category_dir)
                summary["moved"] += 1
            summary["categories"][category] += 1
        except Exception as exc:  # noqa: BLE001
            status = "error"
            message = str(exc)
            summary["errors"] += 1
            summary["skipped"] += 1
            final_dest = (category_dir / item.name) if final_dest is None else final_dest

        original_path = item.resolve()
        dest_path_str = (
            str(final_dest.resolve(strict=False)) if final_dest is not None else ""
        )

        rows.append(
            {
                "original_path": str(original_path),
                "dest_path": dest_path_str,
                "category": category,
                "action": action,
                "status": status,
                "message": message,
            }
        )

    return summary


def write_log(rows: List[Dict[str, str]], export_dir: Path) -> Path:
    """Persist the provided log rows to a timestamped CSV file under export_dir."""
    export_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = export_dir / f"sort_log_{timestamp}.csv"

    with log_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=LOG_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    return log_path.resolve()


def _print_summary(summary: Dict[str, object], log_path: Path, src_dir: Path, dst_dir: Path) -> None:
    """Print detailed summary information to stdout."""
    print(f"Working directory: {Path.cwd().resolve()}")
    print(f"Source: {src_dir.resolve()}")
    print(f"Destination: {dst_dir.resolve(strict=False)}")
    print(f"Log CSV: {log_path}")
    print(f"Files processed: {summary['total']}")
    print(f"Moved: {summary['moved']} | Planned: {summary['planned']} | Skipped: {summary['skipped']} | Errors: {summary['errors']}")
    print("Per-category counts:")
    categories: Dict[str, int] = summary["categories"]
    for category in sorted(CATEGORIES.keys() | {"Other"}):
        count = categories.get(category, 0)
        print(f"  - {category}: {count}")
    other_only = set(categories.keys()) - set(CATEGORIES.keys()) - {"Other"}
    for extra in sorted(other_only):
        print(f"  - {extra}: {categories[extra]}")
    print(f"[OK] Sorted {summary['total']} files. Log: {log_path}")


def run_cli(argv: List[str]) -> None:
    """Run the sorter in CLI mode."""
    parser = argparse.ArgumentParser(
        description="Organize files from a source folder into categorized subfolders."
    )
    parser.add_argument("--src", required=True, help="Source directory with files to sort")
    parser.add_argument("--dst", required=True, help="Destination directory for sorted files")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate actions without moving files",
    )
    args = parser.parse_args(argv)

    src_raw = args.src.strip()
    if not src_raw:
        print("Error: --src must not be empty.", file=sys.stderr)
        sys.exit(2)

    dst_raw = args.dst.strip()
    if not dst_raw:
        print("Error: --dst must not be empty.", file=sys.stderr)
        sys.exit(2)

    src_dir = Path(src_raw).expanduser()
    dst_dir = Path(dst_raw).expanduser()

    if not src_dir.exists() or not src_dir.is_dir():
        print(
            f"Error: Source directory is invalid: {src_dir.resolve(strict=False)}",
            file=sys.stderr,
        )
        sys.exit(2)

    src_dir = src_dir.resolve()
    dst_dir = dst_dir.resolve(strict=False)

    try:
        summary = sort_files(src_dir, dst_dir, args.dry_run)
    except Exception as exc:  # noqa: BLE001
        print(f"Error during sorting: {exc}", file=sys.stderr)
        sys.exit(1)

    log_path = write_log(summary["rows"], Path.cwd() / "exports")

    for row in summary["rows"]:
        dest_display = row["dest_path"] or "<no-destination>"
        print(f"{row['action'].upper()}: {row['original_path']} -> {dest_display} [{row['status']}]")

    _print_summary(summary, log_path, src_dir, dst_dir)


class SorterGUI:
    """Tkinter GUI wrapper for the sorter."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Folder File Sorter")
        self.root.geometry("400x220")
        self.root.resizable(False, False)

        self.src_var = tk.StringVar()
        self.dst_var = tk.StringVar()
        self.dry_var = tk.BooleanVar(value=False)

        self._build_layout()

    def _build_layout(self) -> None:
        """Create GUI widgets."""
        padding = {"padx": 10, "pady": 5}

        tk.Label(self.root, text="Source Folder:").grid(row=0, column=0, sticky="w", **padding)
        tk.Label(self.root, textvariable=self.src_var, anchor="w", relief="sunken", width=40).grid(
            row=0, column=1, **padding
        )
        tk.Button(self.root, text="Select Source Folder", command=self._choose_source).grid(
            row=0, column=2, **padding
        )

        tk.Label(self.root, text="Destination Folder:").grid(row=1, column=0, sticky="w", **padding)
        tk.Label(self.root, textvariable=self.dst_var, anchor="w", relief="sunken", width=40).grid(
            row=1, column=1, **padding
        )
        tk.Button(self.root, text="Select Destination Folder", command=self._choose_destination).grid(
            row=1, column=2, **padding
        )

        tk.Checkbutton(self.root, text="Dry-run", variable=self.dry_var).grid(
            row=2, column=1, sticky="w", **padding
        )

        tk.Button(self.root, text="Run Sorter", command=self._run_sorter, width=20).grid(
            row=3, column=1, pady=20
        )

    def _choose_source(self) -> None:
        """Prompt for source directory."""
        selected = filedialog.askdirectory(title="Select Source Folder")
        if selected:
            self.src_var.set(str(Path(selected).resolve()))

    def _choose_destination(self) -> None:
        """Prompt for destination directory."""
        selected = filedialog.askdirectory(title="Select Destination Folder")
        if selected:
            self.dst_var.set(str(Path(selected).resolve()))

    def _run_sorter(self) -> None:
        """Execute the sort operation and show results."""
        src = self.src_var.get().strip()
        dst = self.dst_var.get().strip()

        if not src:
            messagebox.showerror("Missing source", "Please select a source folder.")
            return
        if not dst:
            messagebox.showerror("Missing destination", "Please select a destination folder.")
            return

        src_dir = Path(src)
        dst_dir = Path(dst)

        if not src_dir.exists() or not src_dir.is_dir():
            messagebox.showerror("Invalid source", f"Source directory is invalid:\n{src_dir}")
            return

        try:
            summary = sort_files(src_dir, dst_dir, self.dry_var.get())
            log_path = write_log(summary["rows"], Path.cwd() / "exports")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Sort failed", str(exc))
            return

        for row in summary["rows"]:
            dest_display = row["dest_path"] or "<no-destination>"
            print(f"{row['action'].upper()}: {row['original_path']} -> {dest_display} [{row['status']}]")

        _print_summary(summary, log_path, src_dir, dst_dir)

        message = (
            "Sorting completed successfully.\n"
            f"Destination: {dst_dir.resolve()}\n"
            f"Log CSV: {log_path}"
        )
        messagebox.showinfo("Success", message)


def run_gui() -> None:
    """Launch the Tkinter GUI."""
    root = tk.Tk()
    SorterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_cli(sys.argv[1:])
    else:
        run_gui()
