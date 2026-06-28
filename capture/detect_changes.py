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
        "--baselines-dir", type=Path, default=DEFAULT_BASELINES_DIR,
        help="Where to store .phash.json files",
    )
    parser.add_argument(
        "--threshold", type=int, default=DEFAULT_THRESHOLD,
        help=f"Hamming distance threshold (default: {DEFAULT_THRESHOLD})",
    )
    parser.add_argument(
        "--update-baseline", action="store_true",
        help="Overwrite the baseline with the new hash",
    )
    parser.add_argument(
        "--check-drift", action="store_true",
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
