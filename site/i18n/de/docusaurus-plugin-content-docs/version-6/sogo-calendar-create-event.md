---
title: "Kalenderereignis erstellen"
description: "Schritt-für-Schritt-Anleitung zum Erstellen von Ereignissen im SOGo 6-Kalender"
sidebar_label: "Kalenderereignis erstellen"
---

# Kalenderereignis erstellen

Dieses Tutorial führt Sie durch das Erstellen eines neuen Ereignisses im SOGo 6-Kalender,
einschließlich Datum und Uhrzeit, dem Hinzufügen von Teilnehmern und der Konfiguration von Erinnerungen.

## Voraussetzungen

- Ein SOGo 6-Konto mit gültigen Anmeldedaten
- Sie sind bei SOGo 6 angemeldet

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
| **Ereignistitel** | Ein kurzer Name für Ihr Ereignis | "Team-Besprechung" |
| **Kalender** | In welchem Kalender gespeichert werden soll — Auswahl aus Ihrer Kalenderliste | Ihr persönlicher Kalender |
| **Ganztägig** | Schalter für Ganztägiges Ereignis (z. B. Geburtstage, Feiertage); die Zeitfelder sind dann deaktiviert | — |
| **Startzeit / Endzeit** | Datum und Uhrzeit von Beginn und Ende | Heute, 10:00–11:00 |
| **Zeitzone (Ereignis)** | Zeitzone für Beginn und Ende — nützlich bei Ereignissen über Zeitzonen hinweg | GMT+01:00 Europe/Berlin |
| **Ort** | Wo das Ereignis stattfindet | "Konferenzraum B" |
| **Beschreibung** | Notizen, Tagesordnung oder Vorbereitungshinweise | — |
| **URL** | Optionaler Link (z. B. zum Besprechungsdokument) | — |

Der Dialog bietet darüber hinaus Felder, die beeinflussen, wie das
Ereignis für andere erscheint:

