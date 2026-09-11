"""Tests for accessibility/validate.py — AccessibilityValidator class."""

import sys

import pytest

from accessibility.validate import AccessibilityValidator, main

# ---------------------------------------------------------------------------
# _extract_tables
# ---------------------------------------------------------------------------


class TestExtractTables:
    def test_single_table(self):
        content = "| Header A | Header B |\n| -------- | -------- |\n| Cell 1   | Cell 2   |\n"
        validator = AccessibilityValidator()
        tables = validator._extract_tables(content)
        assert len(tables) == 1
        assert "Header A" in tables[0]["header"]
        assert tables[0]["line_start"] == 0
        assert tables[0]["line_end"] == 2

    def test_multiple_tables_with_text_between(self):
        content = (
            "| H1 | H2 |\n"
            "| -- | -- |\n"
            "| a  | b  |\n"
            "\n"
            "Some text in between\n"
            "\n"
            "| C1 | C2 |\n"
            "| -- | -- |\n"
            "| x  | y  |\n"
        )
        validator = AccessibilityValidator()
        tables = validator._extract_tables(content)
        assert len(tables) == 2

    def test_no_tables(self):
        content = "Just some text.\n\nNo tables here."
        validator = AccessibilityValidator()
        tables = validator._extract_tables(content)
        assert tables == []

    def test_malformed_table_pipe_no_separator(self):
        """Line with pipe but no valid separator row → not a table."""
        content = "| Just a pipe line\n| Another pipe line\n"
        validator = AccessibilityValidator()
        tables = validator._extract_tables(content)
        assert tables == []


# ---------------------------------------------------------------------------
# _has_empty_first_cell
# ---------------------------------------------------------------------------


class TestHasEmptyFirstCell:
    def test_empty_first_cell_returns_true(self):
        validator = AccessibilityValidator()
        assert validator._has_empty_first_cell("| | Feature | Status |") is True

    def test_normal_header_returns_false(self):
        validator = AccessibilityValidator()
        assert validator._has_empty_first_cell("| Feature | Status |") is False

    def test_no_pipe_prefix_returns_false(self):
        validator = AccessibilityValidator()
        assert validator._has_empty_first_cell("Feature | Status") is False

    def test_empty_row(self):
        """Fully empty row still counts as empty first cell."""
        validator = AccessibilityValidator()
        assert validator._has_empty_first_cell("| | |") is True


# ---------------------------------------------------------------------------
# validate_file
# ---------------------------------------------------------------------------


class TestValidateFile:
    def test_proper_heading_hierarchy(self, tmp_path):
        md = tmp_path / "proper.md"
        md.write_text("# Title\n## Section\n### Subsection\nContent here.\n")
        validator = AccessibilityValidator()
        issues = validator.validate_file(md)
        heading_issues = [i for i in issues if i["type"] == "heading_hierarchy"]
        assert heading_issues == []

    def test_skipped_heading_level(self, tmp_path):
        md = tmp_path / "skip.md"
        md.write_text("# Title\n### Skipped level\n")
        validator = AccessibilityValidator()
        issues = validator.validate_file(md)
        heading_issues = [i for i in issues if i["type"] == "heading_hierarchy"]
        assert len(heading_issues) == 1
        for iss in heading_issues:
            assert iss["fixable"] is True

    def test_proper_table_headers(self, tmp_path):
        md = tmp_path / "table_ok.md"
        md.write_text("| Feature | Status |\n| ------- | ------ |\n| Login   | Done   |\n")
        validator = AccessibilityValidator()
        issues = validator.validate_file(md)
        table_issues = [i for i in issues if i["type"] == "empty_first_cell"]
        assert table_issues == []

    def test_table_with_empty_first_cell(self, tmp_path):
        md = tmp_path / "table_bad.md"
        md.write_text("| Feature | Status |\n| ------- | ------ |\n|        | Done   |\n")
        validator = AccessibilityValidator()
        issues = validator.validate_file(md)
        table_issues = [i for i in issues if i["type"] == "empty_first_cell"]
        assert len(table_issues) == 1
        assert table_issues[0]["fixable"] is True

    def test_table_header_with_empty_first_cell(self, tmp_path):
        """| | Header | in the HEADER row is reported (distinct from data rows)."""
        md = tmp_path / "table_hdr_bad.md"
        md.write_text("| | Feature | Status |\n| ------- | ------ | ------ |\n| 1 | a | b |\n")
        validator = AccessibilityValidator()
        issues = validator.validate_file(md)
        table_issues = [i for i in issues if i["type"] == "empty_first_cell"]
        assert len(table_issues) == 1
        assert "header" in table_issues[0]["message"].lower()

    def test_keyboard_navigation_section_present(self, tmp_path):
        md = tmp_path / "has_kb.md"
        md.write_text("# Keyboard Navigation\nUse Tab to navigate.\n")
        validator = AccessibilityValidator()
        issues = validator.validate_file(md)
        kb_issues = [i for i in issues if i["type"] == "missing_keyboard_section"]
        assert kb_issues == []

    def test_missing_keyboard_section(self, tmp_path):
        md = tmp_path / "no_kb.md"
        md.write_text("# Just a title\n")
        validator = AccessibilityValidator()
        issues = validator.validate_file(md)
        kb_issues = [i for i in issues if i["type"] == "missing_keyboard_section"]
        assert len(kb_issues) == 1
        assert kb_issues[0]["fixable"] is False

    def test_gif_with_screen_reader_section(self, tmp_path):
        md = tmp_path / "gif_ok.md"
        md.write_text(
            "![animation](demo.gif)\n\n## Screen Reader: Workflow\nDescription for blind users.\n"
        )
        validator = AccessibilityValidator()
        issues = validator.validate_file(md)
        sr_issues = [i for i in issues if i["type"] == "missing_screen_reader"]
        assert sr_issues == []

    def test_gif_without_screen_reader(self, tmp_path):
        md = tmp_path / "gif_bad.md"
        md.write_text("![demo](demo.gif)\n")
        validator = AccessibilityValidator()
        issues = validator.validate_file(md)
        sr_issues = [i for i in issues if i["type"] == "missing_screen_reader"]
        assert len(sr_issues) == 1
        assert sr_issues[0]["fixable"] is False

    def test_accessibility_with_high_contrast_mention(self, tmp_path):
        md = tmp_path / "hc_ok.md"
        md.write_text("## Accessibility\nSupports high contrast mode.\n")
        validator = AccessibilityValidator()
        issues = validator.validate_file(md)
        hc_issues = [i for i in issues if i["type"] == "missing_high_contrast"]
        assert hc_issues == []

    def test_accessibility_without_high_contrast(self, tmp_path):
        md = tmp_path / "hc_bad.md"
        md.write_text("## Accessibility\nSome info here.\n")
        validator = AccessibilityValidator()
        issues = validator.validate_file(md)
        hc_issues = [i for i in issues if i["type"] == "missing_high_contrast"]
        assert len(hc_issues) == 1
        assert hc_issues[0]["fixable"] is False

    def test_empty_markdown_file(self, tmp_path):
        md = tmp_path / "empty.md"
        md.write_text("")
        validator = AccessibilityValidator()
        issues = validator.validate_file(md)
        types = {i["type"] for i in issues}
        assert "missing_keyboard_section" in types
        assert "missing_accessibility_section" in types


