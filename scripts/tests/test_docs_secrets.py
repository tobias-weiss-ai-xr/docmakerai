"""No internal data may leak into the published docs corpus.

The docmakerai repository and the built site are PUBLIC. Everything an
internal eval stack considers private — credentials, RFC1918 addresses,
internal hostnames, ops commands, internal AI-infra endpoints, internal
account display names — must never appear in published content, and the
eval password must never appear anywhere in the tree (history aside).

Scope rules:
- PUBLISHED dirs (site/docs, site/suite-docs, site/versioned_docs,
  site/i18n, site/src, site/static, site/*.ts/*.json config, provenance):
  strictest set — no passwords, no internal IPs/hostnames, no ops
  commands, no internal endpoints, no internal account names.
- DEV tooling (capture/, scripts/, tests elsewhere): the eval password
  stays forbidden (env-only); dev usernames inside URL fragments of
  tooling configs are tolerated.
- This test file is exempt from its own patterns (it names them).
"""

import re
from pathlib import Path

SITE = Path(__file__).resolve().parents[2] / "site"

PUBLISHED_DIRS = [
    SITE / "docs",
    SITE / "suite-docs",
    SITE / "versioned_docs",
    SITE / "i18n",
    SITE / "src",
    SITE / "static",
]
PUBLISHED_FILES = [
    SITE / "docusaurus.config.ts",
    SITE / "sidebars.ts",
    SITE / "suite-sidebars.ts",
    SITE / "image-provenance.json",
]

# ── Pattern catalogue ──────────────────────────────────────────────────────
# Built by concatenation so this file itself does not carry the literals
# in greppable form.
_PASSWORD = "eval" + "2026"
_TESTUSER_URL = re.compile(r"/u/testuser")  # public booking page URL: allowed
_USERNAME_BARE = "testuser"

_FORBIDDEN_EVERYWHERE = [
    (_PASSWORD, "eval-stack password literal"),
]

_FORBIDDEN_PUBLISHED = [
    # credentials & internal accounts
    (_PASSWORD, "eval-stack password literal"),
    (re.compile(r"(?<!/u/)\btestuser\b", re.IGNORECASE), "internal eval username (prose)"),
    ("Test User User", "internal eval account display name"),
    # RFC1918 / internal addressing
    (re.compile(r"\b192\.168\.\d{1,3}\.\d{1,3}\b"), "RFC1918 address"),
    (re.compile(r"\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"), "RFC1918 address"),
    (re.compile(r"\b172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}\b"), "RFC1918 address"),
    # internal hostnames & runner topology
    (re.compile(r"\blegions?\b", re.IGNORECASE), "internal runner hostname"),
    ("legions-docmaker-runner", "internal runner service"),
    # ops commands in user-facing docs
    (re.compile(r"^\s*(kubectl|argocd|helm)\s", re.MULTILINE), "ops command"),
    # internal AI infrastructure
    ("api.z.ai", "internal AI endpoint"),
    ("litellm", "internal AI proxy"),
    (re.compile(r"\bglm-[\w.-]+", re.IGNORECASE), "internal model id"),
]


def _iter_published_files():
    for d in PUBLISHED_DIRS:
        if not d.exists():
            continue
        for f in sorted(d.rglob("*")):
            if f.is_file() and f.suffix in {
                ".md", ".mdx", ".ts", ".tsx", ".json", ".css", ".html", ".txt"
            }:
                yield f
    for f in PUBLISHED_FILES:
        if f.exists():
            yield f


def _dev_files():
    root = SITE.parent
    for sub in ("capture", "scripts", "docs", ".github", ".forgejo"):
        d = root / sub
        if not d.exists():
            continue
        for f in sorted(d.rglob("*")):
            if f.is_file() and f.suffix in {".py", ".yml", ".yaml", ".mjs", ".sh", ".ts", ".json"}:
                if "test_docs_secrets" in f.name:
                    continue
                yield f


def test_no_password_anywhere_in_tree():
    """The eval password must never sit in any tracked file (env-only)."""
    bad = []
    for f in list(_iter_published_files()) + list(_dev_files()):
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if _PASSWORD in text:
            bad.append(str(f))
    assert not bad, "eval password literal found in: " + ", ".join(bad)


def test_no_internal_data_in_published_content():
    """Published docs/config must not disclose internal infrastructure."""
    bad = []
    for f in _iter_published_files():
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pat, why in _FORBIDDEN_PUBLISHED:
            rx = re.compile(pat) if isinstance(pat, str) else pat
            for m in rx.finditer(text):
                # public booking-URL username is the one allowed testuser form
                if why.startswith("internal eval username") and _TESTUSER_URL.search(
                    text[max(0, m.start() - 3) : m.end() + 1]
                ):
                    continue
                ctx = text[max(0, m.start() - 40) : m.end() + 40].replace("\n", " ")
                bad.append(f"{f.relative_to(SITE.parent)}: [{why}] …{ctx}…")
                break  # one hit per pattern per file is enough signal
    assert not bad, "internal data leaked into published content:\n" + "\n".join(bad)


def test_no_internal_hostnames_in_build_output():
    """The built site (if present) must be leak-free too."""
    build = SITE / "build"
    if not build.exists():
        return
    bad = []
    for f in sorted(build.rglob("*.html")):
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pat, why in _FORBIDDEN_PUBLISHED[2:6]:  # IP + hostname + display name
            rx = re.compile(pat) if isinstance(pat, str) else pat
            if rx.search(text):
                bad.append(f"{f.relative_to(build)}: {why}")
                break
    assert not bad, "internal data in built site:\n" + "\n".join(bad)
