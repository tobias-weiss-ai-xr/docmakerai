---
title: "Kalenderereignis erstellen"
description: "Schritt-für-Schritt-Anleitung zum Erstellen von Ereignissen im SOGo 5-Kalender"
sidebar_label: "Kalenderereignis erstellen"
---

# Kalenderereignis erstellen

Dieses Tutorial führt Sie durch das Erstellen eines neuen Ereignisses im SOGo 5-Kalender,
einschließlich Datum und Uhrzeit, dem Hinzufügen von Teilnehmern und der Konfiguration von Erinnerungen.

## Voraussetzungen

- Ein SOGo 5-Konto mit gültigen Anmeldedaten
- Sie sind bei SOGo 5 angemeldet

## Schritt-für-Schritt-Anleitung

### Schritt 1: Kalendermodul öffnen

Klicken Sie oben in der Navigationsleiste auf **Kalender**,
um die Kalenderansicht zu öffnen.

![Kalendermodul in der Navigationsleiste](./assets/01-calendar-create-view.png)

Der Kalender öffnet standardmäßig in der **Wochenansicht**. Sie können zwischen
den Ansichten Tag, Woche, Monat und Jahr mit den Schaltflächen in der oberen Symbolleiste wechseln.

### Schritt 2: Neues Ereignis erstellen

Es gibt drei Möglichkeiten, ein Ereignis zu erstellen:

| Methode | Aktion |
|---------|--------|
| **Auf +-Schaltfläche klicken** | Klicken Sie auf die **+** (Plus)-Schaltfläche am unteren Rand der Kalenderansicht |
| **Doppelklicken** | Doppelklicken Sie auf einen beliebigen Zeitbereich im Kalendergitter |
| **Datumsauswahl verwenden** | Klicken Sie auf ein Datum im Minikalender links, dann auf **+** |

Wählen Sie die gewünschte Methode. Ein Dialog für ein neues Ereignis wird angezeigt.

### Schritt 3: Ereignisdetails eingeben

Füllen Sie die Ereignisdetails aus:

| Eingabefeld | Beschreibung | Beispiel |
|------|-------------|----------|
| **Titel** | Ein kurzer Name für Ihr Ereignis | "Team-Besprechung" |
| **Ort** | Wo das Ereignis stattfindet | "Konferenzraum B" |
| **Beginn** | Datum und Uhrzeit des Ereignisbeginns | Heute um 10:00 |
| **Ende** | Datum und Uhrzeit des Ereignisendes | Heute um 11:00 |
| **Kalender** | In welchem Kalender gespeichert werden soll — Auswahl aus Ihrer Kalenderliste | Ihr Account-Kürzel (vom Hochschulrechenzentrum vergeben) |
| **Kategorie** | Eine farbcodierte Kategorie | Besprechung (blau) |

:::tip
Für **Ganztägige Ereignisse** (z. B. Geburtstage, Feiertage) aktivieren Sie den
Schalter **Ganztägig**. Die Zeitfelder werden dann deaktiviert.
:::

### Schritt 4: Teilnehmer hinzufügen (Optional)

Wenn Sie andere Personen einladen möchten:

1. Klicken Sie auf den Bereich **Teilnehmer**, um ihn zu erweitern
2. Beginnen Sie mit der Eingabe des Namens oder der E-Mail-Adresse eines Kollegen
3. Wählen Sie die Person aus den automatischen Vervollständigungsvorschlägen aus
4. Wählen Sie deren **Teilnahmerolle**:
   - **Erforderlich** — Muss teilnehmen
   - **Optional** — Willkommen, aber nicht erforderlich
5. Wiederholen Sie dies für jeden weiteren Teilnehmer

SOGo 5 sendet jedem Teilnehmer eine E-Mail-Einladung, wenn Sie das Ereignis speichern.

### Schritt 5: Erinnerung festlegen (Optional)

Um eine Erinnerung vor dem Ereignis zu erhalten:

1. Klicken Sie auf den Bereich **Alarm**, um ihn zu erweitern
2. Wählen Sie, wann Sie erinnert werden möchten:
   - **15 Minuten vorher** (Standard)
   - **30 Minuten vorher**
   - **1 Stunde vorher**
   - **1 Tag vorher**
   - **Benutzerdefiniert** — eigene Zeit eingeben