# ---------------------------------------------------------------------------
# fix_file
# ---------------------------------------------------------------------------


class TestFixFile:
    def test_fixes_heading_hierarchy(self, tmp_path):
        md = tmp_path / "fix_heading.md"
        md.write_text("# Title\n### Skipped\n")
        validator = AccessibilityValidator()
        fixes = validator.fix_file(md)
        assert fixes == 1
        content = md.read_text()
        assert "## Skipped" in content

    def test_no_table_auto_fix(self, tmp_path):
        """fix_file no longer mangles table headers with ': Description'."""
        md = tmp_path / "fix_table.md"
        md.write_text("| Feature | Status |\n| ------- | ------ |\n| Login   | Done   |\n")
        validator = AccessibilityValidator()
        fixes = validator.fix_file(md)
        assert fixes == 0
        content = md.read_text()
        assert "Feature: Description" not in content
        assert "| Feature | Status |" in content

    def test_no_modifications_when_no_issues(self, tmp_path):
        md = tmp_path / "clean.md"
        content = "# Clean\n\nNo issues here.\n"
        md.write_text(content)
        validator = AccessibilityValidator()
        fixes = validator.fix_file(md)
        assert fixes == 0
        assert md.read_text() == content


# ---------------------------------------------------------------------------
# fix_directory
# ---------------------------------------------------------------------------


class TestFixDirectory:
    def test_fixes_multiple_files(self, tmp_path):
        a = tmp_path / "a.md"
        a.write_text("# Title\n### Bad heading\n")
        b = tmp_path / "b.md"
        b.write_text("| X | Y |\n| - | - |\n| 1 | 2 |\n")
        validator = AccessibilityValidator()
        total = validator.fix_directory(tmp_path)
        assert total == 1  # only the heading fix; table headers are not auto-fixed
        assert "## Bad heading" in a.read_text()
        assert "X: Description" not in b.read_text()

    def test_skips_node_modules(self, tmp_path):
        (tmp_path / "node_modules").mkdir()
        (tmp_path / "node_modules" / "bad.md").write_text("# Title\n### Skipped\n")
        validator = AccessibilityValidator()
        assert validator.fix_directory(tmp_path) == 0

    def test_skips_template_files(self, tmp_path):
        (tmp_path / "accessibility-section-template.md").write_text("### Bad\n")
        (tmp_path / "real.md").write_text("| X | Y |\n| - | - |\n| 1 | 2 |\n")
        validator = AccessibilityValidator()
        total = validator.fix_directory(tmp_path)
        # Only real.md's heading would be fixed; template is skipped. Table is untouched.
        assert total == 0


