"""
DocMaker AI — Pillow Overlay Engine

Annotates raw screenshots with step-header overlays and UI highlight markers.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Optional

from PIL import Image, ImageDraw, ImageFont


HEADER_HEIGHT = 50
HEADER_BG = (30, 30, 30, 200)
HEADER_TEXT = (255, 255, 255)
HIGHLIGHT_CIRCLE = (220, 40, 40)
HIGHLIGHT_FILL = (220, 40, 40, 40)
ARROW_COLOR = (220, 40, 40)

CIRCLED_NUMBERS = ['\u2460', '\u2461', '\u2462', '\u2463', '\u2464',
                   '\u2465', '\u2466', '\u2467', '\u2468', '\u2469']


def _load_font(size: int = 22) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size
        )
    except (IOError, OSError):
        return ImageFont.load_default()


def _build_header_text(step_label: str, step_number: int, locale: str) -> str:
    prefix = "Step" if locale == "en" else "Schritt"
    circled = CIRCLED_NUMBERS[step_number - 1] if 1 <= step_number <= len(CIRCLED_NUMBERS) else str(step_number)
    return f"{circled} {prefix} {step_number}: {step_label}"


def _draw_header(img: Image.Image, text: str) -> Image.Image:
    result = Image.alpha_composite(img, Image.new("RGBA", img.size, (0, 0, 0, 0)))
    draw = ImageDraw.Draw(result)
    draw.rectangle([(0, 0), (img.width, HEADER_HEIGHT)], fill=HEADER_BG)
    font = _load_font(22)
    draw.text((12, (HEADER_HEIGHT - 22) // 2), text, fill=HEADER_TEXT, font=font)
    return result


def _draw_circle_highlight(img: Image.Image, highlight: dict) -> Image.Image:
    x = highlight.get("x", 0)
    y = highlight.get("y", 0)
    w = highlight.get("width", 0)
    h = highlight.get("height", 0)

    pad = max(4, w // 8, h // 8)
    bbox = (x - pad, y - pad, x + w + pad, y + h + pad)

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.ellipse(bbox, fill=HIGHLIGHT_FILL, outline=HIGHLIGHT_CIRCLE, width=4)
    return Image.alpha_composite(img, overlay)


def _draw_arrow_highlight(img: Image.Image, highlight: dict) -> Image.Image:
    x = highlight.get("x", 0)
    y = highlight.get("y", 0)
    w = highlight.get("width", 0)
    h = highlight.get("height", 0)

    cx = x + w // 2
    target_y = y + h // 2

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    start_y = HEADER_HEIGHT + 4
    overlay_draw.line([(cx, start_y), (cx, target_y)], fill=ARROW_COLOR, width=3)

    arrow_len = 14
    angle = math.radians(25)
    p1 = (cx - arrow_len * math.sin(angle), target_y - arrow_len * math.cos(angle))
    p2 = (cx + arrow_len * math.sin(angle), target_y - arrow_len * math.cos(angle))
    overlay_draw.polygon([(cx, target_y), p1, p2], fill=ARROW_COLOR)

    return Image.alpha_composite(img, overlay)


def annotate_frame(
    frame_path: str | Path,
    step_label: str,
    step_number: int,
    highlights: list[dict[str, Any]],
    locale: str = "de",
    output_path: Optional[str | Path] = None,
) -> Optional[Image.Image]:
    """Draw step header and UI highlights on a screenshot.

    Args:
        frame_path: Path to the raw PNG screenshot.
        step_label: Text label for the step (e.g. "Doppelklick auf Zeitslot").
        step_number: 1-based step number.
        highlights: List of highlight dicts (keys: type, x, y, width, height).
        locale: Language code ("en" or "de").
        output_path: If provided, save annotated PNG to this path.

    Returns:
        PIL Image with overlays drawn, or None on failure.
    """
    try:
        img = Image.open(frame_path).convert("RGBA")
    except Exception:
        return None

    text = _build_header_text(step_label, step_number, locale)
    img = _draw_header(img, text)

    for hl in highlights or []:
        hl_type = hl.get("type", "")
        if hl_type == "circle":
            img = _draw_circle_highlight(img, hl)
        elif hl_type == "arrow":
            img = _draw_arrow_highlight(img, hl)

    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.convert("RGB").save(output_path, "PNG")

    return img.convert("RGB")


def _save_animation(
    pil_frames: list[Image.Image],
    durations: list[int],
    output_path: Path,
    fmt: str = "WEBP",
) -> bool:
    """Save annotated frames as animated GIF or WebP.

    WebP produces much smaller files with 24-bit color (vs GIF's 256 colors)
    and is natively supported in all modern browsers via <img> tag.
    """
    try:
        if fmt == "WEBP":
            pil_frames[0].save(
                output_path,
                save_all=True,
                append_images=pil_frames[1:],
                duration=durations,
                loop=0,
                format="WEBP",
                lossless=False,
                quality=85,
                method=6,  # slowest/best compression
            )
        else:
            # GIF fallback
            gif_frames = []
            for f in pil_frames:
                gif_frames.append(f.convert("P", palette=Image.Palette.ADAPTIVE))
            gif_frames[0].save(
                output_path,
                save_all=True,
                append_images=gif_frames[1:],
                duration=durations,
                loop=0,
                format="GIF",
                optimize=True,
            )
        return True
    except Exception:
        return False


def build_segment_animation(
    frames_dir: str | Path,
    metadata_path: str | Path,
    output_path: str | Path,
    locale: str = "de",
    annotated_dir: str | Path = "",
    fmt: str = "WEBP",
) -> bool:
    """Annotate frames and assemble into an animated WebP or GIF.

    Args:
        frames_dir: Directory containing raw PNG frames.
        metadata_path: Path to frames.json (list of dicts with keys:
                       file, step, duration, highlights).
        output_path: Where to save the animated output.
        locale: Language code ("en" or "de").
        annotated_dir: Directory to save annotated intermediate PNGs.
        fmt: Output format — "WEBP" (default) or "GIF".

    Returns:
        True if the animation was saved, False otherwise.
    """
    try:
        with open(metadata_path) as f:
            frames_meta = json.load(f)
    except Exception:
        return False

    frames_dir = Path(frames_dir)
    annotated_dir = Path(annotated_dir)
    annotated_dir.mkdir(parents=True, exist_ok=True)

    pil_frames = []
    durations = []

    for i, entry in enumerate(frames_meta):
        filename = entry.get("file", "")
        step_label = entry.get("step", "")
        step_number = i + 1
        duration = entry.get("duration", 800)
        highlights = entry.get("highlights", [])

        src = frames_dir / filename
        if not src.exists():
            continue

        annotated_path = annotated_dir / filename
        img = annotate_frame(str(src), step_label, step_number,
                             highlights, locale, str(annotated_path))
        if img is None:
            continue

        try:
            pil_frames.append(img.convert("RGB"))
            durations.append(duration)
        except Exception:
            continue

    if len(pil_frames) < 2:
        return False

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    return _save_animation(pil_frames, durations, output_path, fmt)
