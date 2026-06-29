#!/usr/bin/env python3
"""Validate markdown files for accessibility compliance (WCAG 2.1 Level A)."""

import re
import sys
from pathlib import Path


class AccessibilityValidator:
    """Validates markdown files for accessibility compliance."""

    def __init__(self):
        self.issues: list[dict] = []

    def validate_file(self, file_path: Path) -> list[dict]:
        """Validate a single markdown file for accessibility issues."""
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        file_issues = []

        headings = []
        for i, line in enumerate(lines):
            match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if match:
                level = len(match.group(1))
                headings.append((level, i + 1, match.group(2).strip()))

        prev_level = 0
        for level, line_num, _text in headings:
            if level > prev_level + 1 and prev_level != 0 and level not in [1, 2]:
                file_issues.append({
                    'line': line_num,
                    'type': 'heading_hierarchy',
                    'message': (
                        f'Heading level {level} after {prev_level} '
                        f'(should progress gradually, or reset to h1/h2)'
                    ),
                    'file': file_path.name,
                    'fixable': True
                })
            prev_level = level

        tables = self._extract_tables(content)
        for table in tables:
            if not self._has_descriptive_table_headers(table['header']):
                file_issues.append({
                    'line': table['line_start'] + 1,
                    'type': 'table_header',
                    'message': (
                        'Table row missing proper header markers '
                        '(use | Header: description | for accessibility)'
                    ),
                    'file': file_path.name,
                    'fixable': True
                })

        prev_level = 0
        for level, line_num, _text in headings:
            if level > prev_level + 1 and prev_level != 0 and level not in [1, 2]:
                file_issues.append({
                    'line': line_num,
                    'type': 'heading_hierarchy',
                    'message': (
                        f'Heading level {level} after {prev_level} '
                        f'(should progress gradually, or reset to h1/h2)'
                    ),
                    'file': file_path.name,
                    'fixable': True
                })
            prev_level = level

        keyboard_section = re.search(
            r'#+.*(keyboard|shortcut|Keyboard|Shortcut).*navigation',
            content,
            re.IGNORECASE,
        )
        if not keyboard_section:
            file_issues.append({
                'line': None,
                'type': 'missing_keyboard_section',
                'message': (
                    'Missing "Accessibility: Keyboard Navigation" section '
                    'for screen reader/keyboard users'
                ),
                'file': file_path.name,
                'fixable': False
            })

        has_gif = bool(re.search(r'\.gif\)', content))
        has_screen_reader = re.search(r'#.*(screen.?reader).*workflow', content, re.IGNORECASE)
        if has_gif and not has_screen_reader:
            file_issues.append({
                'line': None,
                'type': 'missing_screen_reader',
                'message': 'GIF present but no "Screen Reader: [Topic]" workflow for blind users',
                'file': file_path.name,
                'fixable': False
            })

        accessibility_section = re.search(r'#+.*(accessibility|Accessibility)', content)
        if not accessibility_section:
            file_issues.append({
                'line': None,
                'type': 'missing_accessibility_section',
                'message': (
                    'Missing "Accessibility" section with keyboard shortcuts '
                    'and screen reader info'
                ),
                'file': file_path.name,
                'fixable': False
            })

        high_contrast = re.search(
            r'(high.?contrast|High.?Contrast|dark.?mode|Dark.?Mode)',
            content,
            re.IGNORECASE,
        )
        if accessibility_section and not high_contrast:
            file_issues.append({
                'line': None,
                'type': 'missing_high_contrast',
                'message': 'Accessibility section should mention high contrast/dark mode support',
                'file': file_path.name,
                'fixable': False
            })

        return file_issues

    def _extract_tables(self, content: str) -> list[dict]:
        """Extract all markdown tables from content."""
        tables = []
        lines = content.split('\n')
        i = 0

        while i < len(lines):
            if '|' in lines[i]:
                table_start = i
                header_row = lines[i]
                next_is_sep = (
                    i + 1 < len(lines)
                    and '|' in lines[i + 1]
                    and re.match(r'^[\s\-\|:]+$', lines[i + 1])
                )
                if next_is_sep:
                    separator_row = lines[i + 1]
                    j = i + 2
                    while (
                        j < len(lines)
                        and '|' in lines[j]
                        and not lines[j].strip().startswith('#')
                    ):
                        j += 1

                    tables.append({
                        'line_start': table_start,
                        'header': header_row,
                        'separator': separator_row,
                        'line_end': j - 1
                    })
                    i = j
                else:
                    i += 1
            else:
                i += 1

        return tables

    def _has_descriptive_table_headers(self, header_row: str) -> bool:
        """Check if table header has descriptive format with colons."""
        cells = [cell.strip() for cell in header_row.split('|') if cell.strip()]
        return any(':' in cell for cell in cells)

    def fix_file(self, file_path: Path) -> int:
        fixes = 0
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')

        headings = []
        for i, line in enumerate(lines):
            match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if match:
                level = len(match.group(1))
                headings.append((level, i, match.group(2).strip()))

        prev_level = 0
        for level, line_idx, text in headings:
            if level > prev_level + 1 and prev_level != 0 and level not in [1, 2]:
                corrected_level = prev_level + 1
                prefix = '#' * corrected_level
                lines[line_idx] = f"{prefix} {text}"
                fixes += 1
            prev_level = level

        for table in self._extract_tables('\n'.join(lines)):
            if not self._has_descriptive_table_headers(table['header']):
                cells = [cell.strip() for cell in table['header'].split('|') if cell.strip()]
                if cells:
                    first = cells[0]
                    rest = cells[1:]
                    fixed_first = f"{first}: Description"
                    new_header = '| ' + ' | '.join([fixed_first] + rest) + ' |'
                    lines[table['line_start']] = new_header
                    fixes += 1

        if fixes > 0:
            file_path.write_text('\n'.join(lines), encoding='utf-8')

        return fixes

    def fix_directory(self, directory: Path) -> int:
        total_fixes = 0
        for md_file in directory.glob('**/*.md'):
            if 'node_modules' in md_file.parts:
                continue
            if 'accessibility-section-template' in md_file.name:
                continue
            fixes = self.fix_file(md_file)
            if fixes:
                print(f"  🔧 Fixed {fixes} issue(s) in {md_file.name}")
                total_fixes += fixes
        return total_fixes

    def validate_directory(self, directory: Path) -> list[dict]:
        """Validate all markdown files in a directory."""
        all_issues = []
        md_files = directory.glob('**/*.md')

        for md_file in md_files:
            if 'node_modules' in md_file.parts:
                continue
            if 'accessibility-section-template' in md_file.name:
                continue

            issues = self.validate_file(md_file)
            if issues:
                all_issues.extend(issues)

        return all_issues

    def print_report(self, issues: list[dict]):
        """Print the validation report."""
        print("\n" + "=" * 70)
        print("ACCESSIBILITY VALIDATION REPORT")
        print("=" * 70)

        if not issues:
            print("\n✅ All files passed accessibility checks!")
            print("=" * 70)
            return

        print(f"\nTotal issues found: {len(issues)}")
        fixable = sum(1 for issue in issues if issue.get('fixable', False))
        print(f"Fixable issues: {fixable}\n")

        issue_types = {}
        for issue in issues:
            issue_type = issue['type']
            if issue_type not in issue_types:
                issue_types[issue_type] = 0
            issue_types[issue_type] += 1

        print("Issues by type:")
        for issue_type, count in sorted(issue_types.items()):
            type_name = issue_type.replace('_', ' ').title()
            print(f"  - {type_name}: {count}")

        print("\n" + "-" * 70)
        print("FILE-BY-FILE DETAIL")
        print("-" * 70 + "\n")

        by_file = {}
        for issue in issues:
            filename = issue['file']
            if filename not in by_file:
                by_file[filename] = []
            by_file[filename].append(issue)

        for filename, file_issues in sorted(by_file.items()):
            print(f"{filename}:")
            for issue in file_issues:
                line_info = f" (line {issue['line']})" if issue.get('line') else ""
                icon = "⚠️  " if issue.get('fixable', False) else "❌ "
                print(f"  {icon}[{issue['type'].upper()}]{line_info} {issue['message']}")
            print()

        print("=" * 70)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Validate markdown accessibility")
    parser.add_argument("directory", nargs="?", default="site/docs")
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-fix heading hierarchy and table headers",
    )
    parser.add_argument(
        "--check-only", action="store_true", help="Only check, no auto-fix (default)"
    )
    args = parser.parse_args()

    directory = Path(args.directory)
    if not directory.exists():
        print(f"Error: Directory '{directory}' not found.")
        sys.exit(1)

    validator = AccessibilityValidator()

    if args.fix:
        print(f"🔧 Auto-fixing accessibility issues in {directory}...\n")
        if directory.is_file():
            total_fixes = validator.fix_file(directory)
        else:
            total_fixes = validator.fix_directory(directory)
        print(f"\n✅ Applied {total_fixes} fixes")

    print(f"Checking markdown in {directory}...\n")
    if directory.is_file():
        issues = validator.validate_file(directory)
    else:
        issues = validator.validate_directory(directory)
    validator.print_report(issues)
    sys.exit(0 if not issues else 1)


if __name__ == '__main__':
    main()
