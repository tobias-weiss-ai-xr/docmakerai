---
title: "Delegation & Berechtigungen"
description: "Wie Freigabe und Rechte in SOGo 6 funktionieren"
sidebar_label: "Delegation & Berechtigungen"
---

# Delegation & Berechtigungen

Delegieren Sie Zugriff auf Ihre Kalender, indem Sie anderen Benutzern Rechte daran einräumen.

## Voraussetzungen

- Ein SOGo 6-Konto mit gültigen Anmeldedaten
- Sie sind bei SOGo 6 angemeldet
- Mindestens zwei Benutzer mit SOGo-Konten (für die Delegation)

## Das Rechte-Modell

Wenn Sie einen Kalender freigeben, räumen Sie jeder Person eines dieser
Rechte ein:

| Recht | Was es erlaubt |
|:------|:---------------|
| Ereignisse ohne Details sehen | Nur belegte und freie Zeiten — keine Titel, keine Details |
| Ereignisse mit Details sehen | Titel, Zeiten und Beschreibungen |
| Antworten | Auf Einladungen reagieren |
| Bearbeiten | Ereignisse anlegen, ändern und löschen |

Wie ein bestimmtes Ereignis der Person erscheint, hängt von ihrem Recht
und der Einstufung des Ereignisses ab — siehe
[Frei/Gebucht: Was andere sehen](./sogo-calendar-freebusy#was-andere-sehen).

Dasselbe Zwei-Achsen-Modell gilt für Adressbücher und E-Mail-Ordner,
sofern Ihre Installation deren Freigabe ermöglicht.

## Freigabe in der Praxis

Wo sich die Freigabe-Steuerungen befinden, hängt von Ihrer Installation
ab: Sie erscheinen bei den Menüs einzelner Elemente oder Sammlungen
eines Moduls.

:::info
Die Demo-Umgebung unter demov6.sogo.nu blendet die Freigabe-Steuerungen
nicht ein — deshalb zeigt diese Anleitung bewusst keine Schritt-für-
Schritt-Beschreibung davon.
:::

## Verwandte Einstellungen

Kalenderverhalten, das Sie selbst einstellen können (Avatar-Menü →
**Calendar**):

- Standardkalender und Standard-Einstufung (z. B. *Confidential*)
- Ob Zeiten außerhalb der Arbeitszeit als belegt angezeigt werden —
  siehe [Frei/Gebucht](./sogo-calendar-freebusy)
- Erster Tag der Woche

## Siehe auch

- [Frei/Gebucht](./sogo-calendar-freebusy) — wie geteilte Verfügbarkeit aussieht
- [Kalenderfreigabe](./sogo-calendar-share) — Anleitung zur gegenseitigen Freigabe

## Barrierefreiheit

### Tastaturnavigation

Die Freigabe-Steuerungen — sofern Ihre Installation sie zeigt — sind
gewöhnliche Schaltflächen und Dropdowns: erreichen Sie sie mit
`Tab` / `Shift+Tab`, aktivieren Sie sie mit `Enter`.

### Screenreader

- `Strg+Pos1` bringt Sie an den Seitenanfang — ein verlässlicher
  Ausgangspunkt, um die Seite mit `h` (Überschriften) zu erschließen.
- Die Rechtetabellen oben verwenden echtes Tabellen-Markup — Screenreader
  können sie Zeile für Zeile lesen.

- **Hochkontrast und Dunkelmodus:** Kontrast und dunkle Themes kommen vom
  Betriebssystem oder Browser — Windows `Win+Strg+C`, macOS „Kontrast erhöhen“
  oder eine Browser-Erweiterung wie Dark Reader. Bietet die App ein eigenes
  dunkles Theme, schalten Sie es in den Einstellungen; die oben beschriebene
  Bedienung gilt weiterhin.
