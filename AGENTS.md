# Schreib-Leitlinien für SOGo-Anleitungen

## Barrierefreiheits-Abschnitte (Screenreader)

Quelle: Review „Sogo mit Screenreader.docx" (J. Bauer).

- **Keine Tab-für-Tab-Pfade beschreiben.** Die Tab-Reihenfolge hängt von Browser,
  Instanz und Screenreader-Einstellungen ab. Stattdessen: Felder benennen und die
  grundsätzliche Reihenfolge beschreiben („Das Ziel ist das Ziel"). Formulierung:
  „`Tab` (ggf. mehrfach), bis Sie hören: ‚…'" statt „`Tab` aus der Adressleiste".
- **Keine Vorhersagen über Ansagen beim Laden.** Ob ein Screenreader die Seite
  automatisch vorliest, hängt von dessen Einstellungen ab. Verlässlicher Einstieg:
  `Strg+Pos1` / `Ctrl+Home`, dann per Navigation erschließen. Statt „Screen reader
  announces: X" → „You should hear: X" (EN) / „Sie hören: X" (DE).
- **NVDA-Hinweis zentral statt wiederholt** (siehe sogo-login): Lesemodus vs.
  Fokusmodus und Sprungnavigation mit `h` gelten dokumentweit.
- Escape verlässt den Fokusmodus des Screenreaders und löscht in der Regel
  keine Formulareingaben — nicht als „Abbrechen/leeren" dokumentieren.