| Feld | Optionen | Wirkung |
|--------|---------|--------|
| **Visibility** | Public · Private · Confidential | Einstufung pro Ereignis — siehe [Frei/Gebucht: Was andere sehen](./sogo-calendar-freebusy#was-andere-sehen) |
| **Show as** | Busy · Free · Out of office · Tentative | Wie das Ereignis erscheint, wenn jemand Ihre Verfügbarkeit prüft |
| **Status** | Confirmed · Tentative · Cancelled | Der Status des Ereignisses selbst |
| **Labels** | — | Optionale Labels für das Ereignis |
| **Participants** | — | Eingeladene Personen — siehe nächster Schritt |

### Schritt 4: Teilnehmer hinzufügen (Optional)

Wenn Sie andere Personen einladen möchten:

1. Klicken Sie auf den Bereich **Teilnehmer**, um ihn zu erweitern
2. Beginnen Sie mit der Eingabe des Namens oder der E-Mail-Adresse eines Kollegen
3. Wählen Sie die Person aus den automatischen Vervollständigungsvorschlägen aus
4. Wählen Sie deren **Teilnahmerolle**:
   - **Erforderlich** — Muss teilnehmen
   - **Optional** — Willkommen, aber nicht erforderlich
5. Wiederholen Sie dies für jeden weiteren Teilnehmer

SOGo 6 sendet jedem Teilnehmer eine E-Mail-Einladung, wenn Sie das Ereignis speichern.

### Schritt 5: Erinnerung festlegen (Optional)

Um eine Erinnerung vor dem Ereignis zu erhalten:

1. Klicken Sie auf **Add reminder** (Erinnerung hinzufügen)
2. Legen Sie fest, wie weit im Voraus Sie erinnert werden möchten

Sie können mehrere Erinnerungen pro Ereignis hinzufügen.

### Schritt 6: Beschreibung hinzufügen (Optional)

Nutzen Sie das Feld **Beschreibung**, um Notizen, eine Tagesordnung oder Vorbereitungshinweise
für das Ereignis hinzuzufügen. Dieses Feld unterstützt Klartext.

### Schritt 7: Wiederholung festlegen (Optional)

Für sich wiederholende Ereignisse klicken Sie auf den Bereich **Wiederholen** und wählen ein Muster:

| Zeitlicher Abstand | Beispiel |
|--------|----------|
| **Day(s)** — täglich | Tägliches Standup-Meeting |
| **Week(s)** — wöchentlich | Team-Meeting jeden Dienstag |
| **Month(s)** — monatlich | Abteilungsmeeting am ersten Montag jedes Monats |
| **Year(s)** — jährlich | Geburtstag oder Jahrestag |

Sie können auch ein **Enddatum** für die Wiederholung festlegen (z. B. Wiederholung bis
zum Semesterende).

### Schritt 8: Ereignis speichern

Klicken Sie auf **Create Event** (Ereignis erstellen), um das Ereignis zu erstellen — oder auf **Cancel** (Abbrechen), um es zu verwerfen.

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
- `Tab` zur Schaltfläche **Create Event** (Ereignis erstellen)
- Sie hören: „Neues Ereignis, Schaltfläche“
- `Eingabetaste` – der Ereignisdialog öffnet sich

**Möglichkeit 2: Zeitfenster doppelklicken** *(nur mit Maus)*
- Suchen Sie das gewünschte Zeitfenster (z. B. Montag 10:00)
- Doppelklicken Sie darauf
- Tastaturnutzer: Verwenden Sie stattdessen die Schaltfläche **Create Event** (`Tab`, dann `Eingabetaste`)

**Möglichkeit 3: Datumsauswahl plus Schaltfläche**
- `Tab` zum Minikalender auf der linken Seite
- Pfeiltasten zum gewünschten Datum, `Eingabetaste` zur Auswahl
- `Tab` zur Plus-Schaltfläche, `Eingabetaste` zum Erstellen

**Schritt 3: Ereignisformular ausfüllen**

Die Formularfelder erscheinen in dieser Reihenfolge (Fokusreihenfolge des Screenreaders):

1. **Ereignistitel** – erforderlich
   - Ereignisnamen eingeben, z. B. „Team-Besprechung“
   - `Tab` zum nächsten Feld
2. **Ort** – optional
   - Ort eingeben, z. B. „Konferenzraum B“
   - `Tab` zum nächsten Feld
3. **Startzeit** – Aufbau: Datumsauswahl → Uhrzeitauswahl
   - Pfeiltasten zur Auswahl des Datums
   - `Eingabetaste` bestätigen, dann die Uhrzeit wählen
   - `Tab` zum nächsten Feld
4. **Endzeit** – gleiches Format wie Startzeit
5. **Kalender** – Auswahl des Kalenders (sein Name ist das Konto-Kürzel)
6. **Ganztägig** – Kontrollfeld für ganztägige Ereignisse
7. **Teilnehmer** – optional
   - Zum Hinzufügen von Personen: `Tab` zu **Teilnehmer**, `Eingabetaste` zum Erweitern
   - Erste Buchstaben des Namens eingeben, Pfeiltasten zur Auswahl
   - `Eingabetaste` zum Übernehmen
8. **Erinnerung** – optional
   - `Tab` zu **Add reminder** (Erinnerung hinzufügen), `Eingabetaste` zum Erweitern
   - Vorlaufzeit mit Pfeiltasten wählen, `Eingabetaste` bestätigen

**Schritt 4: Ereignis speichern**
- `Tab` zur Schaltfläche **Create Event** (Ereignis erstellen)
- Sie hören: „Create Event, Schaltfläche“
- `Eingabetaste` zum Speichern

**Schritt 5: Speichern überprüfen**
- Sie hören: „Ereignis gespeichert“
- Das Ereignis erscheint im Kalender zur gewählten Zeit
- Sie können mit `Tab` zum Ereignistitel springen und die Details lesen

**Häufige Screenreader-Ansagen:**

| Ansage | Bedeutung | Aktion |
|--------|-----------|--------|
| „Ereignisdialog, Titelfeld“ | Dialog geöffnet, Fokus auf dem Titel | Ereignisdaten eingeben |
| „Titel ist ungültig“ | Titel leer oder zu kurz | Gültigen Titel eingeben |
| „Endzeit muss nach der Startzeit liegen“ | Zeitkonflikt | Endzeit anpassen |
| „Teilnehmer nicht gefunden“ | Ungültige E-Mail-Adresse eingegeben | Adresse korrigieren oder Kontakte durchsuchen |
| „Ereignis gespeichert“ | Erfolg | Ereignis wurde im Kalender erstellt |

**Tastenkürzel im Ereignisdialog:**
- `Escape` → Abbrechen/verwerfen
- `Tab` → Nächstes Feld
- `Umschalt+Tab` → Vorheriges Feld

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
