---
title: "Abwesenheitsnotiz"
description: "Automatische E-Mail-Antworten und Kalenderblöcke für Ihre Abwesenheit einrichten"
sidebar_label: "Abwesenheitsnotiz"
---

# Abwesenheitsnotiz

Konfigurieren Sie automatische E-Mail-Antworten und markieren Sie sich im
Kalender als abwesend, wenn Sie im Urlaub oder außer Haus sind.

## Voraussetzungen

- Ein SOGo 5-Konto mit gültigen Anmeldedaten
- Sie sind bei SOGo 5 angemeldet
- Die Abwesenheitsnotiz muss von Ihrem Administrator aktiviert sein
  (`SOGoVacationEnabled = YES`)

## Schritt-für-Schritt-Anleitung

### Schritt 1: Abwesenheitseinstellungen öffnen

1. Klicken Sie auf das **Zahnradsymbol** ⚙ (Einstellungen) in der oberen Symbolleiste
2. Wählen Sie **Abwesenheitsnotiz** aus dem Einstellungsmenü

![Abwesenheitseinstellungen](./assets/01-vacation-settings.png)

### Schritt 2: Auto-Antwort aktivieren

Schalten Sie **Auto-Antwort aktivieren** auf **EIN**.

### Schritt 3: Zeitraum festlegen

| Feld: Description | Beschreibung | Beispiel |
|------|-------------|----------|
| **Startdatum** | Beginn Ihrer Abwesenheit | 2026-07-15 |
| **Enddatum** | Rückkehrdatum | 2026-07-28 |
| **Zeitzone** | Ihre lokale Zeitzone | Europe/Berlin |

Die Auto-Antwort wird am Startdatum um 00:00 Uhr aktiviert und
nach dem Enddatum um 23:59 Uhr deaktiviert.

:::tip
Legen Sie den Zeitraum so fest, dass er Reisetage einschließt — aktivieren Sie ihn
am Abend vor Ihrer Abreise und deaktivieren Sie ihn am Morgen nach Ihrer Rückkehr.
:::

### Schritt 4: Auto-Antwort-Nachricht verfassen

Verfassen Sie die Nachricht, die an Personen gesendet wird, die Ihnen eine E-Mail schreiben:

```
Betreff: Abwesenheit — Max Mustermann

Vielen Dank für Ihre Nachricht.

Ich bin vom 15. Juli bis 28. Juli 2026 außer Haus
und habe nur eingeschränkten E-Mail-Zugriff.

Bei dringenden Angelegenheiten wenden Sie sich bitte an
Erika Mustermann (erika.mustermann@firma.com).

Mit freundlichen Grüßen,
Max Mustermann
```

### Schritt 5: Antwortoptionen wählen

| Option: Description | Beschreibung |
|--------|-------------|
| **Antwort senden an** | Jeder, oder nur Personen in Ihren Kontakten/Ihrem Adressbuch |
| **Wiederholte Antworten** | Einmal pro Absender (Standard) oder jedes Mal, wenn sie schreiben |
| **Originalbetreff beibehalten** | `Re:` hinzufügen oder den ursprünglichen Betreff beibehalten |

**Empfohlen:** Einmal pro Absender senden, um Kollegen, die mehrfach
schreiben, nicht zu überfluten.

### Schritt 6: Speichern

Klicken Sie auf **Speichern** oder **Übernehmen**. Das Sieve-Skript wird auf dem
Mail-Server aktiviert.

## Kalender: Abwesenheit markieren

Während Sie die Abwesenheitsnotiz konfigurieren, blockieren Sie auch Ihren Kalender:

### Ein Abwesenheitsereignis erstellen

1. Öffnen Sie das Modul **Kalender**
2. Erstellen Sie ein neues Ereignis, das Ihren Abwesenheitszeitraum abdeckt
3. Stellen Sie es als **Ganztägiges** Ereignis ein
4. Fügen Sie "Abwesenheit" oder "Urlaub" als Titel hinzu
5. Markieren Sie es in den Sichtbarkeitseinstellungen als **Beschäftigt** oder **Abwesend**
6. Speichern

Dadurch wird der Zeitraum blockiert, sodass Kollegen bei der
Frei/Gebucht-Abfrage sehen, dass Sie nicht verfügbar sind.

## Einrichtung testen

### Test-E-Mail senden

1. Senden Sie eine E-Mail an Ihre SOGo 5-Adresse von einem anderen Konto aus
2. Sie sollten die Auto-Antwort innerhalb weniger Minuten erhalten
3. Die Auto-Antwort wird nur einmal pro Absender ausgelöst (gemäß konfigurierter Regel)

### Abwesenheitsstatus überprüfen

Öffnen Sie erneut **Einstellungen** → **Abwesenheitsnotiz**, um zu überprüfen:
- Der Schalter zeigt **EIN**
- Der Zeitraum ist korrekt
- Die Nachricht ist gespeichert

## Auto-Antwort deaktivieren

Wenn Sie zurück sind:

1. Gehen Sie zu **Einstellungen** → **Abwesenheitsnotiz**
2. Schalten Sie **Auto-Antwort aktivieren** auf **AUS**
3. Klicken Sie auf **Speichern**

Die Auto-Antwort wird sofort gestoppt. Löschen Sie optional das
Kalenderblock-Ereignis.

## Fehlerbehebung

### Auto-Antwort wird nicht gesendet

- Überprüfen Sie, ob die Abwesenheitsnotiz von Ihrem Administrator aktiviert wurde
- Vergewissern Sie sich, dass der Sieve-Server läuft (`SOGoSieveScriptsEnabled`)
- Die Auto-Antwort wird nur einmal pro Absender gesendet — testen Sie mit einer
  anderen E-Mail-Adresse
- Überprüfen Sie, ob der Zeitraum das aktuelle Datum einschließt

### "Sieve-Skript-Fehler" beim Speichern

- Der Sieve-Server ist möglicherweise nicht verfügbar
- Kontaktieren Sie Ihren Administrator, um den Sieve-Dienst zu überprüfen
- Vereinfachen Sie den Nachrichtentext (Sonderzeichen können Probleme verursachen)

## Fazit

Die Abwesenheits-Auto-Antwort stellt sicher, dass Personen über Ihre Abwesenheit
informiert sind. In Kombination mit einem Kalenderblock
können Kollegen Ihre Verfügbarkeit auf einen Blick erkennen.
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

