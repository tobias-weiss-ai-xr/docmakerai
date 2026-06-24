#!/usr/bin/env python3
"""
DocMaker AI — Asset Optimization Pipeline

Reduces WebP and PNG asset sizes for the Docusaurus documentation site.

Strategies:
  - WebP animations: reduce frame rate, lower quality via ffmpeg
  - PNG screenshots: quantize to 256 colors, strip metadata via Pillow

Usage:
  python capture/optimize.py                    # optimize all assets
  python capture/optimize.py --dry-run          # preview sizes without changes
  python capture/optimize.py --target site/docs/assets
  python capture/optimize.py --max-size 150     # target KB per asset
"""

from __future__ import annotations

import argparse
import shutil
import tempfile
from pathlib import Path
from typing import NamedTuple

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TARGETS = [
    ROOT / "site" / "versioned_docs" / "sogo5" / "assets",
    ROOT / "site" / "versioned_docs" / "sogo6" / "assets",
]

# Quality settings
WEBP_QUALITY = 60          # 0-100, lower = smaller (was: default ~80)
WEBP_FRAME_SKIP = 2        # keep every Nth frame (2 = halve frame count)
WEBP_MAX_SIZE_KB = 200     # target max size per WebP
PNG_COLORS = 256           # quantize to N colors
PNG_MAX_SIZE_KB = 80       # target max size per PNG


class OptimizationResult(NamedTuple):
    file: Path
    original_kb: float
    optimized_kb: float
    reduction_pct: float
    method: str


def get_size_kb(path: Path) -> float:
    return path.stat().st_size / 1024


def optimize_webp(source: Path, target: Path, quality: int = WEBP_QUALITY,
                  frame_skip: int = WEBP_FRAME_SKIP) -> bool:
    """Optimize an animated WebP using Pillow frame extraction and re-encoding.

    Reduces frame count and quality while preserving animation.
    Returns True if optimization succeeded and produced a smaller file.
    """
    original_kb = get_size_kb(source)

    try:
        img = Image.open(source)
        n_frames = getattr(img, "n_frames", 1)

        if n_frames <= 1:
            img.save(target, format="WEBP", quality=quality, method=6)
        else:
            selected_indices = list(range(0, n_frames, frame_skip))
            frames = []
            durations = []
            for i in selected_indices:
                img.seek(i)
                frame = img.convert("RGBA")
                frames.append(frame)
                durations.append(img.info.get("duration", 100) * frame_skip)

            if not frames:
                return False

            frames[0].save(
                target,
                format="WEBP",
                save_all=True,
                append_images=frames[1:],
                duration=durations,
                loop=0,
                quality=quality,
                method=6,
            )

        if not target.exists():
            return False

        new_kb = get_size_kb(target)
        return new_kb < original_kb

    except Exception as e:
        print(f"  ⚠ WebP optimization failed: {e}")
        return False


def optimize_png(source: Path, target: Path, colors: int = PNG_COLORS) -> bool:
    """Optimize a PNG using Pillow quantization and metadata stripping.

    Returns True if optimization succeeded and produced a smaller file.
    """
    original_kb = get_size_kb(source)

    try:
        img = Image.open(source)

        # Convert to RGBA if has transparency, RGB otherwise
        if img.mode in ("P", "L"):
            img = img.convert("RGBA" if "transparency" in img.info else "RGB")
        elif img.mode != "RGBA" and img.mode != "RGB":
            img = img.convert("RGB")

        # Quantize to reduce color palette
        quantized = img.quantize(
            colors=colors,
            method=Image.Quantize.MEDIANCUT,
            dither=Image.Dither.FLOYDSTEINBERG,
        )

        # Save without metadata
        quantized.save(target, format="PNG", optimize=True)

        new_kb = get_size_kb(target)
        return new_kb < original_kb

    except Exception as e:
        print(f"  ⚠ PNG optimization failed: {e}")
        return False