# ---------------------------------------------------------------------------
# validate_directory
# ---------------------------------------------------------------------------


class TestValidateDirectory:
    def test_validates_all_md_files(self, tmp_path):
        a = tmp_path / "a.md"
        a.write_text("# Ok\n")
        b = tmp_path / "b.md"
        b.write_text("| X | Y |\n| - | - |\n| | 2 |\n")
        validator = AccessibilityValidator()
        issues = validator.validate_directory(tmp_path)
        empty_cell = [i for i in issues if i["type"] == "empty_first_cell"]
        assert len(empty_cell) >= 1  # b has an empty-first-cell row

    def test_skips_template_files(self, tmp_path):
        (tmp_path / "accessibility-section-template.md").write_text("| X |\n| - |\n| 1 |\n")
        (tmp_path / "real.md").write_text("# Real\n")
        validator = AccessibilityValidator()
        issues = validator.validate_directory(tmp_path)
        files = {i["file"] for i in issues}
        assert "real.md" in files
        assert "accessibility-section-template.md" not in files

    def test_skips_node_modules(self, tmp_path):
        (tmp_path / "node_modules").mkdir()
        (tmp_path / "node_modules" / "x.md").write_text("| X |\n| - |\n| | 2 |\n")
        validator = AccessibilityValidator()
        assert validator.validate_directory(tmp_path) == []


# ---------------------------------------------------------------------------
# print_report
# ---------------------------------------------------------------------------


class TestPrintReport:
    def test_no_issues(self, capsys):
        validator = AccessibilityValidator()
        validator.print_report([])
        captured = capsys.readouterr()
        assert "All files passed" in captured.out

    def test_with_issues(self, capsys):
        validator = AccessibilityValidator()
        issues = [
            {
                "line": 3,
                "type": "heading_hierarchy",
                "message": "Bad heading",
                "file": "test.md",
                "fixable": True,
            },
            {
                "line": None,
                "type": "missing_keyboard_section",
                "message": "No KB",
                "file": "test.md",
                "fixable": False,
            },
        ]
        validator.print_report(issues)
        captured = capsys.readouterr()
        assert "Total issues found: 2" in captured.out
        assert "Heading Hierarchy" in captured.out
        assert "Missing Keyboard Section" in captured.out
        assert "test.md" in captured.out
        assert "HEADING_HIERARCHY" in captured.out
        assert "MISSING_KEYBOARD_SECTION" in captured.out


# ---------------------------------------------------------------------------
# main — argparse behavior
# ---------------------------------------------------------------------------


class TestMain:
    def test_default_arguments(self, tmp_path, monkeypatch):
        docs = tmp_path / "site" / "docs"
        docs.mkdir(parents=True)
        (docs / "test.md").write_text("# Hello\n")
        monkeypatch.setattr(sys, "argv", ["validate.py", str(docs)])
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 1

    def test_with_fix_flag(self, tmp_path, monkeypatch):
        docs = tmp_path / "site" / "docs"
        docs.mkdir(parents=True)
        (docs / "test.md").write_text("### Bad\n")
        monkeypatch.setattr(sys, "argv", ["validate.py", str(docs), "--fix"])
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 1
        content = (docs / "test.md").read_text()
        assert "## Bad" in content

    def test_non_existent_directory(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["validate.py", "/nonexistent/path"])
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 1

    def test_validate_single_file(self, tmp_path, monkeypatch):
        """CLI accepts a single markdown file, not just directories."""
        md = tmp_path / "one.md"
        md.write_text(
            "# Keyboard Navigation\nUse Tab to navigate.\n\n## Accessibility\n\n"
            "Use Tab and keyboard shortcuts. For GIFs, screen reader text is provided. "
            "High contrast mode is supported.\n"
        )
        monkeypatch.setattr(sys, "argv", ["validate.py", str(md)])
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 0  # clean file

    def test_fix_single_file(self, tmp_path, monkeypatch):
        """--fix works on a single markdown file."""
        md = tmp_path / "one.md"
        md.write_text("# Title\n### Skipped\n")
        monkeypatch.setattr(sys, "argv", ["validate.py", str(md), "--fix"])
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 1  # keyboard section still missing
        assert "## Skipped" in md.read_text()

    def test_main_module_exit_code(self, tmp_path):
        """python -m accessibility.validate <clean file> exits 0 via __main__."""
        import subprocess

        md = tmp_path / "clean.md"
        md.write_text(
            "# Keyboard Navigation\nUse Tab to navigate.\n\n## Accessibility\n\n"
            "Use Tab and keyboard shortcuts. For GIFs, screen reader text is provided. "
            "High contrast mode is supported.\n"
        )
        result = subprocess.run(
            [sys.executable, "-m", "accessibility.validate", str(md)],
            capture_output=True,
            cwd=".",
        )
        assert result.returncode == 0
