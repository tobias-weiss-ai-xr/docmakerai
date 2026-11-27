#!/usr/bin/env python3
"""Validate markdown files for accessibility compliance (WCAG 2.1 Level A).

Aligned with the writing guidelines in AGENTS.md:

- Screen-reader sections must NOT predict what a reader will announce on load
  ("Screen reader announces: X"). They use "You should hear: X" (EN) /
  "Sie hören: X" (DE) and start from ``Strg+Pos1`` / ``Ctrl+Home``.
- No tab-for-tab paths ("Tab from the address bar", "Tab, Tab, Tab"); the tab
  order depends on browser, instance and screen-reader settings. Describe the
  field and say "Tab (repeat as needed) until ...".
- NVDA reading vs. focus mode is a global note, not repeated per page.
- Escape leaves screen-reader focus mode; it does not clear form input.

Severity model: ``error`` breaks compliance, ``warning`` is advisory. Exit
code is non-zero only when errors exist (``--strict`` promotes warnings).
"""

import re
import sys
from pathlib import Path

# Meta / tooling pages that are not user guides and are exempt from the
# accessibility-section requirements.
META_EXCLUDE = {
    "README.md",
    "ROADMAP.md",
    "SEO.md",
    "performance.md",
    "accessibility-section-template.md",
    "sogo-gaps.md",
}

GERMAN_DIR_MARKERS = ("i18n/de",)

# Phrases that encode tab-for-tab paths (AGENTS.md forbids them).
FORBIDDEN_TAB_CHAINS = [
    r"`?Tab`?\s+(?:from|starting at|beginning at)\s+(?:the\s+)?(?:address\s*bar|browser\s*bar)",
    r"`?Tab`?\s+aus\s+der\s+Adressleiste",
    r"(?:`Tab`,?\s+){3,}",  # three+ consecutive Tab presses described as a path
]

# Predictions about screen-reader output instead of "you should hear".
FORBIDDEN_ANNOUNCEMENTS = [
    r"screen\s*reader\s+announces\s*:",
    r"(?<!\bshould\s)(?<!\bwill\s)\bannounces\s*:",
    r"screen\s*reader\s*:\s*" "",
    r"screenreader\s*:\s*" "",
    r"\bvorliest\s*:\s*\"",  # German: predicting the load announcement
]

KEYBOARD_HINTS = re.compile(
    r"`?(Tab|Shift\+Tab|Enter|Space|Arrow|Strg|Tastatur|keyboard|Shortcut|Alt\+|Ctrl\+|Escape)`?",
    re.IGNORECASE,
)

ORIENTATION_HINTS = re.compile(
    r"(Ctrl\+Home|Strg\+Pos1|Ctrl\+Pos1|"
    r"to the top of the page|zum Seitenanfang|Seitenanfang)",
    re.IGNORECASE,
)

HIGH_CONTRAST = re.compile(
    r"(high.?contrast|High.?Contrast|dark.?mode|Dark.?Mode|Hochkontrast|Dunkelmodus)",
    re.IGNORECASE,
)