def optimize_directory(directory: Path, dry_run: bool = False,
                       max_size_kb: int | None = None) -> list[OptimizationResult]:
    """Optimize all WebP and PNG assets in a directory."""
    results: list[OptimizationResult] = []

    if not directory.exists():
        print(f"  ⚠ Directory not found: {directory}")
        return results

    webp_files = sorted(directory.glob("*.webp"))
    png_files = sorted(directory.glob("*.png"))

    print(f"\n📦 {directory}")
    print(f"   {len(webp_files)} WebP, {len(png_files)} PNG files")

    for webp in webp_files:
        original_kb = get_size_kb(webp)

        if max_size_kb and original_kb <= max_size_kb:
            results.append(OptimizationResult(webp, original_kb, original_kb, 0.0, "skip"))
            continue

        if dry_run:
            print(f"   🔍 {webp.name}: {original_kb:.0f}KB (would optimize)")
            results.append(OptimizationResult(webp, original_kb, original_kb, 0.0, "dry-run"))
            continue

        with tempfile.NamedTemporaryFile(suffix=".webp", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        try:
            if optimize_webp(webp, tmp_path):
                new_kb = get_size_kb(tmp_path)
                reduction = ((original_kb - new_kb) / original_kb) * 100
                shutil.copy2(tmp_path, webp)
                print(
                    f"   ✅ {webp.name}: {original_kb:.0f}KB → {new_kb:.0f}KB"
                    f" ({reduction:.0f}% smaller)"
                )
                results.append(OptimizationResult(webp, original_kb, new_kb, reduction, "webp"))
            else:
                print(f"   ⏭️  {webp.name}: {original_kb:.0f}KB (no improvement)")
                results.append(OptimizationResult(webp, original_kb, original_kb, 0.0, "skip"))
        finally:
            tmp_path.unlink(missing_ok=True)

    for png in png_files:
        original_kb = get_size_kb(png)

        if dry_run:
            print(f"   🔍 {png.name}: {original_kb:.0f}KB (would quantize)")
            results.append(OptimizationResult(png, original_kb, original_kb, 0.0, "dry-run"))
            continue

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        try:
            if optimize_png(png, tmp_path):
                new_kb = get_size_kb(tmp_path)
                reduction = ((original_kb - new_kb) / original_kb) * 100
                shutil.copy2(tmp_path, png)
                print(
                    f"   ✅ {png.name}: {original_kb:.0f}KB → {new_kb:.0f}KB"
                    f" ({reduction:.0f}% smaller)"
                )
                results.append(OptimizationResult(png, original_kb, new_kb, reduction, "png"))
            else:
                print(f"   ⏭️  {png.name}: {original_kb:.0f}KB (no improvement)")
                results.append(OptimizationResult(png, original_kb, original_kb, 0.0, "skip"))
        finally:
            tmp_path.unlink(missing_ok=True)

    return results


def print_summary(all_results: list[OptimizationResult]) -> None:
    """Print a summary of all optimization results."""
    print("\n" + "=" * 70)
    print("OPTIMIZATION SUMMARY")
    print("=" * 70)

    total_original = sum(r.original_kb for r in all_results)
    total_optimized = sum(r.optimized_kb for r in all_results)

    if total_original > 0:
        total_reduction = ((total_original - total_optimized) / total_original) * 100
    else:
        total_reduction = 0.0

    optimized_count = sum(1 for r in all_results if r.method in ("webp", "png"))
    skipped_count = sum(1 for r in all_results if r.method in ("skip", "dry-run"))

    print(f"  Files optimized: {optimized_count}")
    print(f"  Files skipped:   {skipped_count}")
    print(f"  Total size:      {total_original:.0f}KB → {total_optimized:.0f}KB")
    print(f"  Reduction:       {total_reduction:.1f}%")
    print("=" * 70)

    over_target = [r for r in all_results if r.optimized_kb > WEBP_MAX_SIZE_KB and r.file.suffix == ".webp"]
    if over_target:
        print(f"\n⚠️  WebP files still over {WEBP_MAX_SIZE_KB}KB target:")
        for r in sorted(over_target, key=lambda x: x.optimized_kb, reverse=True):
            print(f"   {r.file.name}: {r.optimized_kb:.0f}KB")


def main() -> None:
    parser = argparse.ArgumentParser(description="Optimize documentation assets")
    parser.add_argument("--dry-run", action="store_true", help="Preview without changes")
    parser.add_argument("--target", type=Path, help="Specific directory to optimize")
    parser.add_argument("--max-size", type=int, default=None, help="Skip files already under this size (KB)")
    args = parser.parse_args()

    directories = [args.target] if args.target else DEFAULT_TARGETS

    print("🔧 DocMaker AI — Asset Optimization Pipeline")
    print(f"   Mode: {'DRY RUN' if args.dry_run else 'OPTIMIZE'}")

    all_results: list[OptimizationResult] = []
    for directory in directories:
        results = optimize_directory(directory, dry_run=args.dry_run, max_size_kb=args.max_size)
        all_results.extend(results)

    print_summary(all_results)


if __name__ == "__main__":
    main()
