import json
from pathlib import Path
from unittest.mock import patch

from PIL import Image, ImageFont

from capture.annotate import _load_font, _save_animation, build_segment_animation


class TestLoadFont:
    def test_default_fallback_on_ioerror(self):
        default_font = ImageFont.ImageFont()
        with (
            patch("capture.annotate.ImageFont.truetype", side_effect=IOError),
            patch("capture.annotate.ImageFont.load_default", return_value=default_font),
        ):
            font = _load_font(22)
            assert isinstance(font, ImageFont.ImageFont)

    def test_default_fallback_on_oserror(self):
        default_font = ImageFont.ImageFont()
        with (
            patch("capture.annotate.ImageFont.truetype", side_effect=OSError),
            patch("capture.annotate.ImageFont.load_default", return_value=default_font),
        ):
            font = _load_font(22)
            assert isinstance(font, ImageFont.ImageFont)

    def test_loads_truetype_when_available(self):
        font = _load_font(22)
        assert font is not None


class TestSaveAnimation:
    def test_saves_gif_with_frames(self, tmp_path):
        frames = [
            Image.new("RGB", (10, 10), (255, 0, 0)),
            Image.new("RGB", (10, 10), (0, 255, 0)),
        ]
        out = tmp_path / "out.gif"
        result = _save_animation(frames, [500, 500], out, fmt="GIF")
        assert result is True
        assert out.exists()
        assert out.stat().st_size > 0

    def test_saves_webp_with_frames(self, tmp_path):
        frames = [
            Image.new("RGB", (10, 10), (255, 0, 0)),
            Image.new("RGB", (10, 10), (0, 255, 0)),
        ]
        out = tmp_path / "out.webp"
        result = _save_animation(frames, [500, 500], out, fmt="WEBP")
        assert result is True
        assert out.exists()
        assert out.stat().st_size > 0

    def test_single_frame_saves_successfully(self, tmp_path):
        frames = [Image.new("RGB", (10, 10), (255, 0, 0))]
        out = tmp_path / "single.webp"
        result = _save_animation(frames, [500], out, fmt="WEBP")
        assert result is True
        assert out.exists()

    def test_exception_returns_false(self, tmp_path):
        frames = [
            Image.new("RGB", (10, 10), (255, 0, 0)),
            Image.new("RGB", (10, 10), (0, 255, 0)),
        ]
        out = Path("/nonexistent_dir_12345_xyz/output.gif")
        result = _save_animation(frames, [500, 500], out, fmt="GIF")
        assert result is False


