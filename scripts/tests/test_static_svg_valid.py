"""All shipped SVG assets must parse as strict XML.

Regression: the navbar logo once contained `--` inside an XML comment
(`Deep green = --ifm-color-primary`). Chromium rejects the whole SVG
(naturalWidth = 0, logo renders unsized), while Inkscape tolerates it --
so local renders looked fine and only the e2e logo-size gate caught it.
"""

import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

SITE_DIR = Path(__file__).resolve().parents[2] / "site" / "static"

svg_files = sorted(SITE_DIR.rglob("*.svg"))


def test_static_img_dir_exists():
    assert SITE_DIR.is_dir(), f"missing {SITE_DIR}"
    assert svg_files, "no svg assets found - glob broken?"


@pytest.mark.parametrize("svg", svg_files, ids=[str(p.relative_to(SITE_DIR)) for p in svg_files])
def test_svg_parses_as_strict_xml(svg: Path):
    ET.parse(svg)  # raises on `--` in comments, unbalanced tags, bad attrs
