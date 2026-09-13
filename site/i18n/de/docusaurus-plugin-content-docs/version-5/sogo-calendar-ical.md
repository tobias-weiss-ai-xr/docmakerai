---
title: "Kalender — Import & Export (iCal)"
description: "Kalender mit dem iCal-Format (.ics) in SOGo 5 importieren und exportieren"
sidebar_label: "Import & Export (iCal)"
---

# Kalender — Import & Export (iCal)

Teilen Sie Ihren Kalender mit anderen, indem Sie ihn als iCal-Datei exportieren, oder importieren Sie Kalender aus anderen Anwendungen in SOGo.

## Voraussetzungen

- Ein SOGo 5-Konto mit gültigen Anmeldedaten
- Sie sind bei SOGo 5 angemeldet

## Schritt-für-Schritt-Anleitung

### Schritt 1: Kalendermodul öffnen

Klicken Sie oben in der Navigationsleiste auf **Kalender**, um die Kalenderansicht zu öffnen.

### Schritt 2: Kalendereinstellungen aufrufen

Klicken Sie auf das **Dreipunkt-Menü** (⋯) in der Kalender-Symbolleiste.

### Schritt 3: Kalender exportieren

1. Öffnen Sie über das Dreipunkt-Menü die Einstellungen des gewünschten Kalenders
2. Wählen Sie die Option zum Exportieren — der Kalender wird als `.ics`-Datei (iCal) heruntergeladen

### Schritt 4: Kalender importieren

1. Klicken Sie auf die Schaltfläche **Import** in den Kalendereinstellungen
2. Wählen Sie die `.ics`-Datei aus, die Sie importieren möchten
3. Wählen Sie den Zielkalender für den Import
4. Klicken Sie auf **Importieren**, um zu beginnen

:::info
iCal (`.ics`) ist ein Standard-Kalenderdateiformat, das von den meisten Kalenderanwendungen unterstützt wird, einschließlich Google Kalender, Microsoft Outlook und Apple Kalender.
:::

## Importoptionen

| Option | Beschreibung | Verwenden wenn |
|--------|-------------|---------------|
| **Alle Ereignisse hinzufügen** | Importiert alle Ereignisse aus der Datei | Erster Import |
| **Duplikate zusammenführen** | Überspringt Ereignisse mit gleichem Datum und Titel | Vorhandenen Kalender aktualisieren |
| **Vorhandene aktualisieren** | Ersetzt Ereignisse mit übereinstimmenden Zeiten | Freigegebenen Kalender aktualisieren |

:::warning
Der Import eines Kalenders mit Hunderten von Ereignissen kann mehrere Minuten dauern. Schließen Sie die Seite nicht, während der Import läuft.
:::

## Freigabe über iCal

Um Ihren Kalender in einer anderen Anwendung (z. B. auf dem Smartphone) zu abonnieren, benötigen Sie die Kalender-URL:

1. Öffnen Sie die Einstellungen des gewünschten Kalenders über das Dreipunkt-Menü
2. Die Kalender-URL finden Sie dort unter **Links zu diesem Kalender** — nicht im Export-Dialog
3. Teilen Sie die URL mit anderen; sie können Ihren Kalender damit in ihrer eigenen Anwendung abonnieren

## Fehlerbehebung

| Problem | Mögliche Ursache | Lösung |
|---------|-----------------|--------|
| Import-Button nicht sichtbar | Kalenderfreigabe nicht aktiviert | Kontaktieren Sie Ihren Administrator, um die Freigabe zu aktivieren |
| Import schlägt fehl | Ungültiges `.ics`-Dateiformat | Überprüfen Sie, ob die Datei in einer Kalenderanwendung geöffnet werden kann |
| Exportdatei ist leer | Kalender hat keine Ereignisse | Fügen Sie vor dem Export Ereignisse zum Kalender hinzu |

## Fazit

Sie haben erfolgreich gelernt, wie Sie Kalender im iCal-Format in SOGo 5 importieren und exportieren.
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
