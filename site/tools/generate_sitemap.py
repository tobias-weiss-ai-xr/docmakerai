#!/usr/bin/env python3
"""Generate sitemap.xml for ALL locales with hreflang alternates.

Docusaurus's sitemap plugin only sees default-locale routes, so /de/ pages
never make it into sitemap.xml. This script walks the finished build/ tree
and emits one <url> per page with <xhtml:link> alternates for en + de
(x-default -> en), giving the German tree search-engine discovery.

Wired as the npm `postbuild` hook (runs after `npm run build`; a bare
`npx docusaurus build` does not trigger it).

Usage: python3 tools/generate_sitemap.py [--build-dir build] [--base URL]
"""

import argparse
import os
import sys
from pathlib import Path
from urllib.parse import quote

PROD_BASE = "https://tobias-weiss-ai-xr.github.io/docmakerai/"
LOCALES = ("en", "de")  # en is the default locale (no path prefix)


def page_url(rel_html: str, base: str) -> str:
    """build-relative path -> absolute site URL with trailing slash."""
    path = rel_html.replace(os.sep, "/")
    if path.endswith("/index.html"):
        path = path[: -len("index.html")]
    return base + quote(path)


def locale_of(path: str) -> str | None:
    """Classify a URL path as 'de', 'en', or None (non-doc page)."""
    parts = [p for p in path.split("/") if p]
    if not parts:
        return None
    if parts[0] == "de":
        return "de"
    if parts[0] in ("sogo5", "sogo6", "docs"):
        return "en"
    return None


def canonical_key(url_path: str) -> str:
    """Strip the locale dimension so en/de variants group together."""
    return url_path.replace("/docmakerai/de/", "/docmakerai/")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--build-dir", default="build")
    ap.add_argument("--base", default=PROD_BASE)
    args = ap.parse_args()

    build = Path(args.build_dir)
    if not build.is_dir():
        print(f"error: build dir not found: {build}", file=sys.stderr)
        return 1

    groups: dict[str, dict[str, str]] = {}  # key -> {locale: url}
    for html in build.rglob("*.html"):
        rel = html.relative_to(build).as_posix()
        if rel == "404.html" or rel.endswith("/404.html"):
            continue
        text = html.read_text(encoding="utf-8", errors="replace")
        # Mirror Docusaurus: unlisted pages carry a robots noindex meta and
        # must not be advertised in the sitemap.
        if 'content="noindex' in text or "content=noindex" in text:
            continue
        url = page_url(rel, args.base)
        loc = locale_of(url[len(args.base) :])
        if loc is None:
            continue
        groups.setdefault(canonical_key(url), {})[loc] = url

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    per_locale = {loc: 0 for loc in LOCALES}
    for key in sorted(groups):
        variants = groups[key]
        if not variants:
            continue
        # alternates: every available locale + x-default pointing at en
        alts = []
        for loc, url in sorted(variants.items()):
            alts.append(
                f'    <xhtml:link rel="alternate" hreflang="{loc}" href="{url}"/>'
            )
        if "en" in variants:
            alts.append(
                f'    <xhtml:link rel="alternate" hreflang="x-default" '
                f'href="{variants["en"]}"/>'
            )
        for loc, url in sorted(variants.items()):
            per_locale[loc] += 1
            lines.append(f"  <url>")
            lines.append(f"    <loc>{url}</loc>")
            lines.extend(alts)
            lines.append("  </url>")

    lines.append("</urlset>")
    out = build / "sitemap.xml"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    total = sum(per_locale.values())
    print(
        f"sitemap: {total} URLs ({', '.join(f'{l}={n}' for l, n in per_locale.items())}), "
        f"{sum(1 for v in groups.values() if len(v) > 1)} groups with alternates -> {out}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
