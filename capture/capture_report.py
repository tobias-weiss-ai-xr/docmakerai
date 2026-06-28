import json
import time
from pathlib import Path
from typing import Any


def generate_capture_report(
    results: list[tuple[str, bool, int, str | None, float]],
    assets_dir: Path,
    output_path: Path | None = None,
) -> dict[str, Any]:
    total = len(results)
    succeeded = sum(1 for _, ok, _, _, _ in results if ok)
    failed = total - succeeded
    total_duration = sum(duration for _, _, _, _, duration in results)
    slowest = max(results, key=lambda r: r[4], default=None) if results else None

    report: dict[str, Any] = {
        "total_workflows": total,
        "succeeded": succeeded,
        "failed": failed,
        "success_rate": round(succeeded / max(total, 1) * 100, 1),
        "total_duration_seconds": round(total_duration, 2),
        "slowest_workflow": slowest[0] if slowest else None,
        "slowest_duration_seconds": round(slowest[4], 2) if slowest else 0.0,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "workflows": [],
    }

    for name, ok, frames, error, duration in results:
        webp_path = assets_dir / f"{name}.webp"
        entry: dict[str, Any] = {
            "name": name,
            "status": "ok" if ok else "failed",
            "annotated_frames": frames if ok else 0,
            "duration_seconds": round(duration, 2),
            "file_size_kb": webp_path.stat().st_size // 1024 if ok and webp_path.exists() else 0,
        }
        if error:
            entry["error"] = error
        report["workflows"].append(entry)

    large_files = [w for w in report["workflows"] if w["file_size_kb"] > 200]
    if large_files:
        report["warnings"] = {
            "large_files": [
                {"name": w["name"], "size_kb": w["file_size_kb"]}
                for w in sorted(large_files, key=lambda x: x["file_size_kb"], reverse=True)
            ]
        }

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

    return report


def print_capture_report(report: dict[str, Any]) -> None:
    print(f"\n{'=' * 60}")
    rate = report["success_rate"]
    print(
        f"CAPTURE REPORT: {report['succeeded']}/{report['total_workflows']} succeeded "
        f"({rate}%) in {report.get('total_duration_seconds', 0):.1f}s"
    )

    for w in report["workflows"]:
        mark = "✓" if w["status"] == "ok" else "✗"
        size_info = f", {w['file_size_kb']}KB" if w["file_size_kb"] else ""
        frames_info = f", {w['annotated_frames']} frames" if w["annotated_frames"] else ""
        duration_info = f", {w.get('duration_seconds', 0):.1f}s"
        error_info = f" — {w['error']}" if w.get("error") else ""
        print(f"  {mark} {w['name']}{frames_info}{size_info}{duration_info}{error_info}")

    if "warnings" in report and report["warnings"].get("large_files"):
        print("\n⚠️  Large files (>200KB):")
        for f in report["warnings"]["large_files"]:
            print(f"   {f['name']}: {f['size_kb']}KB")

    print(f"{'=' * 60}")