class AccessibilityValidator:
    """Validates markdown files for accessibility compliance."""

    def __init__(self, strict: bool = False):
        self.strict = strict
        self.issues: list[dict] = []

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _is_meta(file_path: Path) -> bool:
        return file_path.name in META_EXCLUDE

    @staticmethod
    def _is_german(file_path: Path) -> bool:
        return any(m in str(file_path) for m in GERMAN_DIR_MARKERS)

    @staticmethod
    def _section_body(content: str, heading_re: str) -> str | None:
        """Return the text of the first matching section up to the next h1/h2."""
        m = re.search(heading_re, content, re.IGNORECASE | re.MULTILINE)
        if not m:
            return None
        start = m.start()
        rest = content[start:]
        nxt = re.search(r"^#{1,2}\s", rest[len(m.group(0)) :], re.MULTILINE)
        return rest[: len(m.group(0)) + nxt.start()] if nxt else rest

    def _issue(self, type_, message, file_path, line=None, severity="error", fixable=False):
        return {
            "line": line,
            "type": type_,
            "message": message,
            "file": file_path.name,
            "severity": severity,
            "fixable": fixable,
        }

    def _extract_tables(self, content: str) -> list[dict]:
        tables = []
        lines = content.split("\n")
        i = 0
        while i < len(lines):
            if "|" in lines[i]:
                next_is_sep = (
                    i + 1 < len(lines)
                    and "|" in lines[i + 1]
                    and re.match(r"^[\s\-\|:]+$", lines[i + 1])
                )
                if next_is_sep:
                    j = i + 2
                    while (
                        j < len(lines) and "|" in lines[j] and not lines[j].strip().startswith("#")
                    ):
                        j += 1
                    tables.append(
                        {
                            "line_start": i,
                            "header": lines[i],
                            "separator": lines[i + 1],
                            "line_end": j - 1,
                        }
                    )
                    i = j
                else:
                    i += 1
            else:
                i += 1
        return tables

    @staticmethod
    def _has_empty_first_cell(row: str) -> bool:
        stripped = row.strip()
        if not stripped.startswith("|"):
            return False
        cells = [c.strip() for c in stripped.split("|")]
        return len(cells) >= 2 and cells[1] == ""

    # ------------------------------------------------------------------
    # validation
    # ------------------------------------------------------------------

    def validate_file(self, file_path: Path) -> list[dict]:
        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")
        file_issues: list[dict] = []
        german = self._is_german(file_path)
        meta = self._is_meta(file_path)

        # --- heading hierarchy ---
        headings = []
        for i, line in enumerate(lines):
            match = re.match(r"^(#{1,6})\s+(.+)$", line)
            if match:
                headings.append((len(match.group(1)), i + 1, match.group(2).strip()))

        prev_level = 0
        for level, line_num, _text in headings:
            if level > prev_level + 1 and prev_level != 0 and level not in (1, 2):
                file_issues.append(
                    self._issue(
                        "heading_hierarchy",
                        f"Heading level {level} after {prev_level} "
                        "(progress gradually or reset to h1/h2)",
                        file_path,
                        line=line_num,
                        severity="warning",
                        fixable=True,
                    )
                )
            prev_level = level

        # --- tables: empty first cell ---
        for table in self._extract_tables(content):
            if self._has_empty_first_cell(table["header"]):
                file_issues.append(
                    self._issue(
                        "empty_first_cell",
                        "Table header has an empty first cell (use | Header |, not | | Header |)",
                        file_path,
                        line=table["line_start"] + 1,
                        severity="warning",
                        fixable=True,
                    )
                )
            for row_idx in range(table["line_start"] + 2, table["line_end"] + 1):
                row = lines[row_idx] if row_idx < len(lines) else ""
                if self._has_empty_first_cell(row):
                    file_issues.append(
                        self._issue(
                            "empty_first_cell",
                            "Table row has an empty first cell (remove the leading | | or fill it)",
                            file_path,
                            line=row_idx + 1,
                            severity="warning",
                            fixable=True,
                        )
                    )

        if meta:
            return file_issues

        # --- accessibility section ---
        heading_re = r"^#{1,2}\s*(Accessibility|Barrierefreiheit)\b"
        body = self._section_body(content, heading_re)
        if body is None:
            file_issues.append(
                self._issue(
                    "missing_accessibility_section",
                    f"Missing an Accessibility section "
                    f"('## {'Barrierefreiheit' if german else 'Accessibility'}')",
                    file_path,
                )
            )
            return file_issues

        if not KEYBOARD_HINTS.search(body):
            file_issues.append(
                self._issue(
                    "missing_keyboard_guidance",
                    "Accessibility section does not describe keyboard "
                    "navigation (Tab/Enter/Strg/... )",
                    file_path,
                )
            )

        if not ORIENTATION_HINTS.search(body):
            file_issues.append(
                self._issue(
                    "missing_orientation_hint",
                    "Accessibility section should offer an orientation "
                    "exit (Ctrl+Home / Strg+Pos1)",
                    file_path,
                    severity="warning",
                )
            )

        if not HIGH_CONTRAST.search(body):
            file_issues.append(
                self._issue(
                    "missing_high_contrast",
                    "Accessibility section should mention high contrast / dark mode support",
                    file_path,
                )
            )

        # --- forbidden tab chains (whole file, deduplicated by line) ---
        seen: set[tuple[int, str]] = set()
        for pattern in FORBIDDEN_TAB_CHAINS:
            for m in re.finditer(pattern, content, re.IGNORECASE):
                line = content[: m.start()].count("\n") + 1
                if (line, "forbidden_tab_chain") in seen:
                    continue
                seen.add((line, "forbidden_tab_chain"))
                file_issues.append(
                    self._issue(
                        "forbidden_tab_chain",
                        "Tab-for-tab path is forbidden; name the field "
                        "and say 'Tab (repeat as needed) until ...'",
                        file_path,
                        line=line,
                    )
                )

        # --- announcement predictions (whole file, deduplicated by line) ---
        for pattern in FORBIDDEN_ANNOUNCEMENTS:
            for m in re.finditer(pattern, content, re.IGNORECASE):
                line = content[: m.start()].count("\n") + 1
                if (line, "predicted_announcement") in seen:
                    continue
                seen.add((line, "predicted_announcement"))
                file_issues.append(
                    self._issue(
                        "predicted_announcement",
                        "Do not predict announcements; use 'You should "
                        "hear: …' (EN) / 'Sie hören: …' (DE)",
                        file_path,
                        line=line,
                    )
                )

        return file_issues

    # ------------------------------------------------------------------
    # auto-fix (heading hierarchy only; tables via scripts/fix_table_bugs.py)
    # ------------------------------------------------------------------

    def fix_file(self, file_path: Path) -> int:
        fixes = 0
        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        headings = []
        for i, line in enumerate(lines):
            match = re.match(r"^(#{1,6})\s+(.+)$", line)
            if match:
                headings.append((len(match.group(1)), i, match.group(2).strip()))

        prev_level = 0
        for level, line_idx, text in headings:
            if level > prev_level + 1 and prev_level != 0 and level not in (1, 2):
                corrected = prev_level + 1
                lines[line_idx] = f"{'#' * corrected} {text}"
                fixes += 1
            prev_level = level

        if fixes:
            file_path.write_text("\n".join(lines), encoding="utf-8")
        return fixes

    def fix_directory(self, directory: Path) -> int:
        total = 0
        for md_file in directory.glob("**/*.md"):
            if "node_modules" in md_file.parts:
                continue
            if md_file.name in META_EXCLUDE:
                continue
            fixes = self.fix_file(md_file)
            if fixes:
                print(f"  🔧 Fixed {fixes} issue(s) in {md_file.name}")
                total += fixes
        return total

    def validate_directory(self, directory: Path) -> list[dict]:
        all_issues = []
        for md_file in directory.glob("**/*.md"):
            if "node_modules" in md_file.parts:
                continue
            issues = self.validate_file(md_file)
            if issues:
                all_issues.extend(issues)
        return all_issues

    # ------------------------------------------------------------------
    # reporting
    # ------------------------------------------------------------------

    def errors(self, issues: list[dict]) -> list[dict]:
        return [i for i in issues if i["severity"] == "error"]

    def warnings(self, issues: list[dict]) -> list[dict]:
        return [i for i in issues if i["severity"] == "warning"]

    def print_report(self, issues: list[dict]) -> None:
        print("\n" + "=" * 70)
        print("ACCESSIBILITY VALIDATION REPORT")
        print("=" * 70)

        errs = self.errors(issues)
        warns = self.warnings(issues)

        if not issues:
            print("\n✅ All files passed accessibility checks!")
            print("=" * 70)
            return

        print(f"\nTotal issues found: {len(issues)} (errors: {len(errs)}, warnings: {len(warns)})")

        by_type: dict[str, int] = {}
        for issue in issues:
            by_type[issue["type"]] = by_type.get(issue["type"], 0) + 1

        print("\nIssues by type:")
        for type_name, count in sorted(by_type.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"  - {type_name.replace('_', ' ').title()}: {count}")

        print("\n" + "-" * 70)
        print("FILE-BY-FILE DETAIL")
        print("-" * 70 + "\n")

        by_file: dict[str, list[dict]] = {}
        for issue in issues:
            by_file.setdefault(issue["file"], []).append(issue)

        for filename, file_issues in sorted(by_file.items()):
            print(f"{filename}:")
            for issue in file_issues:
                loc = f" (line {issue['line']})" if issue.get("line") else ""
                icon = "❌ " if issue["severity"] == "error" else "⚠️  "
                print(f"  {icon}[{issue['type'].upper()}]{loc} {issue['message']}")
            print()

        print("=" * 70)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Validate markdown accessibility")
    parser.add_argument("directory", nargs="?", default="site/docs")
    parser.add_argument("--fix", action="store_true", help="Auto-fix heading hierarchy")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat advisory warnings as errors (non-zero exit)",
    )
    args = parser.parse_args()

    directory = Path(args.directory)
    if not directory.exists():
        print(f"Error: Directory '{directory}' not found.")
        sys.exit(1)

    validator = AccessibilityValidator(strict=args.strict)

    if args.fix:
        print(f"🔧 Auto-fixing accessibility issues in {directory}...\n")
        total = (
            validator.fix_file(directory)
            if directory.is_file()
            else validator.fix_directory(directory)
        )
        print(f"\n✅ Applied {total} fixes\n")

    print(f"Checking markdown in {directory}...\n")
    issues = (
        validator.validate_file(directory)
        if directory.is_file()
        else validator.validate_directory(directory)
    )
    validator.print_report(issues)

    blocking = issues if args.strict else validator.errors(issues)
    sys.exit(1 if blocking else 0)


if __name__ == "__main__":
    main()
