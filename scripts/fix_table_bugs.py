#!/usr/bin/env python3
"""
Fix systematic table bugs in SOGo documentation:

1. Remove ": Description" and similar suffixes from table header cells
   (e.g. "Methode: Description" → "Methode",
    "Tastenkombination: Zu drückende Taste" → "Tastenkombination")
2. Fix empty-first-cell bug in table data rows (| | content | ... → | content | ...)
3. Rename specific headers per reviewer feedback:
   "Feld" → "Eingabefeld", "Muster" → "Zeitlicher Abstand"

Usage: python3 scripts/fix_table_bugs.py [--dry-run]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DIRS = [
    REPO_ROOT / "site" / "i18n" / "de" / "docusaurus-plugin-content-docs" / "version-5",
    REPO_ROOT / "site" / "versioned_docs" / "version-5",
    REPO_ROOT / "site" / "versioned_docs" / "version-6",
    REPO_ROOT / "site" / "i18n" / "de" / "docusaurus-plugin-content-docs" / "version-6",
]

# Special header renames (applied AFTER stripping the ": suffix")
HEADER_RENAMES = {
    "Feld": "Eingabefeld",
    "Muster": "Zeitlicher Abstand",
}


def strip_header_suffix(cell: str) -> str:
    """Remove ': Description' style suffixes from a table header cell, keeping the label.
    Preserves leading/trailing whitespace for alignment."""
    stripped = cell.strip()
    if ": " not in stripped:
        return cell
    # Keep the part before the first ": " (the label)
    label = stripped.split(": ", 1)[0].strip()
    # Apply special renames
    label = HEADER_RENAMES.get(label, label)
    # Preserve original padding: leading space + label + trailing space
    lead = len(cell) - len(cell.lstrip())
    trail = len(cell) - len(cell.rstrip())
    return " " * lead + label + " " * trail


def count_columns(row: str) -> int:
    """Count the number of columns in a markdown table row."""
    return row.count("|") - 1  # subtract 1 because leading | is not a separator


def fix_table_headers_and_rows(lines: list[str]) -> list[str]:
    """Fix table header suffixes and empty-first-cell in data rows."""
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Detect table header: current line starts with | and next line is a separator
        if (
            line.strip().startswith("|")
            and i + 1 < len(lines)
            and re.match(r"^\s*\|[-\s|:]+\|\s*$", lines[i + 1])
        ):
            # This is a table header line — strip ": suffix" from each cell
            cells = line.split("|")
            # cells[0] is empty (before first |), cells[-1] is empty (after last |)
            new_cells = [cells[0]]
            for c in cells[1:-1]:
                new_cells.append(strip_header_suffix(c))
            new_cells.append(cells[-1])
            new_header = "|".join(new_cells)
            result.append(new_header)
            result.append(lines[i + 1])  # separator line unchanged
            i += 2
            # Fix data rows: remove empty first cell if row has one more column
            # than header
            header_cols = count_columns(new_header)
            while (
                i < len(lines)
                and lines[i].strip().startswith("|")
                and not re.match(r"^\s*\|[-\s|:]+\|\s*$", lines[i])
            ):
                data_line = lines[i]
                data_cols = count_columns(data_line)
                if data_cols == header_cols + 1 and re.match(r"^\s*\|\s*\|", data_line):
                    # Empty first cell — remove it
                    # Split, remove the empty second element, rejoin
                    parts = data_line.split("|")
                    # parts[0] = "", parts[1] = "" (empty cell), parts[2:] = content
                    new_parts = [parts[0]] + parts[2:]
                    data_line = "|".join(new_parts)
                result.append(data_line)
                i += 1
        else:
            result.append(line)
            i += 1
    return result


def main():
    dry_run = "--dry-run" in sys.argv
    total_files = 0
    total_changes = 0

    for d in DIRS:
        if not d.exists():
            continue
        for md_file in sorted(d.glob("*.md")):
            original = md_file.read_text(encoding="utf-8")
            lines = original.split("\n")
            fixed = fix_table_headers_and_rows(lines)
            fixed_text = "\n".join(fixed)
            if fixed_text != original:
                total_files += 1
                # Count changes
                total_changes += sum(
                    1 for a, b in zip(original.split("\n"), fixed, strict=False) if a != b
                )
                if not dry_run:
                    md_file.write_text(fixed_text, encoding="utf-8")
                    print(f"  Fixed: {md_file.relative_to(REPO_ROOT)}")
                else:
                    print(f"  Would fix: {md_file.relative_to(REPO_ROOT)}")

    status = "Would fix" if dry_run else "Fixed"
    print(f"\n{status} {total_files} files, ~{total_changes} line changes")


if __name__ == "__main__":
    main()
