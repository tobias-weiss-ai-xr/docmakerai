"""Regression tests for the site sitemap generator (site/tools/generate_sitemap.py).

The generator exists to give the German tree search-engine discovery that the
Docusaurus sitemap plugin cannot provide (it only sees default-locale routes):
it walks the finished build/ tree and emits one ``<url>`` per locale variant of
every route, each carrying ``hreflang`` alternates for en + de and
``x-default`` -> en.

These tests pin that contract against a synthetic build tree, including the
exclusion rules (404 pages, robots-noindex pages, non-doc route bases) and the
``--base`` flag: locale grouping must work for any base URL, not only the
production one.
"""

import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
GENERATOR = REPO_ROOT / "site" / "tools" / "generate_sitemap.py"

NS = {
    "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
    "xh": "http://www.w3.org/1999/xhtml",
}

PROD_BASE = "https://tobias-weiss-ai-xr.github.io/docmakerai/"

# Route suffixes that make_build() provides in both locales.
ROUTE_SUFFIXES = ("", "sogo5/mail/", "suite/overview/")


def write_page(path: Path, body: str = "<body>x</body>") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"<html><head></head>{body}</html>\n", encoding="utf-8")


def make_build(tmp_path: Path) -> Path:
    """A miniature dual-locale build tree: en at the root, de under build/de/."""
    build = tmp_path / "build"
    # translatable doc pages (one group per route, en + de each)
    for suffix in ROUTE_SUFFIXES:
        write_page(build / suffix / "index.html")
        write_page(build / "de" / suffix / "index.html")
    # excluded by design: 404 pages, robots-noindex pages, non-doc routes
    write_page(build / "404.html")
    write_page(build / "sogo5" / "404" / "index.html")
    write_page(
        build / "sogo5" / "unlisted" / "index.html",
        '<meta name="robots" content="noindex, nofollow">',
    )
    write_page(build / "clips" / "video" / "index.html")
    return build


def run_generator(build: Path, base: str) -> tuple[str, str]:
    result = subprocess.run(
        [sys.executable, str(GENERATOR), "--build-dir", str(build), "--base", base],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout, result.stderr


def sitemap_urls(build: Path) -> list[ET.Element]:
    tree = ET.fromstring((build / "sitemap.xml").read_text(encoding="utf-8"))
    return tree.findall("sm:url", NS)


def locs(urls: list[ET.Element]) -> list[str]:
    return [u.find("sm:loc", NS).text for u in urls]


def hreflangs(url: ET.Element) -> dict[str, str]:
    return {link.attrib["hreflang"]: link.attrib["href"] for link in url.findall("xh:link", NS)}


def expected_urls(base: str) -> set[str]:
    """One <url> per locale variant of every route: {base, base+de, ...}."""
    return {f"{base}{s}" for s in ROUTE_SUFFIXES} | {f"{base}de/{s}" for s in ROUTE_SUFFIXES}


def test_advertises_every_translatable_route_in_both_locales(tmp_path):
    build = make_build(tmp_path)

    stdout, stderr = run_generator(build, PROD_BASE)

    assert stderr == ""
    assert set(locs(sitemap_urls(build))) == expected_urls(PROD_BASE)
    assert "en=3, de=3" in stdout
    assert "3 groups with alternates" in stdout


def test_emits_hreflang_alternates_and_x_default_for_every_url(tmp_path):
    build = make_build(tmp_path)

    run_generator(build, PROD_BASE)

    for url in sitemap_urls(build):
        loc = url.find("sm:loc", NS).text
        suffix = loc.removeprefix(PROD_BASE)
        if suffix.startswith("de/"):
            suffix = suffix[len("de/") :]
        alts = hreflangs(url)
        assert alts == {
            "en": f"{PROD_BASE}{suffix}",
            "de": f"{PROD_BASE}de/{suffix}",
            "x-default": f"{PROD_BASE}{suffix}",
        }, loc


def test_excludes_404_and_noindex_pages(tmp_path):
    build = make_build(tmp_path)

    run_generator(build, PROD_BASE)

    advertised = " ".join(locs(sitemap_urls(build)))
    assert "404" not in advertised
    assert "unlisted" not in advertised


def test_excludes_non_doc_route_bases(tmp_path):
    build = make_build(tmp_path)

    run_generator(build, PROD_BASE)

    assert "clips" not in " ".join(locs(sitemap_urls(build)))


def test_groups_locales_for_a_custom_base_url(tmp_path):
    """--base must not break en/de grouping (it is a documented CLI option)."""
    build = make_build(tmp_path)
    base = "https://example.org/site/"

    stdout, stderr = run_generator(build, base)

    assert stderr == ""
    assert set(locs(sitemap_urls(build))) == expected_urls(base)
    for url in sitemap_urls(build):
        alts = hreflangs(url)
        loc = url.find("sm:loc", NS).text
        suffix = loc.removeprefix(base)
        if suffix.startswith("de/"):
            suffix = suffix[len("de/") :]
        assert alts["de"] == f"{base}de/{suffix}", loc
        assert alts["x-default"] == f"{base}{suffix}", loc
    assert "3 groups with alternates" in stdout


def test_normalizes_a_base_url_without_a_trailing_slash(tmp_path):
    build = make_build(tmp_path)

    run_generator(build, "https://example.org/site")

    assert set(locs(sitemap_urls(build))) == expected_urls("https://example.org/site/")


def test_fails_when_the_build_dir_is_missing(tmp_path):
    result = subprocess.run(
        [sys.executable, str(GENERATOR), "--build-dir", str(tmp_path / "nope")],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "build dir not found" in result.stderr
