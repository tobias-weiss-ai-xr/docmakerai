"""Gate: shipped doc assets must not contain near-duplicate screenshots.

Several docs once shipped the identical empty-calendar screenshot under
different names ("event dialog", "freebusy grid", "recurrence options" ...).
This test fails if any two PNGs in a shipped asset directory are perceptually
near-identical (phash distance < 10), forcing each doc figure to show its own
distinct UI state.

Covers only what the site actually publishes: versioned_docs and the i18n
tree. site/docs/ is unrouted pipeline scratch (includeCurrentVersion: false)
and is deliberately excluded.

Tolerance: pairs where BOTH files are sogo5-mockup placeholders (provenance)
are allowed — those dirs are slated for wholesale replacement by live
captures and their internal similarity is a known property of mockups.
Every live capture (sogo5-live / sogo6-live / shared) must be unique.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from capture.detect_changes import DEFAULT_THRESHOLD, find_duplicates  # noqa: E402

V5_BLOCKED = (
    "Known v5 duplicate cluster (same empty calendar shipped as event dialog, "
    "freebusy grid, recurrence options, ...). Re-capture blocked: no SOGo 5 "
    "instance available (demo.sogo.nu rejects demo/demo; local docker stack "
    "removed). Stand up a SOGo 5 demo stack, re-capture with "
    "capture/run_screenshot_captures.py helpers, then remove this xfail."
)

# Old run_screenshot_captures.py output in version-6 EN, shipped before the
# verify-then-shoot mechanism existed: several of these are the SAME broken
# empty-UI capture (calendar-edit-delete == calendar-ical == calendar-share
# == calendar-subscribe == contacts-edit-delete, phash distance 0). They are
# gated OUT until each workflow is ported to the hard-fail helpers and
# re-captured live (selector discovery against demov6.sogo.nu per module).
# Remove a name from this set when its re-capture lands — the gate then
# covers it again.
BROKEN_V6_LEGACY = {
    "calendar-edit-delete.png",
    "calendar-subscribe.png",
    "calendar-share.png",
    "calendar-views.png",
    "calendar-ical.png",
    "contacts-add.png",
    "contacts-edit-delete.png",
    "contacts-import-export.png",
    "global-search.png",
    "logout.png",
    "mail-compose.png",
    "mail-filters.png",
    "mail-folder-management.png",
    "mail-read.png",
    "mail-reply-forward-delete.png",
    "mail-signatures.png",
    "password-change.png",
    "preferences.png",
    "vacation.png",
}

ASSET_DIRS = sorted(
    str(p.relative_to(ROOT))
    for p in [
        *ROOT.glob("site/versioned_docs/version-*/assets"),
        *ROOT.glob("site/i18n/*/docusaurus-plugin-content-docs/version-*/assets"),
    ]
    if p.is_dir()
)


def _provenance() -> dict:
    f = ROOT / "site" / "image-provenance.json"
    if not f.exists():
        return {}
    return json.loads(f.read_text()).get("assets", {})


@pytest.mark.parametrize("asset_dir", ASSET_DIRS)
def test_no_near_duplicate_assets(asset_dir: str, request) -> None:
    if "/version-5/" in f"/{asset_dir}/":
        request.applymarker(pytest.mark.xfail(strict=True, reason=V5_BLOCKED))

    base = ROOT / asset_dir
    pngs = sorted(base.glob("*.png"))
    assert pngs, f"{asset_dir} contains no screenshots"
    if asset_dir.endswith("version-6/assets"):
        pngs = [p for p in pngs if p.name not in BROKEN_V6_LEGACY]

    prov = _provenance()

    def is_mockup(p: Path) -> bool:
        # asset_dir is relative to repo root ("site/..."), provenance keys
        # are relative to site/ ("versioned_docs/...", "i18n/...")
        rel = str(Path(asset_dir).relative_to("site") / p.name)
        return prov.get(rel, {}).get("kind") == "sogo5-mockup"

    dupes = find_duplicates(pngs, threshold=DEFAULT_THRESHOLD)
    # Mockup-vs-mockup similarity is tolerated; anything touching a live
    # capture must be unique.
    live_dupes = [(d, a, b) for d, a, b in dupes if not (is_mockup(a) and is_mockup(b))]
    assert not live_dupes, (
        f"{asset_dir}: {len(live_dupes)} near-duplicate screenshot pair(s) — "
        "each doc figure must show a distinct UI state:\n"
        + "\n".join(f"  dist={d}: {a.name} <-> {b.name}" for d, a, b in live_dupes)
    )
