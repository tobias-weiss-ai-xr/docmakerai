---
title: "Frei/Gebucht-Abfrage"
description: "Verfügbarkeit von Kollegen vor der Terminplanung prüfen"
sidebar_label: "Frei/Gebucht-Abfrage"
---

# Frei/Gebucht-Abfrage

Prüfen Sie die Verfügbarkeit Ihrer Kollegen, bevor Sie eine Besprechung
planen — direkt aus dem Dialog zur Ereigniserstellung.

## Warum die Kalenderfreigabe gegenseitig sein muss

Frei/Gebucht-Daten sind nicht öffentlich. Verfügbarkeiten werden nur für
Kalender angezeigt, deren Besitzer sie aktiv freigegeben hat — deshalb muss
die Freigabe in beide Richtungen laufen:

- **Sie sehen Kollegen nur, wenn diese für Sie freigegeben haben.** Ohne
  erteilte Freigabe bleibt die Zeile auf „Keine Daten“ — die Verfügbarkeit
  bleibt unsichtbar.
- **Kollegen sehen Sie nur, wenn Sie freigegeben haben.** Dieselbe Prüfung
  läuft umgekehrt ab, wenn jemand anderes die Besprechung plant.
- **Einseitige Freigabe bricht den Workflow.** Gibt nur eine Seite frei,
  schlägt jede Abfrage in der anderen Richtung fehl — und die E-Mail-Frage
  „Sind Sie um … frei?“ ist genau da wieder da, wo die Frei/Gebucht-Abfrage
  sie eigentlich überflüssig machen sollte.

Bevor Sie sich auf die Verfügbarkeitsanzeige verlassen, stellen Sie die
Freigabe einmalig gegenseitig sicher:

1. [Geben Sie Ihren eigenen Kalender frei](./sogo-calendar-share.md) —
   mindestens die Frei/Gebucht-Berechtigung für Ihr Team
2. Bitten Sie die Teilnehmer, es Ihnen gleichzutun — oder lassen Sie Ihre
   Verwaltung einen organisationsweiten Standard setzen
   (`SOGoCalendarDefaultRoles`)

„Keine Daten“ ist daher kein Fehler: Das Berechtigungssystem funktioniert
genau wie vorgesehen.

## Voraussetzungen

- Ein SOGo 6-Konto mit gültigen Anmeldedaten
- Sie sind bei SOGo 6 angemeldet
- Gegenseitige Kalenderfreigabe: Der Kollege hat seine Frei/Gebucht-
  Informationen für Sie freigegeben, und Sie Ihre für ihn (siehe
  [Warum die Kalenderfreigabe gegenseitig sein muss](#warum-die-kalenderfreigabe-gegenseitig-sein-muss))

## Schritt-für-Schritt-Anleitung

### Schritt 1: Mit der Erstellung eines Ereignisses beginnen

1. Öffnen Sie das Modul **Kalender**
2. Klicken Sie auf **+**, um ein neues Ereignis zu erstellen, oder klicken Sie auf ein vorhandenes Ereignis, um es zu bearbeiten

![Ereignisdialog mit Teilnehmeroptionen](./assets/01-event-dialog.png)

### Schritt 2: Teilnehmer hinzufügen

1. Klicken Sie im Ereignisdialog auf den Bereich **Teilnehmer**
2. Beginnen Sie mit der Eingabe des Namens oder der E-Mail-Adresse eines Kollegen
3. Wählen Sie die Person aus der automatischen Vervollständigungsliste aus
4. Wiederholen Sie den Vorgang für jede Person, die Sie prüfen möchten

Sobald Personen eingetragen sind, öffnet sich das Frei/Gebucht-Raster automatisch —
es gibt keine separate Frei/Gebucht-Schaltfläche.

![Frei/Gebucht-Verfügbarkeitsraster](./assets/02-freebusy-grid.png)

### Schritt 3: Das Raster lesen

Das Raster zeigt Zeitbereiche für jede Person:

| Farbe | Bedeutung |
|-------|----------|
| ✅ **Grün** | Verfügbar |
| ❌ **Rot** | Beschäftigt (hat ein Ereignis) |
| 🟡 **Gelb** | Vorläufig / vielleicht teilnehmend |
| ⬜ **Weiß** | Keine Daten (nicht freigegeben oder außerhalb der Arbeitszeit) |

### Schritt 4: Einen gemeinsamen Zeitraum finden

Suchen Sie nach einem Zeitraum, in dem alle Teilnehmer grün sind.
SOGo 6 schlägt möglicherweise automatisch den nächsten verfügbaren Termin vor.

### Schritt 5: Zeit bestätigen

Klicken Sie auf den gewünschten Zeitbereich im Raster.
Die Start-/Endzeit des Ereignisses wird entsprechend aktualisiert.

## Was andere sehen

Dies ist die Berechtigung, die die gegenseitige Freigabe erteilt — siehe
[Warum die Kalenderfreigabe gegenseitig sein muss](#warum-die-kalenderfreigabe-gegenseitig-sein-muss).

Standardmäßig ist SOGo 6 so konfiguriert, dass andere Benutzer Folgendes sehen können:

| Berechtigung | Was sichtbar ist |
|-------------|-----------------|
| **Frei/Gebucht** | Nur ob Sie verfügbar oder beschäftigt sind (keine Details) |
| **Anzeigen (schreibgeschützt)** | Ereignistitel und -zeiten |
| **Vertrauliche Ereignisse** | Nur als "Beschäftigt" markiert, auch für Betrachter |

Wer nur die Frei/Gebucht-Berechtigung hat, sieht lediglich belegte und freie Zeiten — ohne Titel oder Details. Ereignisse, die Sie als vertraulich markieren, erscheinen für andere ohnehin nur als „beschäftigt".

Ihr Administrator kann die standardmäßigen Berechtigungsstufen über die
Einstellung `SOGoCalendarDefaultRoles` ändern.

## Fehlerbehebung

### Kollege wird nicht angezeigt

- Überprüfen Sie, ob der Kollege ein SOGo 6-Konto hat
- Möglicherweise hat er die Frei/Gebucht-Freigabe nicht aktiviert
- Er befindet sich möglicherweise in einem anderen Adressbuch — versuchen Sie, die vollständige E-Mail-Adresse einzugeben

### Alle Zeiten zeigen "Keine Daten"

- Es fehlt eine Freigabe, keine Störung — siehe
  [Warum die Kalenderfreigabe gegenseitig sein muss](#warum-die-kalenderfreigabe-gegenseitig-sein-muss)
- Der Kollege hat seinen Kalender nicht für Sie freigegeben
- Bitten Sie die Person oder Ihren Administrator, Ihnen den Frei/Gebucht-Zugriff zu gewähren
- Standardrollen können eingeschränkt sein (`PublicDAndTViewer` muss gesetzt sein)

## Fazit

Die Frei/Gebucht-Abfrage hilft Ihnen, Besprechungstermine zu finden, ohne die
lästige E-Mail-Frage "Sind Sie um ... frei?". Sie funktioniert für
alle in Ihrer Organisation, die ihre Kalenderverfügbarkeit freigeben.
Die einmalige Voraussetzung ist die gegenseitige Freigabe: Verfügbarkeiten
werden nur für Kalender angezeigt, deren Besitzer Zugriff gewährt haben —
in beide Richtungen.
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
