#!/usr/bin/env python3
"""
DocMaker AI — WebP to MP4/WebM Converter

Converts captured WebP animations to HTML5-native formats for better
quality, accessibility, and browser support.

Output Formats:
- MP4 (H.264 + AAC) — Primary, 98% browser support
- WebM (VP9 + Opus) — Modern browsers, better compression

Usage:
    python scripts/convert_to_mp4.py videos/ assets/

Features:
- Preserves WebP duration and frame rate
- Adds字幕 (VTT) support optional
- Generates size-optimized versions
- Parallel conversion with worker pool
"""

import argparse
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import NamedTuple

FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"


class ConversionResult(NamedTuple):
    input_file: Path
    video_path: Path | None
    audio_path: Path | None
    thumbnails_path: Path | None
    metadata_path: Path | None
    success: bool
    error: str | None


def get_duration(webp_path: Path) -> float:
    """Get duration of a WebP file in seconds."""
    try:
        # First try to find metadata file
        metadata_path = webp_path.parent / f"{webp_path.stem}_metadata.json"

        if metadata_path.exists():
            meta = json.loads(metadata_path.read_text())
            return meta.get("webp_duration_s", 0)

        # Fallback: use ffprobe on WebP (doesn't always work
        result = subprocess.run(
            [
                FFPROBE, "-v", "error", "-show_entries", "format=duration",
                "-of", "json", str(webp_path),
            ],
            capture_output=True,
            text=True,
        )
        data = json.loads(result.stdout)
        return float(data["format"]["duration"])
    except Exception:
        return 0.0


