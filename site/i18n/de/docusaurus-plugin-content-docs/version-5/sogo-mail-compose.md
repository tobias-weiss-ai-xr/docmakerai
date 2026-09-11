---
title: "E-Mail verfassen und senden"
description: "Erfahren Sie, wie Sie E-Mails in SOGo 5 schreiben, formatieren und versenden"
sidebar_label: "E-Mail verfassen und senden"
---

# E-Mail verfassen und senden

Dieses Tutorial behandelt die Grundlagen des Verfassens und Sendens von E-Mails
über die SOGo 5-Webmail-Oberfläche.

## Voraussetzungen

- Ein SOGo 5-Konto mit gültigen Anmeldedaten
- Sie sind bei SOGo 5 angemeldet

## Schritt-für-Schritt-Anleitung

### Schritt 1: E-Mail-Modul öffnen

Klicken Sie oben in der Navigationsleiste auf **E-Mail**,
um Ihren Posteingang zu öffnen.

![E-Mail-Modul in der Navigationsleiste](./assets/01-mail-inbox.png)

Ihr Posteingang zeigt empfangene Nachrichten in der Hauptansicht, mit Ordnern
(Inbox, Gesendet, Entwürfe, Papierkorb) im linken Bereich.

### Schritt 2: Neue Nachricht beginnen

Klicken Sie auf die Schaltfläche **Verfassen** in der Symbolleiste über Ihrer Nachrichtenliste.

Ein neues Nachrichtenfenster wird geöffnet.

### Schritt 3: Nachricht adressieren

Füllen Sie die Empfängerfelder aus:

| Eingabefeld | Beschreibung |
|------|-------------|
| **An** | Primäre(r) Empfänger. Mehrere Adressen mit Kommas oder Semikolons trennen |
| **Cc** | Kopie — Empfänger erhalten eine Kopie, sichtbar für andere |
| **Bcc** | Blindkopie — Empfänger erhalten eine Kopie, für andere Empfänger verborgen |

**Tipps:**
- Beginnen Sie mit der Eingabe eines Namens — SOGo 5 schlägt passende Kontakte aus Ihrem Adressbuch vor
- Sie können auch vollständige E-Mail-Adressen direkt eingeben
- Verwenden Sie **Cc** für Personen, die informiert werden müssen, aber nicht direkt verantwortlich sind
- Verwenden Sie **Bcc** für Verteilerlisten oder wenn Empfänger einander nicht sehen sollen

### Schritt 4: Betreff eingeben

Geben Sie eine klare, prägnante Betreffzeile in das Feld **Betreff** ein.

:::tip
Gute Betreffzeilen helfen Empfängern, den Zweck Ihrer E-Mail zu verstehen.
Beispiele:
- ❌ "Besprechung"
- ✅ "Sprint-Planung — Dienstag 10:00"
- ❌ "Frage"
- ✅ "Frage zu Kalenderfreigabe-Berechtigungen"
:::

### Schritt 5: Nachricht schreiben

Geben Sie Ihre Nachricht in das große Textfeld ein. Die Symbolleiste bietet
Formatierungsoptionen:

| Schaltfläche | Aktion |
|-------------|--------|
| **B** | Fett |
| *I* | Kursiv |
| **U** | Unterstrichen |
| **Link** | Hyperlink einfügen |
| **Liste** | Aufzählungs- oder nummerierte Liste erstellen |
| **Anhang** 📎 | Datei anhängen |

Um eine Datei anzuhängen:

1. Klicken Sie auf die Schaltfläche **Anhängen** (Büroklammer-Symbol)
2. Wählen Sie eine Datei von Ihrem Computer aus
3. Die Datei wird hochgeladen und als Anhang in Ihrer Nachricht angezeigt

### Schritt 6: Priorität festlegen (Optional)

Wenn Ihre Nachricht zeitkritisch ist, können Sie eine Prioritätsstufe festlegen:

- Klicken Sie auf die Schaltfläche **Priorität** in der Symbolleiste
- Wählen Sie **Niedrig**, **Normal** oder **Hoch**

Nachrichten mit hoher Priorität zeigen ein rotes Ausrufezeichen ❗ im
Posteingang des Empfängers.

### Schritt 7: Nachricht senden

Wenn Ihre Nachricht vollständig ist:

1. Überprüfen Sie Empfänger, Betreff und Inhalt
2. Klicken Sie auf **Senden**

SOGo 5 stellt die Nachricht zu. Eine Kopie wird in Ihrem Ordner **Gesendet** gespeichert.

### Schritt 8: Als Entwurf speichern (Optional)

Wenn Sie noch nicht bereit zum Senden sind:

- Klicken Sie stattdessen auf **Als Entwurf speichern**
- Die Nachricht wird in Ihrem Ordner **Entwürfe** gespeichert
- Um später fortzufahren, öffnen Sie den Ordner Entwürfe und klicken auf die Nachricht

## Fehlerbehebung

### Nachricht wird nicht gesendet

- Überprüfen Sie, ob das Feld **An** mindestens einen gültigen Empfänger enthält
- Große Anhänge können die Server-Größenbeschränkungen überschreiten (in der Regel 25 MB)
- Überprüfen Sie Ihre Internetverbindung

### Empfänger nicht gefunden

- Vergewissern Sie sich, dass die E-Mail-Adresse korrekt ist
- Die automatische Vervollständigung durchsucht Ihre Kontakte, nicht das globale Verzeichnis
- Geben Sie die vollständige E-Mail-Adresse manuell ein

## Fazit

Sie haben erfolgreich eine E-Mail in SOGo 5 verfasst und gesendet. Sie können nun
Ihren Posteingang verwalten, Nachrichten in Ordnern organisieren und E-Mail-Filter
für die automatische Sortierung einrichten.
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
