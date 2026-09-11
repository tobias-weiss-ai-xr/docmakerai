#!/usr/bin/env python3
"""
Replace the English accessibility section with a German translation in all
DE i18n docs. The English section is identical across all tutorial files:

  ## Accessibility
  ### Keyboard Navigation
  ...
  ### High Contrast Mode
  ...

This script replaces everything from '## Accessibility' to end-of-file
with the German equivalent, but ONLY for the standard SOGo tutorial
accessibility section (not ROADMAP.md which has different content).
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DE_DIRS = [
    REPO_ROOT / "site" / "i18n" / "de" / "docusaurus-plugin-content-docs" / "version-5",
    REPO_ROOT / "site" / "i18n" / "de" / "docusaurus-plugin-content-docs" / "version-6",
]

GERMAN_ACCESSIBILITY = """## Barrierefreiheit

### Tastaturnavigation

Diese Anwendung unterstützt die Tastaturnavigation. Keine Maus erforderlich.

| Aktion | Tastenkombination | Hinweise |
|--------|-------------------|----------|
| Module navigieren | `Tab` / `Umschalt+Tab` | Wechselt zwischen Bereichen |
| Auswählen/Aktivieren | `Eingabetaste` oder `Leertaste` | Link oder Schaltfläche aktivieren |
| Abbrechen/Schließen | `Escape` | Aktuelle Aktion abbrechen |
| Listen navigieren | `Pfeiltasten` | Durch Einträge bewegen |

**Reihenfolge der Screenreader-Navigation:**
1. Modul-Navigation → `Tab` zum Betreten
2. Modulinhalte → `Pfeiltasten` zum Navigieren
3. Aktionsschaltflächen → `Leertaste` oder `Eingabetaste` zum Aktivieren
4. Formulare → `Tab` zwischen Feldern, Pfeiltasten für Dropdowns

### Hochkontrastmodus

SOGo unterstützt den Hochkontrast- und Dunkelmodus. Aktivierung über Benutzereinstellungen oder systemweite Barrierefreiheitseinstellungen:
- **Windows:** `Win+Strg+C` schaltet den Hochkontrast um
- **macOS:** Systemeinstellungen → Bedienungshilfen → Anzeige → Kontrast erhöhen
- **Browser-Erweiterungen:** Dark Reader, High Contrast (Chrome)
"""

# Marker that identifies the standard SOGo tutorial accessibility section
STANDARD_MARKER = "This application supports keyboard navigation"


def main():
    dry_run = "--dry-run" in sys.argv
    total = 0
    for d in DE_DIRS:
        if not d.exists():
            continue
        for md_file in sorted(d.glob("*.md")):
            if md_file.name == "ROADMAP.md":
                continue  # different content, skip
            text = md_file.read_text(encoding="utf-8")
            # Find the standard English accessibility section
            idx = text.find("\n## Accessibility\n")
            if idx == -1:
                continue
            # Check it's the standard one (not ROADMAP-style)
            after = text[idx:]
            if STANDARD_MARKER not in after:
                continue
            # Replace from ## Accessibility to end of file
            new_text = text[:idx] + "\n" + GERMAN_ACCESSIBILITY
            # Ensure file ends with newline
            if not new_text.endswith("\n"):
                new_text += "\n"
            if not dry_run:
                md_file.write_text(new_text, encoding="utf-8")
                print(f"  Translated: {md_file.relative_to(REPO_ROOT)}")
            else:
                print(f"  Would translate: {md_file.relative_to(REPO_ROOT)}")
            total += 1
    print(f"\n{'Would translate' if dry_run else 'Translated'} {total} accessibility sections")


if __name__ == "__main__":
    main()
