from pathlib import Path

import pytest
from PIL import Image

FIXTURES = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture
def test_png(tmp_path: Path) -> Path:
    """Create a simple 100×100 test PNG with a colored gradient."""
    path = tmp_path / "test.png"
    img = Image.new("RGB", (100, 100))
    for y in range(100):
        for x in range(100):
            img.putpixel((x, y), (x * 2 % 256, y * 2 % 256, 128))
    img.save(path)
    return path


@pytest.fixture
def blank_png(tmp_path: Path) -> Path:
    """Create a blank (all white) 100×100 PNG."""
    path = tmp_path / "blank.png"
    Image.new("RGB", (100, 100), (255, 255, 255)).save(path)
    return path
