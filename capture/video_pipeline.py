"""
DocMaker AI — Video → Annotated WebP Pipeline

Combines Playwright video recording with ffmpeg frame extraction and
Pillow annotation overlay to produce smooth animated WebP clips.

Workflow:
  1. Record a browser workflow via Playwright video (.webm)
  2. Record step timestamps (performance.now()) + metadata at each step
  3. Close context → finalize video
  4. ffmpeg extracts frames at target FPS
  5. Each frame is annotated with the nearest step's label + highlights
  6. ffmpeg assembles annotated frames into final animated WebP
"""

import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from PIL import Image

try:
    from capture.annotate import annotate_frame
except ImportError:
    from annotate import annotate_frame


def extract_frames(
    video_path: Path,
    output_dir: Path,
    fps: int = 6,
) -> list[Path]:
    """Extract frames from a WebM video at *fps* frames per second.

    Returns a sorted list of extracted PNG paths.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    pattern = str(output_dir / "f_%04d.png")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video_path),
            "-vf",
            f"fps={fps}",
            "-vsync",
            "cfr",
            "-start_number",
            "1",
            "-qscale:v",
            "2",
            pattern,
        ],
        check=True,
        capture_output=True,
    )
    frames = sorted(output_dir.glob("f_*.png"))
    return frames


def map_frames_to_steps(
    frame_count: int,
    video_duration_s: float,
    steps: list[dict],
) -> list[dict]:
    """Map frame indices to their nearest step annotation.

    *steps* must be a list of dicts with keys:
        time_s (float): seconds since start of recording
        label  (str):   step header text
        highlights (list): highlight markers for this step

    Returns a list of dicts with keys: frame_idx, time_s, step_label,
    step_number, highlights.
    """
    mapped = []
    for i in range(frame_count):
        t = (i / max(frame_count - 1, 1)) * video_duration_s
        # Find the step with the closest *preceding* timestamp
        best = steps[0]
        for s in steps:
            if s["time_s"] <= t:
                best = s
        mapped.append(
            {
                "frame_idx": i,
                "time_s": t,
                "step_label": best["label"],
                "step_number": best.get("number", steps.index(best) + 1),
                "highlights": best.get("highlights", []),
            }
        )
    return mapped


def annotate_frames(
    raw_frames: list[Path],
    mapping: list[dict],
    annotated_dir: Path,
    locale: str = "en",
) -> list[Path]:
    """Annotate raw frames with step headers and return annotated paths."""
    annotated_dir.mkdir(parents=True, exist_ok=True)
    annotated_paths = []
    for raw_path, meta in zip(raw_frames, mapping, strict=False):
        out_path = annotated_dir / raw_path.name
        img = annotate_frame(
            raw_path,
            meta["step_label"],
            meta["step_number"],
            meta["highlights"],
            locale=locale,
            output_path=str(out_path),
        )
        if img:
            annotated_paths.append(out_path)
    return annotated_paths


def assemble_webp(
    frame_paths: list[Path],
    output_path: Path,
    fps: int = 6,
    quality: int = 85,
    keep_frames: bool = False,
):
    """Assemble annotated frames into an animated WebP using ffmpeg.

    Uses ffmpeg instead of Pillow to avoid Pillow's frame deduplication
    issues with animated WebP.  Injects a tiny per-frame watermark
    (opaque frame number) to guarantee each frame is unique, preventing
    the libwebp_anim encoder from dropping seemingly identical frames.

    Args:
        frame_paths: Sorted list of annotated PNGs.
        output_path: Where to save the .webp file.
        fps: Output framerate.
        quality: WebP quality (0-100).
        keep_frames: Keep the intermediate annotated frames (for debugging).
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        watermarked_dir = workdir / "wm"
        watermarked_dir.mkdir()

        for i, fp in enumerate(frame_paths):
            wm_path = watermarked_dir / fp.name
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    str(fp),
                    "-vf",
                    f"drawtext=text='':fontsize=1:fontcolor=black@0.01:x=0:y=0:box=0,"
                    f"drawtext=text='{i:04d}':fontsize=1:fontcolor=white@0.02:x=W-15:y=H-3:box=0",
                    "-qscale:v",
                    "1",
                    str(wm_path),
                ],
                check=True,
                capture_output=True,
            )

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-framerate",
                str(fps),
                "-pattern_type",
                "glob",
                "-i",
                str(watermarked_dir / "*.png"),
                "-loop",
                "0",
                "-compression_level",
                "6",
                "-quality",
                str(quality),
                "-vsync",
                "0",
                str(output_path),
            ],
            check=True,
            capture_output=True,
        )

    # Optionally keep annotated frames
    if not keep_frames:
        for fp in frame_paths:
            fp.unlink(missing_ok=True)

    # Verify output
    if not output_path.exists() or output_path.stat().st_size < 100:
        raise RuntimeError(f"WebP assembly failed: {output_path}")


def get_video_duration(video_path: Path) -> float:
    """Get video duration in seconds via ffprobe."""
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(video_path),
        ],
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def is_frame_valid(frame_path: Path) -> bool:
    """Check if a frame has meaningful content (not blank/all-white/all-black)."""
    try:
        img = Image.open(frame_path)
        gray = img.convert("L")
        pixels = list(gray.getdata())
        if len(set(pixels)) == 1:
            return False
        near_white = sum(1 for p in pixels if p > 245)
        if near_white > len(pixels) * 0.98:
            return False
        near_black = sum(1 for p in pixels if p < 10)
        if near_black > len(pixels) * 0.98:
            return False
        bright_pixels = [p for p in pixels if p > 20 and p < 235]
        if len(bright_pixels) < len(pixels) * 0.05:
            return False
        pixel_range = max(pixels) - min(pixels)
        return pixel_range >= 20
    except Exception:
        return False


