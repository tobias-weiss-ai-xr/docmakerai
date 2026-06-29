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

Klicken Sie in der Seitenleiste auf **Kontakte**, um das Adressbuch zu öffnen.

### Schritt 2: Aktionsmenü aufrufen

Klicken Sie auf die Schaltfläche **Aktionen** (oft ein nach unten zeigender Pfeil oder drei Punkte) in der Nähe des oberen Bereichs der Kontaktliste.

### Schritt 3: Kontakte exportieren

1. Wählen Sie **Export** aus dem Aktionsmenü
2. Wählen Sie das zu exportierende Adressbuch aus
3. Die Kontakte werden als `.vcf`-Datei (vCard) heruntergeladen

### Schritt 4: Kontakte importieren

1. Klicken Sie auf **Import** im Aktionsmenü
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

| Duplikatbehandlung: Description | Beschreibung |
|--------------------|-------------|
| **Duplikate überspringen** | Ignoriert Kontakte mit derselben E-Mail-Adresse |
| **Vorhandene aktualisieren** | Überschreibt vorhandene Kontaktdaten mit importierten Informationen |
| **Alle hinzufügen** | Importiert alle Kontakte, erstellt ggf. Duplikate |

## Exportoptionen

| Format: Description | Beschreibung | Typische Größe (100 Kontakte) |
|--------|-------------|-------------------------------|
| **vCard 3.0** | Standard-vCard-Format | ~25 KB |
| **vCard 4.0** | Neueres Format mit erweiterten Feldern | ~30 KB |
| **CSV** | Kommagetrennte Werte für Tabellenkalkulationen | ~15 KB |

:::tip
Um Ihr gesamtes Adressbuch zu sichern, exportieren Sie regelmäßig alle Kontakte in eine vCard-Datei und speichern Sie diese an einem sicheren Ort.
:::

## Fehlerbehebung

| Problem: Description | Mögliche Ursache | Lösung |
|---------|-----------------|--------|
| Import/Export-Aktionen nicht sichtbar | Funktion nicht aktiviert | Kontaktieren Sie Ihren Administrator |
| Import schlägt fehl | Beschädigte vCard-Datei | Öffnen Sie die Datei in einem Texteditor und überprüfen Sie das Format |
| Kontakte erscheinen doppelt | Duplikatbehandlung nicht ausgewählt | Wählen Sie beim Import „Duplikate überspringen" |
| Bestimmte Felder fehlen | Formatinkompatibilität | Konvertieren Sie die vCard in das vCard 3.0-Format und wiederholen Sie den Vorgang |

## Fazit

Sie haben erfolgreich gelernt, wie Sie Kontakte im vCard-Format in SOGo 5 importieren und exportieren.
## Accessibility

### Keyboard Navigation

This application supports keyboard navigation. No mouse required for completing this task.

| Action | Keyboard Shortcut: What key to press | Notes: Additional information |
|--------|--------------------------------------|------------------------------|
| | Navigate modules | `Tab` / `Shift+Tab` | Cycles through sections |
| | Select/activate | `Enter` or `Space` | Activate button or link |
| | Cancel/close | `Escape` | Cancel current action |
| | Navigate lists | `Arrow keys` | Move through items |

**Screen Reader Navigation Order:**
1. Sidebar navigation → `Tab` to enter
2. Module content → `Arrow keys` to navigate
3. Action buttons → `Space` or `Enter` to activate
4. Forms → `Tab` between fields, arrows for dropdowns

### High Contrast Mode

SOGo supports high contrast and dark mode. Toggle via user preferences or use browser/OS-level accessibility settings:
- **Windows:** `Win+Ctrl+C` toggles high contrast
- **macOS:** System Preferences → Accessibility → Display → Increase contrast
- **Browser Extensions:** Dark Reader, High Contrast (Chrome)

