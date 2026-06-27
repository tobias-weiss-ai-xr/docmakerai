import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent.parent / "check_coverage_trend.py"


class TestCoverageTrend(unittest.TestCase):
    def test_passes_when_pr_coverage_equals_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "baseline.xml").write_text(_cov_xml(99.0))
            (tmp / "pr.xml").write_text(_cov_xml(99.0))
            result = subprocess.run(
                [sys.executable, str(SCRIPT),
                 "--baseline", str(tmp / "baseline.xml"),
                 "--pr", str(tmp / "pr.xml"),
                 "--max-drop", "0.5"],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_fails_when_pr_coverage_drops_more_than_threshold(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "baseline.xml").write_text(_cov_xml(99.0))
            (tmp / "pr.xml").write_text(_cov_xml(95.0))
            result = subprocess.run(
                [sys.executable, str(SCRIPT),
                 "--baseline", str(tmp / "baseline.xml"),
                 "--pr", str(tmp / "pr.xml"),
                 "--max-drop", "0.5"],
                capture_output=True, text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("dropped", result.stderr.lower())

    def test_passes_when_pr_coverage_improves(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "baseline.xml").write_text(_cov_xml(95.0))
            (tmp / "pr.xml").write_text(_cov_xml(99.5))
            result = subprocess.run(
                [sys.executable, str(SCRIPT),
                 "--baseline", str(tmp / "baseline.xml"),
                 "--pr", str(tmp / "pr.xml"),
                 "--max-drop", "0.5"],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, msg=result.stderr)


def _cov_xml(percent: float) -> str:
    rate = percent / 100.0
    return f"""<?xml version="1.0" ?>
<coverage line-rate="{rate}" branch-rate="{rate}" version="7.0">
  <sources><source>.</source></sources>
</coverage>
"""


if __name__ == "__main__":
    unittest.main()
