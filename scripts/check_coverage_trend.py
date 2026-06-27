#!/usr/bin/env python3
"""Fail the PR if coverage drops more than --max-drop percent vs the baseline.

Reads two coverage.xml files (Cobertura format), extracts line-rate, and exits
non-zero if PR coverage is more than max-drop percent below the baseline.

Usage:
    python3 scripts/check_coverage_trend.py \\
        --baseline <path/to/baseline-coverage.xml> \\
        --pr <path/to/pr-coverage.xml> \\
        --max-drop 0.5
"""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def extract_line_rate(xml_path: Path) -> float:
    tree = ET.parse(xml_path)
    root = tree.getroot()
    rate = root.attrib.get("line-rate")
    if rate is None:
        raise ValueError(f"No line-rate attribute in {xml_path}")
    return float(rate) * 100.0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True, type=Path,
                        help="Path to baseline coverage.xml (e.g. from main)")
    parser.add_argument("--pr", required=True, type=Path,
                        help="Path to PR coverage.xml")
    parser.add_argument("--max-drop", required=True, type=float,
                        help="Maximum allowed coverage drop in percent points")
    args = parser.parse_args()

    try:
        baseline = extract_line_rate(args.baseline)
        pr = extract_line_rate(args.pr)
    except (ET.ParseError, ValueError, OSError) as exc:
        print(f"::error::{exc}", file=sys.stderr)
        return 2

    drop = baseline - pr
    print(f"Baseline coverage: {baseline:.2f}%")
    print(f"PR coverage:       {pr:.2f}%")
    print(f"Drop:              {drop:.2f} pp (max allowed: {args.max_drop} pp)")

    if drop > args.max_drop:
        print(
            f"::error::Coverage dropped by {drop:.2f} pp, exceeds threshold of "
            f"{args.max_drop} pp. Add tests for new code before merging.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
