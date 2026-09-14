from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import imagehash
from PIL import Image

DEFAULT_THRESHOLD = 10
DEFAULT_BASELINES_DIR = Path(__file__).resolve().parent / "baselines"


def compute_phash(image_path: Path) -> str:
    with Image.open(image_path) as img:
        return str(imagehash.phash(img))


def hamming_distance(a: str, b: str) -> int:
    if len(a) != len(b):
        raise ValueError(f"Hash length mismatch: {len(a)} vs {len(b)}")
    return bin(int(a, 16) ^ int(b, 16)).count("1")


def save_baseline(workflow: str, phash: str, baselines_dir: Path = DEFAULT_BASELINES_DIR) -> None:
    baselines_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "workflow": workflow,
        "phash": phash,
        "saved_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (baselines_dir / f"{workflow}.phash.json").write_text(json.dumps(payload, indent=2))


def load_baseline(workflow: str, baselines_dir: Path = DEFAULT_BASELINES_DIR) -> str | None:
    f = baselines_dir / f"{workflow}.phash.json"
    if not f.exists():
        return None
    return json.loads(f.read_text())["phash"]


def find_duplicates(
    image_paths: list[Path], threshold: int = DEFAULT_THRESHOLD
) -> list[tuple[int, Path, Path]]:
    """Return all pairs of images whose phash distance is below threshold.

    Guards against the same UI state being shipped as several "different"
    doc screenshots (e.g. an empty calendar presented as event dialog AND
    freebusy grid).
    """
    hashes = [(p, imagehash.phash(Image.open(p))) for p in image_paths]
    dupes = []
    for i, (p1, h1) in enumerate(hashes):
        for p2, h2 in hashes[i + 1 :]:
            dist = h1 - h2
            if dist < threshold:
                dupes.append((dist, p1, p2))
    return dupes


def detect_drift(
    workflow: str,
    new_phash: str,
    baselines_dir: Path = DEFAULT_BASELINES_DIR,
    threshold: int = DEFAULT_THRESHOLD,
) -> tuple[bool, int | None]:
    baseline = load_baseline(workflow, baselines_dir)
    if baseline is None:
        return True, None
    dist = hamming_distance(baseline, new_phash)
    return dist > threshold, dist


def main() -> int:
    parser = argparse.ArgumentParser(description="Perceptual-hash UI drift detection")
    parser.add_argument("image", type=Path, help="Path to the captured login screenshot")
    parser.add_argument("--workflow", required=True, help="Workflow name (baseline key)")
    parser.add_argument(
        "--baselines-dir",
        type=Path,
        default=DEFAULT_BASELINES_DIR,
        help="Where to store .phash.json files",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=DEFAULT_THRESHOLD,
        help=f"Hamming distance threshold (default: {DEFAULT_THRESHOLD})",
    )
    parser.add_argument(
        "--update-baseline",
        action="store_true",
        help="Overwrite the baseline with the new hash",
    )
    parser.add_argument(
        "--check-drift",
        action="store_true",
        help="Exit 0 if no drift, exit 1 if drift detected",
    )
    args = parser.parse_args()

    new_hash = compute_phash(args.image)
    baseline = load_baseline(args.workflow, args.baselines_dir)

    if baseline is None:
        print(f"No baseline for '{args.workflow}'. Saving new baseline: {new_hash}")
        save_baseline(args.workflow, new_hash, args.baselines_dir)
        return 1 if args.check_drift else 0

    dist = hamming_distance(baseline, new_hash)
    drifted = dist > args.threshold
    print(f"Workflow: {args.workflow}")
    print(f"  Baseline: {baseline}")
    print(f"  Current:  {new_hash}")
    print(f"  Distance: {dist} (threshold: {args.threshold})")
    print(f"  Drifted:  {drifted}")

    if args.update_baseline:
        save_baseline(args.workflow, new_hash, args.baselines_dir)
        print("  Baseline updated.")

    if args.check_drift:
        return 1 if drifted else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
