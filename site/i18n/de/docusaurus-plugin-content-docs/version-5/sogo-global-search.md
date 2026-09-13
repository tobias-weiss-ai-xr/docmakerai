---
title: "Globale Suche"
description: "E-Mails, Kontakte und Kalender in SOGo 5 durchsuchen"
sidebar_label: "Suche"
---

# Suche in SOGo 5

Die Suche in SOGo 5 erfolgt pro Modul: E-Mails durchsuchen Sie im E-Mail-Modul, Kontakte im Adressbuch und Kalenderereignisse im Kalender — jeweils über das Suchfeld der Oberfläche.

## Voraussetzungen

- Ein SOGo 5-Konto mit gültigen Anmeldedaten
- Sie sind bei SOGo 5 angemeldet

## Schritt-für-Schritt-Anleitung

### Schritt 1: Modul öffnen

Es gibt keine zentrale Such-Schaltfläche. Öffnen Sie das Modul, in dem Sie suchen möchten — **E-Mail**, **Kalender** oder **Adressbuch** in der oberen Leiste.

### Schritt 2: Suchbegriff eingeben

Geben Sie Ihren Suchbegriff in das Suchfeld des Moduls ein. Ergebnisse erscheinen während der Eingabe.

### Schritt 3: Ergebnisse durchsuchen

Jedes Modul durchsucht seine eigenen Inhalte:

| Modul | Was durchsucht wird |
|-------|-------------------|
| **E-Mail** | E-Mail-Betreffzeilen und Absendernamen (falls IMAP verfügbar) |
| **Kalender** | Ereignistitel, Orte und Beschreibungen |
| **Kontakte** | Kontaktnamen, E-Mail-Adressen und Telefonnummern |
| **Aufgaben** | Aufgabentitel (falls verfügbar) |

Klicken Sie auf ein beliebiges Ergebnis, um direkt zu diesem Element zu navigieren.

## Suchtipps

| Technik | Beispiel | Ergebnis |
|---------|----------|----------|
| **Teilübereinstimmung** | `Treff` | Findet „Treffen", „Treffpunkt", „Straßentreffen" |
| **Nach Kontaktname** | `Max` | Findet Kontakte namens Max und Ereignisse mit Max |
| **Nach Datum** | `Juni` | Findet Ereignisse und E-Mails aus dem Juni |
| **Nach Ort** | `Konferenz` | Findet Ereignisse im Konferenzraum |
| **Nach Stichwort** | `Rechnung` | Findet alle passenden Elemente mit „Rechnung" |

:::tip
Suchen Sie in dem Modul, in dem Sie das gesuchte Element erwarten — die Ergebnisse werden pro Modul angezeigt.
:::

## Fehlerbehebung

| Problem | Mögliche Ursache | Lösung |
|---------|-----------------|--------|
| Keine Ergebnisse gefunden | Tippfehler im Suchbegriff | Überprüfen Sie die Rechtschreibung oder versuchen Sie ein Teilwort |
| E-Mail-Ergebnisse werden nicht angezeigt | IMAP-Server nicht verfügbar | Die E-Mail-Suche erfordert eine aktive IMAP-Verbindung |
| Ergebnisse laden langsam | Großes Postfach | Grenzen Sie Ihre Suche mit spezifischeren Begriffen ein |

## Fazit

Sie können nun in jedem SOGo-5-Modul gezielt nach E-Mails, Kontakten und Kalenderereignissen suchen.
## Barrierefreiheit

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
