"""Tests for accessibility/validate.py — AccessibilityValidator class."""

import sys

import pytest

from accessibility.validate import AccessibilityValidator, main

# ---------------------------------------------------------------------------
# _extract_tables
# ---------------------------------------------------------------------------

class TestExtractTables:
    def test_single_table(self):
        content = (
            "| Header A | Header B |\n"
            "| -------- | -------- |\n"
            "| Cell 1   | Cell 2   |\n"
        )
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
        content = (
            "| Just a pipe line\n"
            "| Another pipe line\n"
        )
        validator = AccessibilityValidator()
        tables = validator._extract_tables(content)
        assert tables == []


# ---------------------------------------------------------------------------
# _has_descriptive_table_headers
# ---------------------------------------------------------------------------

class TestHasDescriptiveTableHeaders:
    def test_header_with_colon_returns_true(self):
        validator = AccessibilityValidator()
        assert validator._has_descriptive_table_headers("| Feature: desc | Status |") is True

    def test_header_without_colon_returns_false(self):
        validator = AccessibilityValidator()
        assert validator._has_descriptive_table_headers("| Feature | Status |") is False

    def test_empty_cells(self):
        """Empty cells are filtered out; no colon → False."""
        validator = AccessibilityValidator()
        assert validator._has_descriptive_table_headers("|  |  |") is False


# ---------------------------------------------------------------------------
# validate_file
# ---------------------------------------------------------------------------

class TestValidateFile:
    def test_proper_heading_hierarchy(self, tmp_path):
        md = tmp_path / "proper.md"
        md.write_text(
            "# Title\n"
            "## Section\n"
            "### Subsection\n"
            "Content here.\n"
        )
        validator = AccessibilityValidator()
        issues = validator.validate_file(md)
        heading_issues = [i for i in issues if i["type"] == "heading_hierarchy"]
        assert heading_issues == []

    def test_skipped_heading_level(self, tmp_path):
        md = tmp_path / "skip.md"
        md.write_text(
            "# Title\n"
            "### Skipped level\n"
        )
        validator = AccessibilityValidator()
        issues = validator.validate_file(md)
        # Duplicate hierarchy check adds TWO identical issues
        heading_issues = [i for i in issues if i["type"] == "heading_hierarchy"]
        assert len(heading_issues) == 2
        for iss in heading_issues:
            assert iss["fixable"] is True

    def test_proper_table_headers(self, tmp_path):
        md = tmp_path / "table_ok.md"
        md.write_text(
            "| Feature: desc | Status |\n"
            "| ------------- | ------ |\n"
            "| Login         | Done   |\n"
        )
        validator = AccessibilityValidator()
        issues = validator.validate_file(md)
        table_issues = [i for i in issues if i["type"] == "table_header"]
        assert table_issues == []

    def test_table_missing_descriptive_headers(self, tmp_path):
        md = tmp_path / "table_bad.md"
        md.write_text(
            "| Feature | Status |\n"
            "| ------- | ------ |\n"
            "| Login   | Done   |\n"
        )
        validator = AccessibilityValidator()
        issues = validator.validate_file(md)
        table_issues = [i for i in issues if i["type"] == "table_header"]
        assert len(table_issues) == 1
        assert table_issues[0]["fixable"] is True

    def test_keyboard_navigation_section_present(self, tmp_path):
        md = tmp_path / "has_kb.md"
        md.write_text(
            "# Keyboard Navigation\n"
            "Use Tab to navigate.\n"
        )
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
            "![animation](demo.gif)\n"
            "\n"
            "## Screen Reader: Workflow\n"
            "Description for blind users.\n"
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
        md.write_text(
            "## Accessibility\n"
            "Supports high contrast mode.\n"
        )
        validator = AccessibilityValidator()
        issues = validator.validate_file(md)
        hc_issues = [i for i in issues if i["type"] == "missing_high_contrast"]
        assert hc_issues == []

    def test_accessibility_without_high_contrast(self, tmp_path):
        md = tmp_path / "hc_bad.md"
        md.write_text(
            "## Accessibility\n"
            "Some info here.\n"
        )
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
        md.write_text(
            "# Title\n"
            "### Skipped\n"
        )
        validator = AccessibilityValidator()
        fixes = validator.fix_file(md)
        assert fixes == 1
        content = md.read_text()
        assert "## Skipped" in content

    def test_fixes_table_headers(self, tmp_path):
        md = tmp_path / "fix_table.md"
        md.write_text(
            "| Feature | Status |\n"
            "| ------- | ------ |\n"
            "| Login   | Done   |\n"
        )
        validator = AccessibilityValidator()
        fixes = validator.fix_file(md)
        assert fixes == 1
        content = md.read_text()
        assert "Feature: Description" in content

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
        assert total == 2  # 1 heading fix + 1 table fix
        assert "## Bad heading" in a.read_text()
        assert "X: Description" in b.read_text()

    def test_skips_template_files(self, tmp_path):
        (tmp_path / "accessibility-section-template.md").write_text("### Bad\n")
        (tmp_path / "real.md").write_text("| X | Y |\n| - | - |\n| 1 | 2 |\n")
        validator = AccessibilityValidator()
        total = validator.fix_directory(tmp_path)
        # Only real.md gets fixed (1 table), template is skipped
        assert total == 1


# ---------------------------------------------------------------------------
# validate_directory
# ---------------------------------------------------------------------------

class TestValidateDirectory:
    def test_validates_all_md_files(self, tmp_path):
        a = tmp_path / "a.md"
        a.write_text("# Ok\n")
        b = tmp_path / "b.md"
        b.write_text("| X | Y |\n| - | - |\n| 1 | 2 |\n")
        validator = AccessibilityValidator()
        issues = validator.validate_directory(tmp_path)
        assert len(issues) >= 1  # b has missing keyboard + table + accessibility issues

    def test_skips_template_files(self, tmp_path):
        (tmp_path / "accessibility-section-template.md").write_text("| X |\n| - |\n| 1 |\n")
        (tmp_path / "real.md").write_text("# Real\n")
        validator = AccessibilityValidator()
        issues = validator.validate_directory(tmp_path)
        files = {i["file"] for i in issues}
        assert "real.md" in files
        assert "accessibility-section-template.md" not in files


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
            {"line": 3, "type": "heading_hierarchy", "message": "Bad heading", "file": "test.md",
             "fixable": True},
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
