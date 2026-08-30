#!/usr/bin/env python3
"""Translation coverage report: which pages lack a German translation?

Compares the English versioned docs against the German i18n tree and
prints a plain-text report: missing translations (en -> de), stale
orphans (de page whose English source is gone), and totals per version.

Report only — always exits 0. The maintainer decides what to translate.

Usage: python3 tools/de_coverage.py [locale]   # locale defaults to 'de'
"""

import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
DOC_EXTS = (".md", ".mdx")


def collect(root: Path) -> set[str]:
    return {
        p.relative_to(root).as_posix()
        for p in root.rglob("*")
        if p.suffix in DOC_EXTS
    }


def main() -> int:
    locale = sys.argv[1] if len(sys.argv) > 1 else "de"
    i18n_docs = SITE / "i18n" / locale / "docusaurus-plugin-content-docs"
    if not i18n_docs.is_dir():
        print(f"error: no i18n tree for locale '{locale}': {i18n_docs}", file=sys.stderr)
        return 1

    en_root = SITE / "versioned_docs"
    versions = sorted(p.name for p in en_root.iterdir() if p.is_dir())

    grand_missing = 0
    for version in versions:
        en = collect(en_root / version)
        de_root = i18n_docs / version
        de = collect(de_root) if de_root.is_dir() else set()

        missing = sorted(en - de)
        orphans = sorted(de - en)

        print(f"\n== {version} vs {locale} ==")
        print(f"   en pages: {len(en)}   {locale} pages: {len(de)}")
        if missing:
            print(f"   missing {locale} translations ({len(missing)}):")
            for m in missing:
                print(f"     - {m}")
        if orphans:
            print(f"   stale {locale} pages without en source ({len(orphans)}):")
            for o in orphans:
                print(f"     - {o}")
        if not missing and not orphans:
            print("   fully translated, no orphans")
        grand_missing += len(missing)

    print(
        f"\nsummary: {grand_missing} missing {locale} translation(s) "
        f"across {len(versions)} version(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