def validate_frames(raw_frames: list[Path], workflow_name: str) -> tuple[bool, str]:
    """
    Validate that extracted frames contain meaningful content.

    Returns (is_valid, error_message).
    """
    if len(raw_frames) < 4:
        return False, f"Too few frames ({len(raw_frames)}) for {workflow_name}"
    check_indices = [0, len(raw_frames) // 2, -1]
    for idx in check_indices:
        frame = raw_frames[idx]
        if not is_frame_valid(frame):
            msg = f"{workflow_name}: Frame {idx + 1} appears blank"
            return False, msg
    sample_indices = [len(raw_frames) * i // 10 for i in range(1, 10)]
    sample_size = sum(1 for idx in sample_indices if idx < len(raw_frames))
    valid_count = 0
    for idx in sample_indices:
        if idx < len(raw_frames) and is_frame_valid(raw_frames[idx]):
            valid_count += 1
    if valid_count < sample_size * 0.8:
        msg = f"{workflow_name}: {sample_size - valid_count}/{sample_size} frames blank"
        return False, msg
    return True, ""


class WorkflowRecorder:
    """Records a browser workflow via Playwright video and produces
    an annotated animated WebP.

    Usage:
        recorder = WorkflowRecorder(workflow_name)
        page = await recorder.start(context)
        await recorder.step(page, "Step 1 label", highlights=[...])
        # ... do stuff ...
        await recorder.step(page, "Step 2 label")
        webp_path = await recorder.finish(page)
        # webp_path holds the final .webp file
    """

    def __init__(
        self,
        workflow_name: str,
        video_dir: Path,
        gif_dir: Path,
        fps: int = 6,
        locale: str = "en",
    ):
        self.workflow_name = workflow_name
        self.video_dir = video_dir
        self.gif_dir = gif_dir
        self.fps = fps
        self.locale = locale
        self.steps: list[dict] = []
        self._start_time: float | None = None
        self._page_created_time: float | None = None

    async def start(self, context) -> Any:
        """Create a new page in *context* and start recording."""
        page = await context.new_page()
        # Record baseline timestamp (ms since epoch via JS)
        self._page_created_time = await page.evaluate("performance.now()")
        return page

    async def step(
        self,
        page,
        label: str,
        highlights: list | None = None,
    ):
        """Record a step annotation with the current page timestamp."""
        now = await page.evaluate("performance.now()")
        elapsed_s = (now - self._page_created_time) / 1000.0
        self.steps.append(
            {
                "time_s": elapsed_s,
                "label": label,
                "number": len(self.steps) + 1,
                "highlights": highlights or [],
            }
        )

    async def finish(self, page, keep_raw_video: bool = False) -> Path | None:
        """Close the page, process video, and return the WebP path.

        Returns None on failure.
        """
        await page.close()

        # Locate the recorded video
        if not page.video:
            return None
        video_path = Path(await page.video.path())

        if not video_path.exists() or video_path.stat().st_size < 1000:
            return None

        duration = get_video_duration(video_path)
        if duration < 0.5:
            return None

        # Extract frames
        raw_dir = video_path.parent / f"{self.workflow_name}_raw"
        raw_frames = extract_frames(video_path, raw_dir, fps=self.fps)

        if len(raw_frames) < 4:
            return None

        # Validate frames have meaningful content (not blank)
        frame_valid, frame_error = validate_frames(raw_frames, self.workflow_name)
        if not frame_valid:
            print(f"  Frame validation failed: {frame_error}")
            if not keep_raw_video:
                shutil.rmtree(raw_dir, ignore_errors=True)
            if video_path.exists():
                video_path.unlink(missing_ok=True)
            return None

        # Map frames to steps
        mapping = map_frames_to_steps(len(raw_frames), duration, self.steps)

        # Annotate
        annotated_dir = video_path.parent / f"{self.workflow_name}_annotated"
        annotated_frames = annotate_frames(raw_frames, mapping, annotated_dir, locale=self.locale)

        if len(annotated_frames) < 4:
            if not keep_raw_video:
                shutil.rmtree(raw_dir, ignore_errors=True)
                shutil.rmtree(annotated_dir, ignore_errors=True)
                if video_path.exists():
                    video_path.unlink(missing_ok=True)
            return None

        # Assemble WebP
        webp_path = self.gif_dir / f"{self.workflow_name}.webp"
        assemble_webp(
            annotated_frames,
            webp_path,
            fps=self.fps,
        )

        # Cleanup
        if not keep_raw_video:
            shutil.rmtree(raw_dir, ignore_errors=True)
            shutil.rmtree(annotated_dir, ignore_errors=True)

        # Write metadata for reference
        meta = video_path.parent / f"{self.workflow_name}_metadata.json"
        with open(meta, "w") as f:
            json.dump(
                {
                    "workflow": self.workflow_name,
                    "video_file": video_path.name,
                    "duration_s": duration,
                    "raw_frames": len(raw_frames),
                    "annotated_frames": len(annotated_frames),
                    "fps": self.fps,
                    "steps": self.steps,
                    "webp_file": webp_path.name,
                    "webp_size_kb": webp_path.stat().st_size // 1024,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )
        if not keep_raw_video:
            video_path.unlink(missing_ok=True)

        return webp_path
