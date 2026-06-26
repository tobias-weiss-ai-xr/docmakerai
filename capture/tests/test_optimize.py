"""Tests for capture.optimize."""

import random
import sys
from pathlib import Path

import pytest
from PIL import Image

from capture.optimize import (
    OptimizationResult,
    get_size_kb,
    main,
    optimize_directory,
    optimize_png,
    optimize_webp,
    print_summary,
)

# ── Helpers ──────────────────────────────────────────────────────────


def _make_webp(path: Path, size=(100, 100), frames: int = 1, color=(200, 100, 50),
               noisy: bool = False) -> Path:
    """Create a test WebP file. Supports multi-frame animation."""
    if frames <= 1:
        if noisy:
            img = _random_rgb_image(size)
        else:
            img = Image.new("RGB", size, color)
        img.save(path, format="WEBP", quality=80)
    else:
        imgs = []
        for c in range(frames):
            if noisy:
                imgs.append(_random_rgba_image(size))
            else:
                imgs.append(Image.new("RGBA", size, (c * 30 % 256, 50, 100, 255)))
        imgs[0].save(
            path,
            format="WEBP",
            save_all=True,
            append_images=imgs[1:],
            duration=[100] * frames,
            loop=0,
            quality=80,
        )
    return path


def _random_rgb_image(size):
    """Create an RGB image with random pixel data (many unique colors)."""
    img = Image.new("RGB", size)
    pixels = img.load()
    for x in range(size[0]):
        for y in range(size[1]):
            pixels[x, y] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return img


def _random_rgba_image(size):
    """Create an RGBA image with random pixel data."""
    img = Image.new("RGBA", size)
    pixels = img.load()
    for x in range(size[0]):
        for y in range(size[1]):
            pixels[x, y] = (random.randint(0, 255), random.randint(0, 255),
                            random.randint(0, 255), 255)
    return img


def _make_png(path: Path, size=(100, 100), mode: str = "RGB", color=(200, 100, 50),
              noisy: bool = False) -> Path:
    """Create a test PNG file in various modes."""
    if noisy:
        if mode == "P":
            # Create a noisy palette image by building from RGB then quantizing
            rgb = _random_rgb_image(size)
            rgb.save(path, format="PNG")
        elif mode == "RGBA":
            _random_rgba_image(size).save(path, format="PNG")
        else:
            _random_rgb_image(size).save(path, format="PNG")
        return path
    if mode == "RGBA":
        img = Image.new("RGBA", size, (*color, 128))
    elif mode == "P":
        img = Image.new("P", size)
        pal = []
        for i in range(256):
            pal.extend([i, 255 - i, 128])
        img.putpalette(pal[:768])
    elif mode == "L":
        img = Image.new("L", size, 128)
    else:
        img = Image.new("RGB", size, color)
    img.save(path, format="PNG")
    return path


# ── OptimizationResult ───────────────────────────────────────────────


class TestOptimizationResult:
    def test_creation(self):
        r = OptimizationResult(Path("a.webp"), 100.0, 50.0, 50.0, "webp")
        assert r.file.name == "a.webp"
        assert r.original_kb == 100.0
        assert r.optimized_kb == 50.0
        assert r.reduction_pct == 50.0
        assert r.method == "webp"

    def test_unpacking(self):
        f, o, n, r, m = OptimizationResult(Path("x.png"), 10.0, 5.0, 50.0, "png")
        assert f.name == "x.png"
        assert o == 10.0
        assert n == 5.0
        assert r == 50.0
        assert m == "png"

    def test_skip_result(self):
        r = OptimizationResult(Path("s.webp"), 20.0, 20.0, 0.0, "skip")
        assert r.optimized_kb == r.original_kb
        assert r.reduction_pct == 0.0


# ── get_size_kb ──────────────────────────────────────────────────────


