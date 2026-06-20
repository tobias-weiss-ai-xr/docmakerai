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
