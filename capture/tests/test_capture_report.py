import json
import tempfile
from pathlib import Path

from capture.capture_report import generate_capture_report, print_capture_report


def _make_results():
    return [
        ("calendar-create-event", True, 20, None, 12.5),
        ("mail-read", False, 0, "blank capture", 8.3),
        ("contacts-add", True, 15, None, 6.7),
        ("vacation", False, 0, "blank capture", 4.2),
        ("logout", True, 8, None, 3.1),
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
    large = tmp_path / "calendar-create-event.webp"
    large.write_bytes(b"x" * 300 * 1024)

    results = [("calendar-create-event", True, 20, None, 5.0)]
    report = generate_capture_report(results, tmp_path)

    assert "warnings" in report
    assert "large_files" in report["warnings"]
    assert len(report["warnings"]["large_files"]) > 0


def test_report_no_large_files_warning(tmp_path):
    results = [("test-ok", True, 0, None, 1.0)]
    assets = tmp_path
    report = generate_capture_report(results, assets)
    assert "warnings" not in report or not report["warnings"].get("large_files")


def test_report_print_with_warnings(capsys, tmp_path):
    large = tmp_path / "calendar-create-event.webp"
    large.write_bytes(b"x" * 300 * 1024)

    results = [("calendar-create-event", True, 20, None, 5.0)]
    report = generate_capture_report(results, tmp_path)
    print_capture_report(report)

    output = capsys.readouterr().out
    assert "Large files" in output


def test_report_output_path(tmp_path):
    results = [("logout", True, 8, None, 2.0)]
    output = tmp_path / "reports" / "capture_report.json"
    report = generate_capture_report(results, Path("/fake/assets"), output)

    assert output.exists()
    loaded = json.loads(output.read_text())
    assert loaded["total_workflows"] == 1
    assert loaded == report


def test_report_includes_total_duration():
    results = _make_results()
    report = generate_capture_report(results, Path("/fake/assets"))

    assert "total_duration_seconds" in report
    expected = round(12.5 + 8.3 + 6.7 + 4.2 + 3.1, 2)
    assert report["total_duration_seconds"] == expected


def test_report_workflow_entry_has_duration():
    results = _make_results()
    report = generate_capture_report(results, Path("/fake/assets"))

    for entry in report["workflows"]:
        assert "duration_seconds" in entry
    first = report["workflows"][0]
    assert first["duration_seconds"] == 12.5


def test_report_slowest_workflow():
    results = _make_results()
    report = generate_capture_report(results, Path("/fake/assets"))

    assert report["slowest_workflow"] == "calendar-create-event"
    assert report["slowest_duration_seconds"] == 12.5


def test_report_generated_at_timestamp():
    results = _make_results()
    report = generate_capture_report(results, Path("/fake/assets"))

    assert "generated_at" in report
    import re

    assert re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", report["generated_at"])


def test_report_zero_duration_when_all_instant():
    results = [
        ("a", True, 5, None, 0.0),
        ("b", True, 3, None, 0.0),
    ]
    report = generate_capture_report(results, Path("/fake/assets"))
    assert report["total_duration_seconds"] == 0.0
    assert report["slowest_workflow"] == "a"
    assert report["slowest_duration_seconds"] == 0.0
