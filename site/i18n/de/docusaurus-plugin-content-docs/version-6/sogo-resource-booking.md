---
title: "Ressourcenbuchung (Räume, Ausrüstung)"
description: "Gemeinsam genutzte Ressourcen wie Besprechungsräume und Ausrüstung buchen"
sidebar_label: "Ressourcenbuchung"
---

# Ressourcenbuchung

Reservieren Sie gemeinsam genutzte Ressourcen — Besprechungsräume, Projektoren, Ausrüstung — über den Kalender.

:::info
Eine Ressource ist üblicherweise ein besonderes Kalenderkonto, das Ihr
Administrator bereitstellt. Die Demo-Umgebung unter demov6.sogo.nu hat
keine Ressourcenkonten — deshalb beschreibt diese Anleitung den Weg der
Buchung ohne Screenshots einer Ressourcen-Auswahl.
:::

## Voraussetzungen

- Ein SOGo 6-Konto mit gültigen Anmeldedaten
- Sie sind bei SOGo 6 angemeldet
- Ressourcenkonten von Ihrem Administrator konfiguriert

## Der Weg der Buchung

Eine Ressource buchen heißt: ein Ereignis anlegen und die Ressource als
Teilnehmer hinzufügen:

1. Öffnen Sie das **Kalender**-Modul
2. Legen Sie ein Ereignis an — klicken Sie auf die **+**-Schaltfläche in
   der Symbolleiste oder doppelklicken Sie auf ein Zeitfeld im Kalender
   (siehe [Ereignis erstellen](./sogo-calendar-create-event))
3. Klappen Sie im Ereignisdialog **Participants** (Teilnehmer) aus
4. Tippen Sie den Namen der Ressource ein — Räume und Ausrüstung
   erscheinen in derselben automatischen Vervollständigung wie Personen
5. Fügen Sie die teilnehmenden Personen hinzu
6. Klicken Sie auf **Create Event** (Ereignis erstellen)

## Verfügbarkeit der Ressource prüfen

Prüfen Sie vor der Buchung, wann die Ressource frei ist:

- Fügen Sie sie zum Ereignis hinzu und nutzen Sie die Verfügbarkeitsansicht —
  siehe [Frei/Gebucht](./sogo-calendar-freebusy)
- Die belegten Zeiten der Ressource erscheinen wie die jedes Teilnehmers

Wird eine Buchung abgelehnt, wählen Sie einen anderen Zeitpunkt — die
Ressource ist dann bereits reserviert.

## Barrierefreiheit

### Tastaturnavigation

| Aktion | Wie | Hinweis |
|--------|-----|---------|
| Buchungsereignis anlegen | `Tab` zu **Create Event**, dann `Enter` | Siehe Ereignis erstellen |
| Participants öffnen | `Tab` zum Feld Participants | Bereich im Ereignisdialog |
| Buchung speichern | `Tab` zu **Create Event**, dann `Enter` | Bestätigen-Schaltfläche des Dialogs |

### Screenreader

- `Strg+Pos1` bringt Sie an den Seitenanfang — ein verlässlicher
  Ausgangspunkt, um die Seite mit `h` (Überschriften) zu erschließen.
- In der Verfügbarkeitsansicht sind belegte Blöcke rein visuell — die
  Frei/Gebucht-Daten dahinter liest der Screenreader als Text vor.

- **Hochkontrast und Dunkelmodus:** Kontrast und dunkle Themes kommen vom
  Betriebssystem oder Browser — Windows `Win+Strg+C`, macOS „Kontrast erhöhen“
  oder eine Browser-Erweiterung wie Dark Reader. Bietet die App ein eigenes
  dunkles Theme, schalten Sie es in den Einstellungen; die oben beschriebene
  Bedienung gilt weiterhin.
