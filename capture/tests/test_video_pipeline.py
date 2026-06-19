from pathlib import Path

from capture.video_pipeline import is_frame_valid, validate_frames


class TestIsFrameValid:
    def test_valid_frame(self, test_png: Path):
        assert is_frame_valid(test_png) is True

    def test_blank_frame(self, blank_png: Path):
        assert is_frame_valid(blank_png) is False

    def test_missing_file(self):
        assert is_frame_valid(Path("/nonexistent.png")) is False


class TestValidateFrames:
    def test_too_few_frames(self):
        valid, msg = validate_frames([], "test")
        assert valid is False
        assert "Too few frames" in msg

    def test_all_blank_rejected(self, blank_png: Path):
        frames = [blank_png] * 6
        valid, msg = validate_frames(frames, "test")
        assert valid is False

    def test_valid_frames_accepted(self, test_png: Path):
        frames = [test_png] * 6
        valid, msg = validate_frames(frames, "test")
        assert valid is True