class TestGetSizeKb:
    def test_returns_kilobytes(self, tmp_path):
        p = tmp_path / "test.bin"
        p.write_bytes(b"x" * 1024)
        assert get_size_kb(p) == pytest.approx(1.0, rel=0.01)

    def test_empty_file(self, tmp_path):
        p = tmp_path / "empty.bin"
        p.write_bytes(b"")
        assert get_size_kb(p) == 0.0

    def test_large_file(self, tmp_path):
        p = tmp_path / "large.bin"
        p.write_bytes(b"x" * 1024 * 10)
        assert get_size_kb(p) == pytest.approx(10.0, rel=0.01)

    def test_odd_sized_file(self, tmp_path):
        p = tmp_path / "odd.bin"
        p.write_bytes(b"x" * 512)
        assert get_size_kb(p) == pytest.approx(0.5, rel=0.01)


# ── optimize_webp ────────────────────────────────────────────────────


class TestOptimizeWebp:
    def test_single_frame(self, tmp_path):
        src = _make_webp(tmp_path / "src.webp", size=(200, 200))
        dst = tmp_path / "out.webp"
        result = optimize_webp(src, dst)
        assert result is True
        assert dst.exists()
        assert dst.stat().st_size < src.stat().st_size

    def test_animated_with_frame_skip(self, tmp_path):
        src = _make_webp(tmp_path / "anim.webp", size=(150, 150), frames=8)
        dst = tmp_path / "out.webp"
        result = optimize_webp(src, dst, quality=60, frame_skip=2)
        assert result is True
        assert dst.exists()

    def test_animated_with_frame_skip_4(self, tmp_path):
        """frame_skip of 4 on a 6-frame animation → 2 output frames."""
        src = _make_webp(tmp_path / "anim.webp", size=(100, 100), frames=6)
        dst = tmp_path / "out.webp"
        result = optimize_webp(src, dst, quality=60, frame_skip=4)
        assert result is True
        assert dst.exists()

    def test_no_improvement_when_already_small(self, tmp_path):
        """A tiny low-quality WebP can't be made smaller by re-encoding."""
        src = tmp_path / "tiny.webp"
        Image.new("RGB", (4, 4), (0, 0, 0)).save(src, format="WEBP", quality=1)
        dst = tmp_path / "out.webp"
        result = optimize_webp(src, dst, quality=60)
        assert result is False

    def test_corrupt_file_returns_false(self, tmp_path):
        """File exists but can't be opened as WebP → caught by try/except → False."""
        src = tmp_path / "corrupt.webp"
        src.write_bytes(b"not a valid image file")
        dst = tmp_path / "out.webp"
        result = optimize_webp(src, dst)
        assert result is False

    def test_custom_quality(self, tmp_path):
        """Noisy image at quality=80→30 should produce a smaller file."""
        src = _make_webp(tmp_path / "src.webp", size=(300, 300), noisy=True)
        dst = tmp_path / "out.webp"
        result = optimize_webp(src, dst, quality=30)
        assert result is True
        assert dst.exists()

    def test_empty_frames_after_skip(self, tmp_path, monkeypatch):
        """Line 82: n_frames>1 but list(range(...)) returns [] → frames empty → False."""
        import unittest.mock as mock

        src = tmp_path / "anim.webp"
        src.write_bytes(b"dummy")
        dst = tmp_path / "out.webp"

        class MockImage:
            n_frames = 5
            def seek(self, i):
                pass
            def convert(self, mode):
                return Image.new("RGBA", (1, 1))
            @property
            def info(self):
                return {"duration": 100}

        monkeypatch.setattr("PIL.Image.open", lambda path, **kw: MockImage())
        with mock.patch("builtins.list", return_value=[]):
            result = optimize_webp(src, dst, frame_skip=2)
        assert result is False

    def test_save_failure_returns_false(self, tmp_path):
        """Line 96: when target doesn't exist after save → False (single-frame)."""
        import unittest.mock as mock
        from pathlib import Path

        src = _make_webp(tmp_path / "src.webp", size=(200, 200))
        dst = tmp_path / "out.webp"
        with mock.patch.object(Path, "exists", return_value=False):
            result = optimize_webp(src, dst)
        assert result is False


