"""Regression tests for the dual-locale build guard (scripts/verify-dual-locale-build.sh).

Why this matters: building the site as ``docusaurus build --locale en`` followed
by ``docusaurus build --locale de`` does NOT produce a dual-locale artifact.
With a single ``--locale`` CLI option Docusaurus disables automatic baseUrl
localization (see ``@docusaurus/core/lib/commands/build/buildUtils.js``), so the
German pages land on the ROOT baseUrl, wipe the English ones and leave a
German-only build whose postbuild sitemap advertises the German URLs as
``hreflang="en"`` / ``x-default``.

These tests pin the guard to that failure mode: it must reject exactly that
state and accept a genuine dual-locale build (en at the root, de under ``de/``).
"""

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
GUARD = REPO_ROOT / "scripts" / "verify-dual-locale-build.sh"

DUAL_LOCALE_SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://example.com/</loc>
    <xhtml:link rel="alternate" hreflang="en" href="https://example.com/"/>
    <xhtml:link rel="alternate" hreflang="de" href="https://example.com/de/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://example.com/"/>
  </url>
  <url>
    <loc>https://example.com/de/</loc>
    <xhtml:link rel="alternate" hreflang="en" href="https://example.com/"/>
    <xhtml:link rel="alternate" hreflang="de" href="https://example.com/de/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://example.com/"/>
  </url>
</urlset>
"""

# What the postbuild sitemap generator emits for the clobbered build: every URL
# is a German page sitting on the root baseUrl, so it is counted as "en".
GERMAN_ONLY_SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://example.com/</loc>
    <xhtml:link rel="alternate" hreflang="en" href="https://example.com/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://example.com/"/>
  </url>
</urlset>
"""


def write_page(path: Path, lang: str) -> None:
    """Write a minimal Docusaurus-style generated page for the given html lang."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f'<html lang={lang} dir=ltr class="plugin-pages"><body>x</body></html>\n',
        encoding="utf-8",
    )


def dual_locale_build(tmp_path: Path) -> Path:
    """A genuine dual-locale artifact: en at the root, de under build/de/."""
    build = tmp_path / "build"
    write_page(build / "index.html", "en")
    write_page(build / "sogo5" / "mail" / "index.html", "en")
    write_page(build / "de" / "index.html", "de")
    write_page(build / "de" / "sogo5" / "mail" / "index.html", "de")
    (build / "sitemap.xml").write_text(DUAL_LOCALE_SITEMAP, encoding="utf-8")
    return build


def run_guard(build: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(GUARD), str(build)], capture_output=True, text=True, check=False
    )


def test_passes_on_a_dual_locale_build(tmp_path):
    result = run_guard(dual_locale_build(tmp_path))

    assert result.returncode == 0, result.stderr
    assert "dual-locale build ok" in result.stdout


def test_reports_the_locale_page_counts(tmp_path):
    result = run_guard(dual_locale_build(tmp_path))

    assert result.returncode == 0, result.stderr
    assert "en=2 pages" in result.stdout
    assert "de=2 pages" in result.stdout


def test_fails_on_a_build_dir_that_was_never_created(tmp_path):
    result = run_guard(tmp_path / "build")

    assert result.returncode == 1
    assert "build dir not found" in result.stderr


def test_fails_on_a_german_only_build(tmp_path):
    """The regression this guard exists for: `--locale de` clobbers the en pages."""
    build = tmp_path / "build"
    write_page(build / "index.html", "de")
    write_page(build / "sogo5" / "mail" / "index.html", "de")
    (build / "sitemap.xml").write_text(GERMAN_ONLY_SITEMAP, encoding="utf-8")

    result = run_guard(build)

    assert result.returncode == 1
    assert "German locale is missing" in result.stderr


def test_fails_when_the_root_page_is_not_english(tmp_path):
    build = dual_locale_build(tmp_path)
    write_page(build / "index.html", "de")

    result = run_guard(build)

    assert result.returncode == 1
    assert "expected 'en'" in result.stderr
    assert "single-locale build" in result.stderr


def test_fails_when_the_german_tree_is_empty(tmp_path):
    build = dual_locale_build(tmp_path)
    for page in (build / "de").rglob("*.html"):
        page.unlink()

    result = run_guard(build)

    assert result.returncode == 1
    assert "0 German pages" in result.stderr


def test_fails_when_the_english_tree_is_empty(tmp_path):
    build = dual_locale_build(tmp_path)
    (build / "index.html").unlink()
    (build / "sogo5" / "mail" / "index.html").unlink()

    result = run_guard(build)

    assert result.returncode == 1
    assert "0 English pages" in result.stderr


def test_fails_when_the_sitemap_has_no_german_alternates(tmp_path):
    build = dual_locale_build(tmp_path)
    (build / "sitemap.xml").write_text(GERMAN_ONLY_SITEMAP, encoding="utf-8")

    result = run_guard(build)

    assert result.returncode == 1
    assert 'no hreflang="de" alternates' in result.stderr


def test_fails_when_the_sitemap_is_missing(tmp_path):
    build = dual_locale_build(tmp_path)
    (build / "sitemap.xml").unlink()

    result = run_guard(build)

    assert result.returncode == 1
    assert "sitemap.xml" in result.stderr


def test_fails_when_the_sitemap_omits_the_german_urls(tmp_path):
    build = dual_locale_build(tmp_path)
    sitemap = DUAL_LOCALE_SITEMAP.replace(
        "<loc>https://example.com/de/</loc>", "<loc>https://example.com/</loc>"
    )
    (build / "sitemap.xml").write_text(sitemap, encoding="utf-8")

    result = run_guard(build)

    assert result.returncode == 1
    assert "no /de/ <loc> entries" in result.stderr