3. Wählen Sie die Erinnerungsmethode:
   - **Anzeige** — Eine Popup-Benachrichtigung erscheint in Ihrem Browser, wenn die Erinnerung ausgelöst wird
   - **E-Mail** — Eine E-Mail an Ihre Adresse. **Hinweis:** E-Mail-Alarme erfordern den
     serverseitigen Dienst `sogo-ealarms-notify` — wenden Sie sich an Ihren Administrator,
     wenn E-Mail-Erinnerungen nicht ankommen
4. Sie können mehrere Alarme pro Ereignis kombinieren (z. B. **15 Minuten vorher** als
   Popup-Erinnerung plus **1 Tag vorher** als E-Mail): klicken Sie dazu auf **Alarm hinzufügen**

### Schritt 6: Beschreibung hinzufügen (Optional)

Nutzen Sie das Feld **Beschreibung**, um Notizen, eine Tagesordnung oder Vorbereitungshinweise
für das Ereignis hinzuzufügen. Dieses Feld unterstützt Klartext.

### Schritt 7: Wiederholung festlegen (Optional)

Für sich wiederholende Ereignisse klicken Sie auf den Bereich **Wiederholen** und wählen ein Muster:

| Zeitlicher Abstand | Beispiel |
|--------|----------|
| **Täglich** | Tägliches Standup-Meeting |
| **Wöchentlich** | Team-Meeting jeden Dienstag |
| **Alle zwei Wochen** | Sprint-Review alle zwei Wochen |
| **Monatlich** | Abteilungsmeeting am ersten Montag jedes Monats |
| **Jährlich** | Geburtstag oder Jahrestag |

Sie können auch ein **Enddatum** für die Wiederholung festlegen (z. B. Wiederholung bis
zum Semesterende).

### Schritt 8: Ereignis speichern

Klicken Sie auf **Speichern** oder **OK** (je nach Ihrer SOGo 5-Version), um das Ereignis zu erstellen.

Das Ereignis wird in Ihrem Kalender angezeigt. Wenn Sie Teilnehmer hinzugefügt haben, erhalten diese
eine E-Mail-Einladung, die sie annehmen oder ablehnen können.

## Fazit

Sie haben erfolgreich ein Kalenderereignis erstellt. Sie können nun:
- [Ihren Kalender mit anderen teilen](./sogo-calendar-share)
- Das Ereignis durch Klicken bearbeiten
- Es per Drag & Drop verschieben
- Die Dauer durch Ziehen an den Rändern ändern
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

### Screenreader-Workflow

Dieser Abschnitt beschreibt das Erstellen eines Kalenderereignisses mit Tastatur und Screenreader.

**Schritt 1: Kalendermodul öffnen**
1. `Tab` zur Modul-Navigation, Pfeiltasten zur Option **Kalender**, `Eingabetaste`
2. Sie hören: „Kalender, Wochenansicht“
3. Pfeiltasten zum gewünschten Tag

**Schritt 2: Ereignis erstellen (drei Möglichkeiten)**

**Möglichkeit 1: Plus-Schaltfläche**
- `Tab` zur Schaltfläche **+** (Ereignis erstellen)
- Sie hören: „Neues Ereignis, Schaltfläche“
- `Eingabetaste` – der Ereignisdialog öffnet sich

**Möglichkeit 2: Zeitfenster doppelklicken** *(nur mit Maus)*
- Suchen Sie das gewünschte Zeitfenster (z. B. Montag 10:00)
- Doppelklicken Sie darauf
- Tastaturnutzer: Verwenden Sie stattdessen die Plus-Schaltfläche (`Tab`, dann `Eingabetaste`)

**Möglichkeit 3: Datumsauswahl plus Schaltfläche**
- `Tab` zum Minikalender auf der linken Seite
- Pfeiltasten zum gewünschten Datum, `Eingabetaste` zur Auswahl
- `Tab` zur Plus-Schaltfläche, `Eingabetaste` zum Erstellen

**Schritt 3: Ereignisformular ausfüllen**

