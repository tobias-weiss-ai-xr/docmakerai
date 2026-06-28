#!/usr/bin/env python3
"""
DocMaker AI — Local GitHub Runner Setup

Registers this machine as a self-hosted GitHub runner.

Usage:
    GITHUB_TOKEN=ghp_xxx python3 setup_github_runner.py

Environment:
    GITHUB_TOKEN: GitHub Personal Access Token with 'repo' scope (required)
    GITHUB_REPOSITORY: Target repository (default: tobias-weiss-ai-xr/docmakerai)

Runner Labels:
    linux: Platform identifier (required by workflows: runs-on: [self-hosted, linux])
    legions: Custom label for local/legions server identification

Notes:
    - On Legion (192.168.42.42), runner registered as: legions-docmaker-runner
    - Runner auto-starts via systemd user service (after manual svc.sh install)
    - Workdir: ~/actions-runner
    - Requires: gh CLI with authenticated gh auth login

See: https://github.com/actions/runner/releases
"""
import os
import platform
import subprocess
import sys
from pathlib import Path

import requests

# Configuration
TOKEN = os.environ.get("GITHUB_TOKEN")
REPO = os.environ.get("GITHUB_REPOSITORY", "tobias-weiss-ai-xr/docmakerai")
RUNNER_NAME = f"docmakerai-{platform.node()}"
RUNNER_VERSION = "2.319.1"
RUNNER_DIR = Path.home() / "actions-runner"

print("🔧 DocMaker AI — GitHub Runner Setup")
print(f"   Runner name: {RUNNER_NAME}")
print(f"   Repo: {REPO}")
print("   Labels: linux, legions")
print()

# Create runner directory
RUNNER_DIR.mkdir(exist_ok=True)
print(f"📁 Runner directory: {RUNNER_DIR}")

# Download the runner
ARCH = "x64" if platform.machine().lower() == "x86_64" else "arm64"
SYS = platform.system().lower()
filename = f"actions-runner-{SYS}-{ARCH}-{RUNNER_VERSION}.tar.gz"
url = f"https://github.com/actions/runner/releases/download/v{RUNNER_VERSION}/{filename}"

print(f"📥 Downloading: {url}")
response = requests.get(url, stream=True)
response.raise_for_status()

# Download and extract
tarball = RUNNER_DIR / filename
with open(tarball, "wb") as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)

print("📦 Extracting...")
if SYS in ("linux", "darwin"):
    import tarfile
    with tarfile.open(tarball) as tar:
        tar.extractall(RUNNER_DIR)
else:  # Windows
    import zipfile
    with zipfile.ZipFile(tarball, "r") as z:
        z.extractall(RUNNER_DIR)

tarball.unlink()
print(f"   Extracted to: {RUNNER_DIR}")

# Configure the runner
print()
print("⚙️  Configuring runner...")
config_cmd = [
    RUNNER_DIR / "config.sh",
    "--url", f"https://github.com/{REPO}",
    "--token", TOKEN,
    "--name", RUNNER_NAME,
    "--labels", "linux",
    "--labels", "legions",
    "--unattended",
    "--work", str(RUNNER_DIR / "_work"),
]

result = subprocess.run(config_cmd, cwd=RUNNER_DIR, check=False)
if result.returncode != 0:
    print(f"❌ Config failed: exit code {result.returncode}")
    sys.exit(1)

print("✅ Runner configured successfully!")
print()
print("🚀 To start the runner:")
print(f"   cd {RUNNER_DIR}")
print("   ./run.sh")
print()
print("💡 To run as a service (Linux):")
print("   sudo ./svc.sh install")
print("   sudo ./svc.sh start")
print()
print("💡 To run as a service (macOS):")
print("   ./svc.sh install")
print("   ./svc.sh start")
