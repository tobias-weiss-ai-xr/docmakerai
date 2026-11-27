#!/usr/bin/env bash
# verify-dual-locale-build.sh — assert that site/build is a real dual-locale
# artifact (English at the root, German under build/de/).
#
# Why this guard exists: when the CLI is handed a single --locale option,
# Docusaurus disables automatic baseUrl localization (see
# @docusaurus/core/lib/commands/build/buildUtils.js). A build invoked as
# `docusaurus build --locale de` therefore emits the German pages at the ROOT
# baseUrl (/docmakerai/) instead of /docmakerai/de/. Building `--locale en`
# and then `--locale de` into the same out-dir consequently leaves a
# German-only build behind: the English pages are silently clobbered, and the
# postbuild sitemap labels the German URLs as hreflang="en"/x-default.
#
# A correct dual-locale build (a plain `npm run build`, as used by
# .github/workflows/deploy.yml) yields en at the root and de under build/de/.
# This script fails loudly when that is not the case, so a build that silently
# degenerated into a single locale can never pass a gate.
#
# Usage: scripts/verify-dual-locale-build.sh [build-dir]
# Exit status: 0 when the artifact is dual-locale, 1 otherwise.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD="${1:-$ROOT/site/build}"
BUILD="${BUILD%/}"

fail() {
  echo "verify-dual-locale-build: $1" >&2
  exit 1
}

count_html() {
  # count_html <dir> [prune-dir] — number of *.html files, minus a pruned tree.
  if [ "$#" -ge 2 ]; then
    find "$1" -name '*.html' -not -path "$2/*" -print
  else
    find "$1" -name '*.html' -print
  fi | wc -l | tr -d '[:space:]'
}

html_lang() {
  # lang=".." attribute of the first <html ...> tag of a generated page.
  grep -oE '<html [^>]*' "$1" | head -1 | grep -oE 'lang=[^ >]+' |
    head -1 | cut -d= -f2 | tr -d '"'
}

[ -d "$BUILD" ] || fail "build dir not found: $BUILD (run the site build first)"

[ -d "$BUILD/de" ] ||
  fail "no '$BUILD/de' directory — the German locale is missing from the build"

en_pages="$(count_html "$BUILD" "$BUILD/de")"
de_pages="$(count_html "$BUILD/de")"

[ "$en_pages" -gt 0 ] ||
  fail "0 English pages under $BUILD (excluding de/) — the English locale was clobbered or never built"
[ "$de_pages" -gt 0 ] ||
  fail "0 German pages under $BUILD/de — the German locale was never built"

en_root="$BUILD/index.html"
de_root="$BUILD/de/index.html"
[ -f "$en_root" ] || fail "missing $en_root"
[ -f "$de_root" ] || fail "missing $de_root"

en_lang="$(html_lang "$en_root")"
de_lang="$(html_lang "$de_root")"
[ "$en_lang" = "en" ] ||
  fail "$en_root is lang='$en_lang', expected 'en' — a single-locale build wrote a non-English site to the root baseUrl"
[ "$de_lang" = "de" ] ||
  fail "$de_root is lang='$de_lang', expected 'de'"

sitemap="$BUILD/sitemap.xml"
[ -f "$sitemap" ] || fail "missing $sitemap (the postbuild hook did not run)"

# grep -c exits 1 on a zero count, which `set -e` would treat as a hard error.
de_alts="$(grep -c 'hreflang="de"' "$sitemap" || true)"
en_alts="$(grep -c 'hreflang="en"' "$sitemap" || true)"
xd_alts="$(grep -c 'hreflang="x-default"' "$sitemap" || true)"

[ "$de_alts" -gt 0 ] ||
  fail "sitemap.xml advertises no hreflang=\"de\" alternates — German pages are not discoverable"
[ "$en_alts" -gt 0 ] ||
  fail "sitemap.xml advertises no hreflang=\"en\" alternates"
[ "$xd_alts" -gt 0 ] ||
  fail "sitemap.xml advertises no hreflang=\"x-default\" alternate"
grep -q '<loc>[^<]*/de/' "$sitemap" ||
  fail "sitemap.xml contains no /de/ <loc> entries — the German tree is absent"

echo "dual-locale build ok: en=$en_pages pages, de=$de_pages pages," \
  "sitemap alternates en=$en_alts de=$de_alts x-default=$xd_alts"