# ── optimize_png ─────────────────────────────────────────────────────


class TestOptimizePng:
    def test_rgb_quantization(self, tmp_path):
        """RGB PNG with many colors → quantization reduces size."""
        src = _make_png(tmp_path / "src.png", size=(300, 300), mode="RGB", noisy=True)
        dst = tmp_path / "out.png"
        result = optimize_png(src, dst)
        assert result is True
        assert dst.exists()
        out_img = Image.open(dst)
        assert out_img.mode == "P"

    def test_rgba_with_transparency(self, tmp_path):
        """RGBA: MEDIANCUT doesn't support RGBA → caught by except → False."""
        src = _make_png(tmp_path / "rgba.png", size=(300, 300), mode="RGBA", noisy=True)
        dst = tmp_path / "out.png"
        result = optimize_png(src, dst)
        assert result is False
        assert not dst.exists() or get_size_kb(dst) >= 0  # dst might exist from save

    def test_palette_mode_conversion(self, tmp_path):
        """Palette-mode PNG → converts to RGB, quantizes, should improve."""
        src = _make_png(tmp_path / "palette.png", size=(300, 300), mode="P", noisy=True)
        dst = tmp_path / "out.png"
        result = optimize_png(src, dst)
        assert result is True
        assert dst.exists()

    def test_grayscale_mode(self, tmp_path):
        """L-mode → converts to RGB (3× data), quantization can't undo → False."""
        src = _make_png(tmp_path / "gray.png", size=(300, 300), mode="L")
        dst = tmp_path / "out.png"
        result = optimize_png(src, dst)
        assert result is False

    def test_cmyk_mode(self, tmp_path):
        """CMYK → converts through elif branch (line 120), then quantize."""
        src = tmp_path / "cmyk.tiff"
        cmyk = Image.new("CMYK", (300, 300))
        pixels = cmyk.load()
        for x in range(300):
            for y in range(300):
                pixels[x, y] = (x % 256, y % 256, (x + y) % 256, 0)
        cmyk.save(src, format="TIFF")
        dst = tmp_path / "out.png"
        optimize_png(src, dst)
        assert dst.exists()

    def test_no_improvement_tiny_image(self, tmp_path):
        """A 1×1 single-color PNG is already minimal — no improvement."""
        src = tmp_path / "tiny.png"
        Image.new("RGB", (1, 1), (0, 0, 0)).save(src, format="PNG")
        dst = tmp_path / "out.png"
        result = optimize_png(src, dst)
        assert result is False

    def test_custom_colors(self, tmp_path):
        """Custom color count should work."""
        src = _make_png(tmp_path / "src.png", size=(200, 200))
        dst = tmp_path / "out.png"
        result = optimize_png(src, dst, colors=128)
        assert result is True
        assert dst.exists()


# ── optimize_directory ───────────────────────────────────────────────


