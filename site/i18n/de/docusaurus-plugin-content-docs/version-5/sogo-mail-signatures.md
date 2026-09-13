---
title: "E-Mail-Signaturen und Identitäten"
description: "E-Mail-Signaturen und mehrere Absenderidentitäten einrichten"
sidebar_label: "E-Mail-Signaturen und Identitäten"
---

# E-Mail-Signaturen und Identitäten

Konfigurieren Sie professionelle E-Mail-Signaturen und verwalten Sie mehrere
Absenderidentitäten (z. B. geschäftlich vs. privat).

## Teil 1: Eine E-Mail-Signatur erstellen

### Schritt 1: Identitätseinstellungen öffnen

1. Klicken Sie auf das Zahnrad-Symbol (**Einstellungen**) in der oberen Symbolleiste
2. Wählen Sie **E-Mail** → **IMAP-Konten**
3. Klicken Sie auf Ihr E-Mail-Konto, um dessen Identität zu bearbeiten

![Signatur-Einstellungen](./assets/01-mail-signatures.png)

### Schritt 2: Neue Identität anlegen

Signaturen werden pro Identität gepflegt — es gibt keinen separaten „Signaturen“-Bereich. Über **Neue Identität** legen Sie eine weitere Identität an.

### Schritt 3: Signatur schreiben

Geben Sie Ihren Signaturtext in das Feld **Signatur** ein. SOGo 5 unterstützt **Klartext**-Signaturen.

**Gebräuchliches Signaturformat an der Universität Marburg:**
```
Mit freundlichen Grüßen
Max Mustermann
Einrichtung / Institut
Philipps-Universität Marburg
Telefon: +49 6421 28-XXXXX
E-Mail: max.mustermann@uni-marburg.de
```

### Schritt 4: Signaturplatzierung wählen

Die Optionen zur Signaturplatzierung finden Sie im Reiter **Allgemein** der Identität — nicht dort, wo Sie die Signatur erstellt haben. Wählen Sie dort, ob und wohin die Signatur beim Verfassen automatisch eingefügt werden soll.

### Schritt 5: Speichern

Klicken Sie auf **Speichern**, um die Änderungen zu übernehmen.

## Teil 2: Signatur verwenden

Ihre Signatur wird beim Verfassen automatisch entsprechend der gewählten
Platzierung eingefügt (Reiter **Allgemein**, siehe Teil 1). Um eine andere
Signatur zu verwenden, wechseln Sie die Identität (siehe Teil 4).

## Teil 3: HTML-Signaturen (Erweitert)

SOGo 5 unterstützt hauptsächlich Klartext-Signaturen. Für reichhaltige Signaturen
mit Bildern oder Formatierung:

1. Erstellen Sie Ihre HTML-Signatur in einem externen Editor
2. Kopieren Sie den formatierten Inhalt (z. B. aus Gmail oder Outlook)
3. Fügen Sie ihn in das Signaturfeld ein — SOGo 5 behält die grundlegende Formatierung

:::tip
**Bewährte Praxis:** Halten Sie Signaturen als Klartext für maximale
Kompatibilität zwischen E-Mail-Programmen.
:::

## Teil 4: Identitäten verwalten und wechseln

Ihre E-Mail-Adresse und Ihre Signatur sind an die Identität gebunden, die Sie in
Teil 1 über **E-Mail** → **IMAP-Konten** bearbeiten. Zusätzliche Behelfsidentitäten
stehen zur Verfügung, wenn Ihr Administrator sie konfiguriert hat
(`SOGoMailAuxiliaryUserAccountsEnabled`).

### Identität beim Verfassen wechseln

Beim Schreiben einer neuen Nachricht:

1. Suchen Sie das Feld **Von** im Verfassen-Fenster
2. Klicken Sie auf das **X** neben Ihrer E-Mail-Adresse
3. Die Auswahl der verfügbaren Identitäten öffnet sich darüber — wählen Sie die gewünschte Identität aus


## Fazit

Signaturen und Identitäten helfen Ihnen, professionell zu kommunizieren.
Richten Sie eine vollständige Signatur ein und fügen Sie bei Bedarf Behelfsidentitäten hinzu,
wenn Sie mehrere E-Mail-Adressen verwalten.
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