class TestBuildSegmentAnimationExtended:
    def test_with_valid_frames_returns_true(self, tmp_path, test_png, blank_png):
        frames_dir = tmp_path / "frames"
        frames_dir.mkdir()
        frame1 = frames_dir / "frame1.png"
        frame2 = frames_dir / "frame2.png"
        frame1.write_bytes(test_png.read_bytes())
        frame2.write_bytes(blank_png.read_bytes())

        meta = tmp_path / "frames.json"
        meta.write_text(
            json.dumps(
                [
                    {"file": "frame1.png", "step": "First", "duration": 500, "highlights": []},
                    {"file": "frame2.png", "step": "Second", "duration": 500, "highlights": []},
                ]
            )
        )

        out = tmp_path / "out.webp"
        result = build_segment_animation(frames_dir, meta, out, locale="en", fmt="WEBP")
        assert result is True
        assert out.exists()
        assert out.stat().st_size > 0

    def test_missing_metadata_file_returns_false(self, tmp_path):
        out = tmp_path / "out.webp"
        meta = tmp_path / "nonexistent.json"
        result = build_segment_animation(tmp_path, meta, out)
        assert result is False

    def test_empty_metadata_list_returns_false(self, tmp_path):
        out = tmp_path / "out.webp"
        meta = tmp_path / "frames.json"
        meta.write_text(json.dumps([]))
        result = build_segment_animation(tmp_path, meta, out)
        assert result is False

    def test_one_missing_frame_returns_false(self, tmp_path, test_png):
        frames_dir = tmp_path / "frames"
        frames_dir.mkdir()
        frame1 = frames_dir / "frame1.png"
        frame1.write_bytes(test_png.read_bytes())

        meta = tmp_path / "frames.json"
        meta.write_text(
            json.dumps(
                [
                    {"file": "frame1.png", "step": "First", "duration": 500, "highlights": []},
                    {"file": "frame2.png", "step": "Second", "duration": 500, "highlights": []},
                ]
            )
        )

        out = tmp_path / "out.webp"
        result = build_segment_animation(frames_dir, meta, out)
        assert result is False

    def test_corrupt_frame_returns_false(self, tmp_path, test_png):
        frames_dir = tmp_path / "frames"
        frames_dir.mkdir()
        frame1 = frames_dir / "frame1.png"
        frame1.write_bytes(test_png.read_bytes())
        frame2 = frames_dir / "frame2.png"
        frame2.write_bytes(b"not a real png file at all")

        meta = tmp_path / "frames.json"
        meta.write_text(
            json.dumps(
                [
                    {"file": "frame1.png", "step": "First", "duration": 500, "highlights": []},
                    {"file": "frame2.png", "step": "Second", "duration": 500, "highlights": []},
                ]
            )
        )

        out = tmp_path / "out.webp"
        result = build_segment_animation(frames_dir, meta, out)
        assert result is False

    def test_gif_format_output(self, tmp_path, test_png, blank_png):
        frames_dir = tmp_path / "frames"
        frames_dir.mkdir()
        frame1 = frames_dir / "frame1.png"
        frame2 = frames_dir / "frame2.png"
        frame1.write_bytes(test_png.read_bytes())
        frame2.write_bytes(blank_png.read_bytes())

        meta = tmp_path / "frames.json"
        meta.write_text(
            json.dumps(
                [
                    {"file": "frame1.png", "step": "First", "duration": 500, "highlights": []},
                    {"file": "frame2.png", "step": "Second", "duration": 500, "highlights": []},
                ]
            )
        )

        out = tmp_path / "out.gif"
        result = build_segment_animation(frames_dir, meta, out, fmt="GIF")
        assert result is True
        assert out.exists()
        assert out.stat().st_size > 0

    def test_annotated_pngs_saved_to_annotated_dir(self, tmp_path, test_png, blank_png):
        frames_dir = tmp_path / "frames"
        frames_dir.mkdir()
        frame1 = frames_dir / "frame1.png"
        frame2 = frames_dir / "frame2.png"
        frame1.write_bytes(test_png.read_bytes())
        frame2.write_bytes(blank_png.read_bytes())

        annotated_dir = tmp_path / "annotated"
        meta = tmp_path / "frames.json"
        meta.write_text(
            json.dumps(
                [
                    {"file": "frame1.png", "step": "First", "duration": 500, "highlights": []},
                    {"file": "frame2.png", "step": "Second", "duration": 500, "highlights": []},
                ]
            )
        )

        out = tmp_path / "out.webp"
        result = build_segment_animation(frames_dir, meta, out, annotated_dir=str(annotated_dir))
        assert result is True
        assert (annotated_dir / "frame1.png").exists()
        assert (annotated_dir / "frame2.png").exists()

    def test_convert_exception_continues(self, tmp_path, test_png, blank_png):
        frames_dir = tmp_path / "frames"
        frames_dir.mkdir()
        frame1 = frames_dir / "frame1.png"
        frame2 = frames_dir / "frame2.png"
        frame1.write_bytes(test_png.read_bytes())
        frame2.write_bytes(blank_png.read_bytes())

        meta = tmp_path / "frames.json"
        meta.write_text(
            json.dumps(
                [
                    {"file": "frame1.png", "step": "First", "duration": 500, "highlights": []},
                    {"file": "frame2.png", "step": "Second", "duration": 500, "highlights": []},
                ]
            )
        )

        out = tmp_path / "out.webp"

        class ConvertRaisingImage:
            def convert(self, *args, **kwargs):
                raise Exception("convert failed")

        with patch("capture.annotate.annotate_frame", return_value=ConvertRaisingImage()):
            result = build_segment_animation(frames_dir, meta, out)

        assert result is False
