---
title: "E-Mail-Signaturen und Identitäten"
description: "E-Mail-Signaturen und mehrere Absenderidentitäten einrichten"
sidebar_label: "E-Mail-Signaturen und Identitäten"
---

# E-Mail-Signaturen und Identitäten

Konfigurieren Sie professionelle E-Mail-Signaturen und verwalten Sie mehrere
Absenderidentitäten (z. B. geschäftlich vs. privat).

## Teil 1: Eine E-Mail-Signatur erstellen

### Schritt 1: Einstellungen öffnen

1. Klicken Sie auf das **Dreipunkt-Menü** (⋯) (Einstellungen) in der oberen Symbolleiste
2. Wählen Sie **E-Mail** → **Signaturen**

![Signatur-Einstellungen](./assets/01-mail-signatures.png)

### Schritt 2: Neue Signatur hinzufügen

Klicken Sie auf **Signatur hinzufügen** oder die **+**-Schaltfläche.

### Schritt 3: Signatur schreiben

Geben Sie Ihren Signaturtext ein. SOGo 6 unterstützt **Klartext**-Signaturen.

**Empfohlenes Signaturformat:**
```
Mit freundlichen Grüßen,
Max Mustermann
Projektleiter | Firmenname
Telefon: +49 123 456 789
E-Mail: max.mustermann@firma.com
```

### Schritt 4: Signaturplatzierung wählen

Wählen Sie, wann die Signatur eingefügt wird:

| Option | Verhalten |
|--------|-----------|
| **Nur an neue Nachrichten anhängen** | Signatur wird an neue E-Mails angehängt, nicht an Antworten |
| **An alle Nachrichten anhängen** | Wird sowohl an neue als auch an beantwortete/weitergeleitete Nachrichten angehängt |
| **Keine automatische Einfügung** | Manuelles Einfügen über die Verfassen-Symbolleiste |

### Schritt 5: Als Standard festlegen

Wenn Sie mehrere Signaturen haben, wählen Sie aus, welche standardmäßig verwendet wird.

### Schritt 6: Speichern

Klicken Sie auf **Speichern**, um zu übernehmen.

## Teil 2: Signatur manuell einfügen

Beim Verfassen einer Nachricht können Sie eine Signatur einfügen:

1. Klicken Sie auf die Schaltfläche **Signatur** in der Verfassen-Symbolleiste
2. Wählen Sie aus, welche Signatur eingefügt werden soll
3. Die Signatur wird an der Cursorposition eingefügt

## Teil 3: HTML-Signaturen (Erweitert)

SOGo 6 unterstützt hauptsächlich Klartext-Signaturen. Für reichhaltige Signaturen
mit Bildern oder Formatierung:

1. Erstellen Sie Ihre HTML-Signatur in einem externen Editor
2. Kopieren Sie den formatierten Inhalt (z. B. aus Gmail oder Outlook)
3. Fügen Sie ihn in das Signaturfeld ein — SOGo 6 behält die grundlegende Formatierung

:::tip
**Bewährte Praxis:** Halten Sie Signaturen als Klartext für maximale
Kompatibilität zwischen E-Mail-Programmen.
:::

## Teil 4: Identitäten verwalten

Identitäten ermöglichen es Ihnen, E-Mails von verschiedenen Adressen aus demselben
SOGo 6-Konto zu senden.

### Schritt 1: Einstellungen öffnen

Gehen Sie zu **Einstellungen** → **E-Mail** → **Identitäten**

### Schritt 2: Ihre Identitäten anzeigen

Sie sehen Ihre primäre Identität (die mit Ihrem SOGo 6-Konto verknüpfte
E-Mail-Adresse). Zusätzliche Identitäten können angezeigt werden, wenn sie von
Ihrem Administrator konfiguriert wurden.

### Schritt 3: Hilfsidentität hinzufügen

Wenn von Ihrem Administrator aktiviert (`SOGoMailAuxiliaryUserAccountsEnabled`):

1. Klicken Sie auf **Identität hinzufügen**
2. Geben Sie ein:
   - **Vollständiger Name** — Anzeigename für Empfänger
   - **E-Mail-Adresse** — Die Absenderadresse
   - **Antwort-an-Adresse** — (optional) Abweichende Adresse für Antworten
3. Klicken Sie auf **Speichern**

### Schritt 4: Identität beim Verfassen wechseln

Beim Schreiben einer neuen Nachricht:

1. Suchen Sie das Feld **Von** im Verfassen-Fenster
2. Klicken Sie auf den Dropdown-Pfeil neben Ihrer E-Mail-Adresse
3. Wählen Sie aus, als welche Identität Sie senden möchten

## Beispiel: Geschäftlich + Privat

```
Identität 1 (Standard):
  Name:  Max Mustermann
  E-Mail: max@firma.com
  Signatur: Professionell (Titel, Telefon, Firma)

Identität 2 (Hilfsidentität):
  Name:  Max M.
  E-Mail: max.mustermann@gmail.com
  Signatur: Lässig (nur Name)

Beim Verfassen einer privaten E-Mail zu Identität 2 wechseln.
Geschäftliche E-Mails verwenden standardmäßig Identität 1.
```

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