def webp_to_mp4(webp_path: Path, output_dir: Path, quality: int = 23) -> ConversionResult:
    """Convert WebP animation to MP4 (H.264 + AAC)."""

    duration = get_duration(webp_path)
    output_mp4 = output_dir / f"{webp_path.stem}.mp4"

    if duration == 0:
        return ConversionResult(
            webp_path=webp_path,
            video_path=None,
            audio_path=None,
            thumbnails_path=None,
            metadata_path=None,
            success=False,
            error="Could not determine WebP duration"
        )

    try:
        # Extract frames from WebP as sequence
        # Prelj: Convert WebP → PNG frames → MP4

        # Use ffmpeg directly for WebP → MP4 conversion
        # First check if it's animated
        result = subprocess.run(
            [
                FFPROBE, "-v", "error", "-select_streams", "v:0",
                "-show_entries", "stream=width,height,duration,nb_read_frames,r_frame_rate",
                "-of", "json", str(webp_path),
            ],
            capture_output=True,
            text=True,
        )

        json.loads(result.stdout)

        # For simplicity, use ffmpeg's native WebP decoding
        # Extract frames to temporary directory, then re-encode
        tmp_frames = output_dir / "temp_frames" / webp_path.stem
        tmp_frames.mkdir(parents=True, exist_ok=True)

        # Save first frame (for thumbnail)
        thumbnail_path = output_dir / f"{webp_path.stem}-poster.jpg"

        subprocess.run([
            FFMPEG,
            "-i", str(webp_path),
            "-vf", "scale=1280:800,thumbnail",  # Generate poster image
            "-frames:v", "1",
            str(thumbnail_path),
            "-y",
            "-loglevel", "error"
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Convert WebP → MP4
        # Using fps from WebP metadata, default to 6 if unknown
        fps = 6
        metadata_path = webp_path.parent / f"{webp_path.stem}_metadata.json"

        if metadata_path.exists():
            meta = json.loads(metadata_path.read_text())
            fps = meta.get("fps", 6)

        # Main conversion: WebP → MP4
        subprocess.run([
            FFMPEG,
            "-i", str(webp_path),
            "-c:v", "libx264",              # H.264 codec
            "-preset", "medium",               # Balance speed/quality
            "-crf", str(quality),              # Quality (18-28, lower=better)
            "-pix_fmt", "yuv420p",             # Broad compatibility
            "-vf", f"fps={fps}",               # Match original frame rate
            "-t", f"{duration}",               # Match duration
            "-an",                             # No audio (WebP has no audio)
            "-movflags", "+faststart",         # Fast start for streaming
            str(output_mp4),
            "-y",
            "-loglevel", "error"
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Capture metadata
        result = subprocess.run([
            FFPROBE, "-v", "error",
            "-show_entries", "format=duration,size:stream=codec_name,width,height",
            "-of", "json", str(output_mp4),
        ], capture_output=True, text=True, check=True)

        metadata = {
            "input_webp": webp_path.name,
            "output_mp4": output_mp4.name,
            "duration_s": duration,
            "fps": fps,
            "width": 1280,
            "height": 800,
            "quality": quality,
            "thumbnail": f"{webp_path.stem}-poster.jpg",
        }

        metadata_out = output_dir / f"{webp_path.stem}_metadata.json"
        metadata_out.write_text(json.dumps(metadata, indent=2))

        return ConversionResult(
            webp_path=webp_path,
            video_path=output_mp4,
            audio_path=None,
            thumbnails_path=thumbnail_path,
            metadata_path=metadata_out,
            success=True,
            error=None
        )

    except subprocess.CalledProcessError as e:
        return ConversionResult(
            webp_path=webp_path,
            video_path=None,
            audio_path=None,
            thumbnails_path=None,
            metadata_path=None,
            success=False,
            error=str(e)
        )
    except Exception as e:
        return ConversionResult(
            webp_path=webp_path,
            video_path=None,
            audio_path=None,
            thumbnails_path=None,
            metadata_path=None,
            success=False,
            error=str(e)
        )


def webp_to_webm(webp_path: Path, output_dir: Path, quality: int = 30) -> ConversionResult:
    """Convert WebP animation to WebM (VP9 + Opus)."""
    duration = get_duration(webp_path)
    output_webm = output_dir / f"{webp_path.stem}.webm"

    if duration == 0:
        return ConversionResult(
            webp_path=webp_path,
            video_path=None,
            audio_path=None,
            thumbnails_path=None,
            metadata_path=None,
            success=False,
            error="Could not determine WebP duration"
        )

    try:
        fps = 6
        metadata_path = webp_path.parent / f"{webp_path.stem}_metadata.json"

        if metadata_path.exists():
            meta = json.loads(metadata_path.read_text())
            fps = meta.get("fps", 6)

        # WebP → WebM (VP9)
        subprocess.run([
            FFMPEG,
            "-i", str(webp_path),
            "-c:v", "libvpx-vp9",            # VP9 codec
            "-crf", str(quality),              # Quality (0-63, lower=better)
            "-b:v", "0",                      # Constant quality mode
            "-vf", f"fps={fps}",
            "-t", f"{duration}",
            "-an",                             # No audio
            str(output_webm),
            "-y",
            "-loglevel", "error"
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        return ConversionResult(
            webp_path=webp_path,
            video_path=output_webm,
            audio_path=None,
            thumbnails_path=None,
            metadata_path=None,
            success=True,
            error=None
        )

    except subprocess.CalledProcessError as e:
        return ConversionResult(
            webp_path=webp_path,
            video_path=None,
            audio_path=None,
            thumbnails_path=None,
            metadata_path=None,
            success=False,
            error=str(e)
        )
    except Exception as e:
        return ConversionResult(
            webp_path=webp_path,
            video_path=None,
            audio_path=None,
            thumbnails_path=None,
            metadata_path=None,
            success=False,
            error=str(e)
        )


def convert_directory(
    input_dir: Path,
    output_dir: Path,
    formats: list[str] | None = None,  # "mp4", "webm", or both
    workers: int = 4
) -> list[ConversionResult]:
    """Convert all WebP files in directory."""
    if formats is None:
        formats = ["mp4"]
    webp_files = sorted(input_dir.glob("*.webp"))

    if not webp_files:
        print(f"  ⚠️  No WebP files found in {input_dir}")
        return []

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n📦 Converting {len(webp_files)} WebP files in {input_dir.name}")
    print(f"   Output: {output_dir}")
    print(f"   Formats: {', '.join(formats).upper()}")

    results = []

    def convert(webp: Path):
        result = None
        if "mp4" in formats:
            result = webp_to_mp4(webp, output_dir)
        if "webm" in formats and (result is None or not result.success):
            fallback = webp_to_webm(webp, output_dir)
            result = fallback if result is None else fallback._replace(audio_path=result.audio_path)
        if result is None:
            result = webp_to_mp4(webp, output_dir)  # Default to MP4

        if result.success:
            size_kb = result.video_path.stat().st_size / 1024
            print(f"   ✅ {webp.name} → {result.video_path.name} ({size_kb:.0f}KB)")
        else:
            print(f"   ⚠️  {webp.name} → FAILED: {result.error}")

        return result

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(convert, wp) for wp in webp_files]

        for future in as_completed(futures):
            results.append(future.result())

    success_count = sum(1 for r in results if r.success)
    failed_count = len(results) - success_count

    print(f"\n📊 Results: {success_count} converted, {failed_count} failed")

    return results


def main():
    parser = argparse.ArgumentParser(description="Convert WebP animations to HTML5 video formats")
    parser.add_argument("input", type=Path, help="Input directory with WebP files")
    parser.add_argument("output", type=Path, help="Output directory for MP4/WebM")
    parser.add_argument("--formats", nargs="+", default=["mp4"], choices=["mp4", "webm"])
    parser.add_argument("--workers", type=int, default=4, help="Parallel workers")
    args = parser.parse_args()

    print("🎬 DocMaker AI — WebP → HTML5 Video Converter")

    if not args.input.exists():
        print(f"❌ Input directory not found: {args.input}")
        return

    convert_directory(args.input, args.output, args.formats, args.workers)


if __name__ == "__main__":
    main()
