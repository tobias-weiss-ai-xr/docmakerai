import json
import tempfile
from pathlib import Path

from capture.capture_report import generate_capture_report, print_capture_report


def _make_results():
    return [
        ("calendar-create-event", True, 20, None),
        ("mail-read", False, 0, "blank capture"),
        ("contacts-add", True, 15, None),
        ("vacation", False, 0, "blank capture"),
        ("logout", True, 8, None),
    ]


def test_report_generation():
    results = _make_results()
    with tempfile.TemporaryDirectory() as tmp:
        output = Path(tmp) / "report.json"
        report = generate_capture_report(results, Path("/fake/assets"), output)

        assert report["total_workflows"] == 5
        assert report["succeeded"] == 3
        assert report["failed"] == 2
        assert report["success_rate"] == 60.0
        assert len(report["workflows"]) == 5

        assert output.exists()
        loaded = json.loads(output.read_text())
        assert loaded["total_workflows"] == 5


def test_report_failed_workflow_has_error():
    results = _make_results()
    report = generate_capture_report(results, Path("/fake/assets"))

    failed = [w for w in report["workflows"] if w["status"] == "failed"]
    assert len(failed) == 2
    assert failed[0]["error"] == "blank capture"


def test_report_print(capsys):
    results = _make_results()
    report = generate_capture_report(results, Path("/fake/assets"))
    print_capture_report(report)

    output = capsys.readouterr().out
    assert "3/5 succeeded" in output
    assert "60.0%" in output


def test_report_large_files_warning(tmp_path):
    """Large files over 200KB trigger a warning section."""
    large = tmp_path / "calendar-create-event.webp"
    large.write_bytes(b"x" * 300 * 1024)  # 300KB

    results = [("calendar-create-event", True, 20, None)]
    report = generate_capture_report(results, tmp_path)

    assert "warnings" in report
    assert "large_files" in report["warnings"]
    assert len(report["warnings"]["large_files"]) > 0


def test_report_no_large_files_warning(tmp_path):
    """Small files under 200KB produce no warnings."""
    results = [("test-ok", True, 0, None)]
    assets = tmp_path
    report = generate_capture_report(results, assets)
    assert "warnings" not in report or not report["warnings"].get("large_files")


def test_report_print_with_warnings(capsys, tmp_path):
    """Print report with large file warnings."""
    large = tmp_path / "calendar-create-event.webp"
    large.write_bytes(b"x" * 300 * 1024)  # 300KB

    results = [("calendar-create-event", True, 20, None)]
    report = generate_capture_report(results, tmp_path)
    print_capture_report(report)

    output = capsys.readouterr().out
    assert "Large files" in output


def test_report_output_path(tmp_path):
    """Report written to output_path matches returned dict."""
    results = [("logout", True, 8, None)]
    output = tmp_path / "reports" / "capture_report.json"
    report = generate_capture_report(results, Path("/fake/assets"), output)

    assert output.exists()
    import json
    loaded = json.loads(output.read_text())
    assert loaded["total_workflows"] == 1
    assert loaded == report
