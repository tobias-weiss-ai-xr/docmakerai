import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from capture.detect_changes import (
    compute_phash,
    save_baseline,
    load_baseline,
    hamming_distance,
    detect_drift,
    DEFAULT_THRESHOLD,
)


def _make_test_image(color: tuple[int, int, int] = (255, 255, 255), size: tuple[int, int] = (256, 128)) -> Path:

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        path = Path(f.name)
    Image.new("RGB", size, color).save(path)
    return path


class TestComputePhash(unittest.TestCase):
    def test_returns_hex_string_of_expected_length(self):
        img = _make_test_image()
        try:
            h = compute_phash(img)
            self.assertIsInstance(h, str)
            # 64-bit hash = 16 hex chars
            self.assertEqual(len(h), 16)
            int(h, 16)  # raises if not valid hex
        finally:
            img.unlink()

    def test_same_image_produces_same_hash(self):
        a = _make_test_image((100, 150, 200))
        b = _make_test_image((100, 150, 200))
        try:
            self.assertEqual(compute_phash(a), compute_phash(b))
        finally:
            a.unlink()
            b.unlink()

    def test_different_image_produces_different_hash(self):
        a = _make_test_image((0, 0, 0))
        b = _make_test_image((255, 255, 255))
        try:
            self.assertNotEqual(compute_phash(a), compute_phash(b))
        finally:
            a.unlink()
            b.unlink()


class TestHammingDistance(unittest.TestCase):
    def test_identical_hashes_have_zero_distance(self):
        self.assertEqual(hamming_distance("0000000000000000", "0000000000000000"), 0)

    def test_single_bit_difference(self):
        self.assertEqual(hamming_distance("0000000000000000", "0000000000000001"), 1)

    def test_max_distance(self):
        self.assertEqual(hamming_distance("0000000000000000", "ffffffffffffffff"), 64)


class TestBaselineRoundTrip(unittest.TestCase):
    def test_save_then_load_returns_same_hash(self):
        img = _make_test_image()
        try:
            h = compute_phash(img)
            with tempfile.TemporaryDirectory() as tmp:
                baselines = Path(tmp)
                save_baseline("test-wf", h, baselines)
                loaded = load_baseline("test-wf", baselines)
                self.assertEqual(loaded, h)
        finally:
            img.unlink()

    def test_load_missing_baseline_returns_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(load_baseline("nonexistent", Path(tmp)))

    def test_baseline_file_format(self):
        with tempfile.TemporaryDirectory() as tmp:
            baselines = Path(tmp)
            save_baseline("myworkflow", "abcd1234abcd1234", baselines)
            f = baselines / "myworkflow.phash.json"
            self.assertTrue(f.exists())
            data = json.loads(f.read_text())
            self.assertEqual(data["workflow"], "myworkflow")
            self.assertEqual(data["phash"], "abcd1234abcd1234")
            self.assertIn("saved_at", data)


class TestDetectDrift(unittest.TestCase):
    def test_no_drift_when_hashes_match(self):
        with tempfile.TemporaryDirectory() as tmp:
            baselines = Path(tmp)
            save_baseline("wf", "0000000000000000", baselines)
            drift, dist = detect_drift("wf", "0000000000000000", baselines)
            self.assertFalse(drift)
            self.assertEqual(dist, 0)

    def test_drift_when_distance_exceeds_threshold(self):
        with tempfile.TemporaryDirectory() as tmp:
            baselines = Path(tmp)
            save_baseline("wf", "0000000000000000", baselines)
            # 20 bits different, default threshold is 10
            drifted = "00000000000fffff"  # 20 bits set
            drift, dist = detect_drift("wf", drifted, baselines)
            self.assertTrue(drift)
            self.assertEqual(dist, 20)

    def test_no_drift_below_threshold(self):
        with tempfile.TemporaryDirectory() as tmp:
            baselines = Path(tmp)
            save_baseline("wf", "0000000000000000", baselines)
            # 5 bits different, threshold 10
            drifted = "000000000000001f"  # 5 bits set
            drift, dist = detect_drift("wf", drifted, baselines, threshold=10)
            self.assertFalse(drift)
            self.assertEqual(dist, 5)

    def test_drift_when_no_baseline_exists_returns_true(self):
        with tempfile.TemporaryDirectory() as tmp:
            drift, dist = detect_drift("new-wf", "0000000000000000", Path(tmp))
            self.assertTrue(drift)
            self.assertIsNone(dist)


if __name__ == "__main__":
    unittest.main()