Die Formularfelder erscheinen in dieser Reihenfolge (Fokusfolge des Screenreaders):

1. **Titel** – erforderlich
   - Ereignisnamen eingeben, z. B. „Team-Besprechung“
   - `Tab` zum nächsten Feld
2. **Ort** – optional
   - Ort eingeben, z. B. „Konferenzraum B“
   - `Tab` zum nächsten Feld
3. **Startzeit** – Aufbau: Datumsauswahl → Uhrzeitauswahl
   - Pfeiltasten zur Auswahl des Datums
   - `Eingabetaste` bestätigen, dann die Uhrzeit wählen
   - `Tab` zum nächsten Feld
4. **Endzeit** – gleiches Format wie die Startzeit
5. **Kalender** – Auswahlliste; der Name Ihres Standardkalenders ist das Konto-Kürzel
6. **Kategorie** – Auswahlliste für die farbcodierte Kategorie
7. **Teilnehmer** – optional
   - Zum Hinzufügen von Personen: `Tab` zu **Teilnehmer**, `Eingabetaste` zum Erweitern
   - Erste Buchstaben des Namens eingeben, Pfeiltasten zur Auswahl
   - `Eingabetaste` zum Übernehmen
8. **Alarm/Erinnerung** – optional
   - `Tab` zu **Alarm**, `Eingabetaste` zum Erweitern
   - Vorlaufzeit mit Pfeiltasten wählen, `Eingabetaste` bestätigen

**Schritt 4: Ereignis speichern**
- `Tab` zur Schaltfläche **Speichern**
- Sie hören: „Speichern, Schaltfläche“
- `Eingabetaste` zum Aktivieren

**Schritt 5: Speichern überprüfen**
- Sie hören: „Ereignis gespeichert“
- Das Ereignis erscheint im Kalender zur gewählten Zeit
- Mit `Tab` springen Sie zum Ereignistitel und können die Details lesen

**Häufige Screenreader-Ansagen:**

| Ansage | Bedeutung | Aktion |
|--------|-----------|--------|
| „Ereignisdialog, Titelfeld“ | Dialog geöffnet, Fokus auf dem Titel | Ereignisdaten eingeben |
| „Titel ist ungültig“ | Titel leer oder zu kurz | Gültigen Titel eingeben |
| „Endzeit muss nach der Startzeit liegen“ | Zeitkonflikt | Endzeit anpassen |
| „Teilnehmer nicht gefunden“ | Ungültige E-Mail-Adresse eingegeben | Adresse korrigieren oder Kontakte durchsuchen |
| „Ereignis gespeichert“ | Erfolg | Ereignis wurde im Kalender erstellt |
| „Kalender aktualisiert“ | Bestehendes Ereignis geändert | Änderungen wurden gespeichert |

**Tastenkürzel im Ereignisdialog:**
- `Escape` → Abbrechen/verwerfen
- `Tab` → nächstes Feld
- `Umschalt+Tab` → vorheriges Feld

### Beschreibungen der visuellen Inhalte

**01-calendar-create-view.png:** Der statische Screenshot zeigt das Kalendermodul in der Navigationsleiste und die Kalenderansicht, in der Sie ein neues Ereignis erstellen.

**Screenreader-Alternative:** Wenn Sie dieses Bild nicht anzeigen können, verwenden Sie den Abschnitt **Screenreader-Workflow** weiter oben. Er bietet dieselben Informationen in Textform, die für Screenreader geeignet ist.

### Hochkontrastmodus

SOGo unterstützt den Hochkontrast- und Dunkelmodus. Aktivierung über Benutzereinstellungen oder systemweite Barrierefreiheitseinstellungen:
- **Windows:** `Win+Strg+C` schaltet den Hochkontrast um
- **macOS:** Systemeinstellungen → Bedienungshilfen → Anzeige → Kontrast erhöhen
- **Browser-Erweiterungen:** Dark Reader, High Contrast (Chrome)

- **Orientierung:** verlieren Sie Ihren Platz, drücken Sie `Strg+Pos1`, um zum
  Seitenanfang zurückzukehren und von dort weiterzunavigieren.
