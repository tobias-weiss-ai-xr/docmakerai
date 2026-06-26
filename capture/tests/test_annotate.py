from pathlib import Path

from PIL import Image

from capture.annotate import (
    CIRCLED_NUMBERS,
    _build_header_text,
    _draw_circle_highlight,
    _draw_header,
    annotate_frame,
    build_segment_animation,
)


class TestBuildHeaderText:
    def test_english(self):
        result = _build_header_text("Login", 1, "en")
        assert "Step" in result
        assert "Login" in result
        assert CIRCLED_NUMBERS[0] in result

    def test_german(self):
        result = _build_header_text("Anmelden", 3, "de")
        assert "Schritt" in result
        assert "Anmelden" in result
        assert CIRCLED_NUMBERS[2] in result

    def test_circled_number_fallback(self):
        result = _build_header_text("Test", 99, "en")
        assert "99" in result


class TestDrawHeader:
    def test_header_added(self, test_png: Path):
        img = Image.open(test_png).convert("RGBA")
        result = _draw_header(img, "Step 1: Login")
        assert result.size == img.size
        original_first_row = [img.getpixel((x, 0)) for x in range(10)]
        result_first_pixel = result.getpixel((0, 0))
        assert result_first_pixel != original_first_row[0]


class TestDrawCircleHighlight:
    def test_highlight_drawn(self, test_png: Path):
        img = Image.open(test_png).convert("RGBA")
        highlight = {"x": 10, "y": 10, "width": 30, "height": 30}
        result = _draw_circle_highlight(img, highlight)
        assert result.getpixel((25, 25)) != img.getpixel((25, 25))


class TestAnnotateFrame:
    def test_basic_annotation(self, test_png: Path):
        result = annotate_frame(
            test_png,
            step_label="Test Step",
            step_number=1,
            highlights=[],
            locale="en",
        )
        assert result is not None
        assert isinstance(result, Image.Image)

    def test_with_circle_highlight(self, test_png: Path):
        highlights = [{"type": "circle", "x": 10, "y": 10, "width": 20, "height": 20}]
        result = annotate_frame(test_png, "Test", 1, highlights, "en")
        assert result is not None

    def test_with_arrow_highlight(self, test_png: Path):
        highlights = [{"type": "arrow", "x": 50, "y": 50, "width": 10, "height": 10}]
        result = annotate_frame(test_png, "Test", 1, highlights, "en")
        assert result is not None

    def test_saves_to_output_path(self, test_png: Path, tmp_path: Path):
        out = tmp_path / "out.png"
        result = annotate_frame(test_png, "Test", 1, [], "en", output_path=str(out))
        assert result is not None
        assert out.exists()

    def test_missing_file_returns_none(self):
        result = annotate_frame("/nonexistent/image.png", "Test", 1, [], "en")
        assert result is None


class TestBuildSegmentAnimation:
    def test_insufficient_frames_returns_false(self, tmp_path: Path):
        out = tmp_path / "out.webp"
        meta = tmp_path / "frames.json"
        import json

        meta.write_text(json.dumps([]))
        result = build_segment_animation(tmp_path, meta, out)
        assert result is False