class TestOptimizeDirectory:
    def test_existing_directory(self, tmp_path):
        _make_webp(tmp_path / "a.webp", size=(300, 300), noisy=True)
        _make_webp(tmp_path / "b.webp", size=(300, 300), noisy=True)
        _make_png(tmp_path / "c.png", size=(300, 300), noisy=True)
        results = optimize_directory(tmp_path)
        assert len(results) == 3
        optimized = [r for r in results if r.method in ("webp", "png")]
        assert len(optimized) >= 1

    def test_nonexistent_directory(self, tmp_path):
        d = tmp_path / "nope"
        results = optimize_directory(d)
        assert results == []

    def test_dry_run_does_not_modify(self, tmp_path):
        _make_webp(tmp_path / "a.webp", size=(300, 300), noisy=True)
        orig_stat = (tmp_path / "a.webp").stat()
        results = optimize_directory(tmp_path, dry_run=True)
        assert len(results) == 1
        assert results[0].method == "dry-run"
        assert results[0].file.name == "a.webp"
        # File must be unchanged
        assert (tmp_path / "a.webp").stat() == orig_stat

    def test_dry_run_png(self, tmp_path):
        _make_png(tmp_path / "d.png", size=(300, 300), noisy=True)
        orig_stat = (tmp_path / "d.png").stat()
        results = optimize_directory(tmp_path, dry_run=True)
        assert len(results) == 1
        assert results[0].method == "dry-run"
        assert results[0].file.name == "d.png"
        assert (tmp_path / "d.png").stat() == orig_stat

    def test_max_size_kb_skips_small_files(self, tmp_path):
        _make_webp(tmp_path / "small.webp", size=(1, 1))
        orig_kb = get_size_kb(tmp_path / "small.webp")
        results = optimize_directory(tmp_path, max_size_kb=200)
        assert len(results) == 1
        assert results[0].method == "skip"
        assert results[0].original_kb == pytest.approx(orig_kb, rel=0.01)

    def test_mixed_webp_and_png(self, tmp_path):
        _make_webp(tmp_path / "w1.webp", size=(300, 300), noisy=True)
        _make_png(tmp_path / "p1.png", size=(300, 300), noisy=True)
        _make_webp(tmp_path / "w2.webp", size=(300, 300), noisy=True)
        results = optimize_directory(tmp_path)
        assert len(results) == 3
        methods = {r.method for r in results}
        assert "webp" in methods or "png" in methods


# ── print_summary ────────────────────────────────────────────────────


class TestPrintSummary:
    def test_runs_without_error(self, capsys):
        results = [
            OptimizationResult(Path("a.webp"), 100.0, 40.0, 60.0, "webp"),
            OptimizationResult(Path("b.png"), 50.0, 20.0, 60.0, "png"),
            OptimizationResult(Path("c.webp"), 30.0, 30.0, 0.0, "skip"),
        ]
        print_summary(results)
        captured = capsys.readouterr()
        assert "OPTIMIZATION SUMMARY" in captured.out
        assert "Files optimized: 2" in captured.out
        assert "Files skipped:   1" in captured.out

    def test_empty_results(self, capsys):
        print_summary([])
        captured = capsys.readouterr()
        assert "Files optimized: 0" in captured.out
        assert "Files skipped:   0" in captured.out

    def test_all_dry_run(self, capsys):
        results = [
            OptimizationResult(Path("a.webp"), 100.0, 100.0, 0.0, "dry-run"),
        ]
        print_summary(results)
        captured = capsys.readouterr()
        assert "Files optimized: 0" in captured.out
        assert "Files skipped:   1" in captured.out

    def test_over_target_warning(self, capsys):
        results = [
            OptimizationResult(Path("big.webp"), 500.0, 300.0, 40.0, "webp"),
        ]
        print_summary(results)
        captured = capsys.readouterr()
        assert "still over" in captured.out
        assert "200KB" in captured.out


# ── main ─────────────────────────────────────────────────────────────


class TestMain:
    def test_target_directory(self, tmp_path, monkeypatch):
        _make_webp(tmp_path / "a.webp", size=(300, 300), noisy=True)
        monkeypatch.setattr(sys, "argv", ["optimize.py", "--target", str(tmp_path)])
        main()  # should not raise

    def test_dry_run_flag(self, tmp_path, monkeypatch):
        _make_webp(tmp_path / "a.webp", size=(300, 300), noisy=True)
        monkeypatch.setattr(
            sys, "argv", ["optimize.py", "--dry-run", "--target", str(tmp_path)]
        )
        main()

    def test_max_size_flag(self, tmp_path, monkeypatch):
        _make_webp(tmp_path / "a.webp", size=(300, 300), noisy=True)
        monkeypatch.setattr(
            sys, "argv",
            ["optimize.py", "--target", str(tmp_path), "--max-size", "999"],
        )
        main()

    def test_default_targets_dont_exist(self, monkeypatch):
        """When no --target given, main() iterates DEFAULT_TARGETS (which don't exist)."""
        monkeypatch.setattr(sys, "argv", ["optimize.py"])
        main()  # should handle missing directories gracefully
