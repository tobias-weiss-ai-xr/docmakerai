---
title: "Kontakte — Import & Export"
description: "Kontakte mit dem vCard-Format in SOGo 5 übertragen"
sidebar_label: "Import & Export"
---

# Kontakte — Import & Export

Migrieren Sie Kontakte zwischen Anwendungen mit vCard-Import/Export.

## Voraussetzungen

- Ein SOGo 5-Konto mit gültigen Anmeldedaten
- Sie sind bei SOGo 5 angemeldet

## Schritt-für-Schritt-Anleitung

### Schritt 1: Kontaktmodul öffnen

Klicken Sie oben in der Navigationsleiste auf **Kontakte**, um das Adressbuch zu öffnen.

### Schritt 2: Dreipunkt-Menü öffnen

Klicken Sie auf das **Dreipunkt-Menü** (⋯) über der Kontaktliste und wählen Sie die gewünschte Aktion (etwa **Exportieren** oder **Importieren**).

### Schritt 3: Kontakte exportieren

1. Wählen Sie **Export** aus dem Dreipunkt-Menü
2. Wählen Sie das zu exportierende Adressbuch aus
3. Die Kontakte werden als `.vcf`-Datei (vCard) heruntergeladen

### Schritt 4: Kontakte importieren

1. Klicken Sie auf **Import** im Dreipunkt-Menü
2. Wählen Sie die `.vcf`-Datei aus, die Sie importieren möchten
3. Wählen Sie das Zieladressbuch aus
4. Wählen Sie, wie mit Duplikaten umgegangen werden soll:
   - **Überspringen** — Duplikate nicht importieren
   - **Aktualisieren** — Vorhandene Kontakte mit importierten Daten ersetzen
   - **Als neu hinzufügen** — Als separaten Kontakt importieren
5. Klicken Sie auf **Importieren**, um zu beginnen

:::info
vCard (`.vcf`) ist das Standardformat zum Teilen von Kontakten zwischen Anwendungen wie Microsoft Outlook, Apple Kontakte, Gmail und mehr.
:::

## Importoptionen

| Duplikatbehandlung | Beschreibung |
|--------------------|-------------|
| **Duplikate überspringen** | Ignoriert Kontakte mit derselben E-Mail-Adresse |
| **Vorhandene aktualisieren** | Überschreibt vorhandene Kontaktdaten mit importierten Informationen |
| **Alle hinzufügen** | Importiert alle Kontakte, erstellt ggf. Duplikate |

## Exportoptionen

| Format | Beschreibung | Typische Größe (100 Kontakte) |
|--------|-------------|-------------------------------|
| **vCard 3.0** | Standard-vCard-Format | ~25 KB |
| **vCard 4.0** | Neueres Format mit erweiterten Feldern | ~30 KB |
| **CSV** | Kommagetrennte Werte für Tabellenkalkulationen | ~15 KB |

:::tip
Um Ihr gesamtes Adressbuch zu sichern, exportieren Sie regelmäßig alle Kontakte in eine vCard-Datei und speichern Sie diese an einem sicheren Ort.
:::

## Fehlerbehebung

| Problem | Mögliche Ursache | Lösung |
|---------|-----------------|--------|
| Import/Export-Aktionen nicht sichtbar | Funktion nicht aktiviert | Kontaktieren Sie Ihren Administrator |
| Import schlägt fehl | Beschädigte vCard-Datei | Öffnen Sie die Datei in einem Texteditor und überprüfen Sie das Format |
| Kontakte erscheinen doppelt | Duplikatbehandlung nicht ausgewählt | Wählen Sie beim Import „Duplikate überspringen" |
| Bestimmte Felder fehlen | Formatinkompatibilität | Konvertieren Sie die vCard in das vCard 3.0-Format und wiederholen Sie den Vorgang |

## Fazit

Sie haben erfolgreich gelernt, wie Sie Kontakte im vCard-Format in SOGo 5 importieren und exportieren.
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
