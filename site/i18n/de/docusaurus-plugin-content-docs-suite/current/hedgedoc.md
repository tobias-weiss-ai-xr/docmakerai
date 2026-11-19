---
title: "Notizen (HedgeDoc)"
sidebar_label: "Notizen (HedgeDoc)"
sidebar_position: 32
description: "Gemeinsame Markdown-Notizen — mehrere Personen, ein Dokument, in Echtzeit"
---

# Notizen (HedgeDoc)

[HedgeDoc](https://hedgedoc.openedusuite.org) ist der Dienst der
openEduSuite für gemeinsame Markdown-Notizen — mehrere Personen
schreiben gleichzeitig in einem Dokument, live. Öffnen Sie die
Portalkachel **HedgeDoc** und durchlaufen Sie die Suite-Anmeldung:
Die Startseite begrüßt Sie mit „Ideas grow better together".

![HedgeDoc-Startseite nach der Suite-Anmeldung](./assets/hedgedoc-work.png)

## Die Startseite

Die Navigationsleiste trägt drei Einträge — standardmäßig auf
Deutsch: **Einleitung**, **Verlauf** und **Anmelden**. Unter der
Überschrift liegen zwei Schaltflächen, **Anmelden** und
**Entdecke alle Funktionen**, und drei Karten nennen, was der
Editor kann:

- **Kollaboration in Echtzeit** — gemeinsames Schreiben live
- **Unterstützt Diagramme und MathJax** — Diagramme und Formeln
- **Unterstützt Präsentationsmodus** — eine Notiz als Folien

Jede Karte verlinkt in die eingebaute **Features**-Notiz, die den
Editor ausführlich beschreibt. Das Sprachmenü im Fußbereich
bietet rund 45 Sprachen, darunter Deutsch und Englisch; der Fuß
selbst nennt die Software — „Betrieben mit HedgeDoc" — mit den
Links **Versionen** (Release Notes) und **Quelltext** (Quellcode,
er zeigt auf HedgeDoc 1.10.4).

## Notizen lesen

- **Verlauf** öffnet das Panel **Lokaler Browserverlauf**: eine
  Tabelle mit den Spalten **Titel** und **Uhrzeit**, die die in
  diesem Browser geöffneten Notizen auflistet. Ein frischer
  Browser zeigt **Kein Verlauf**; **Vom Browser importieren**
  holt ältere Besuche aus der Chronik des Browsers.
- **Einleitung** verweist auf die Einleitungs-Notiz der Instanz.
  Sie ist für anonyme Besucher geschlossen — die Seite antwortet
  „You are not allowed to access this page. Maybe try logging
  in?"
- Notizen leben unter eigenen Adressen, und der Zugang unterscheidet
  sich je Notiz: Die **Features**-Notiz (über **Entdecke alle
  Funktionen** erreichbar) öffnet sich ohne Anmeldung und dient
  als eingebautes Handbuch, die Einleitungs-Notiz nicht.

## Anmeldung in HedgeDoc

Die Suite-Anmeldung öffnet die Tür zum Dienst, meldet Sie aber
nicht innerhalb von HedgeDoc an — die Navigation zeigt so lange
**Anmelden**, bis Sie einen Schritt mehr gehen:

1. Wählen Sie **Anmelden**. Es öffnet sich ein Dialog
   **Methode wählen**.
2. Entscheiden Sie sich für einen Weg: **Einloggen über
   Keycloak** oder **Einloggen über E-Mail**. Die Reiter
   **Anmelden** und **Registrieren** wechseln zwischen Anmeldung
   und Registrierung eines HedgeDoc-Kontos.

Stand November 2026 läuft die Keycloak-Option in einen Fehler:
Die Weiterleitung antwortet „Internal Server Error", und Sie
landen wieder auf der Startseite, weiterhin abgemeldet.
**Einloggen über E-Mail** fragt E-Mail-Adresse und Passwort ab;
der Reiter **Registrieren** enthält das Formular zum Anlegen
eines Kontos.

## In einer Notiz

Die Werkzeugleiste über einer Notiz bietet:

- **Neu** — eine neue Notiz beginnen
- **Veröffentlichen** — veröffentlichen. „If you want to share a
  read-only note, simply press the publish button and copy the
  URL", wie es die Features-Notiz ausdrückt
- **Menü** — ein Menü mit **Extra**, **Version** (die
  Überarbeitungen der Notiz), **Präsentationsmodus** (Folien
  anzeigen), **Importieren** (aus einem Gist oder der
  Zwischenablage) und **Download** (als Markdown, HTML oder
  reines HTML)

Ein Zähler zeigt, wie viele Personen gerade in der Notiz sind —
„1 ONLINE", wenn Sie allein sind —, und die Statuszeile nennt
das Alter der Notiz, etwa „ERSTELLT VOR EINEM TAG", neben
Markierungen wie **LOCKED**. Auf Desktop und Tablet bietet der
Editor drei Layouts — View (nur Ergebnis), Both (Editor und
Ergebnis nebeneinander) und Edit (nur Editor); auf dem Handy nur
View und Edit. Ein Nachtmodus dunkelt den Bildschirm ab.

Markdown ist das Format: Überschriften, Listen, Code — und mit
MathJax-Unterstützung sowie dem Präsentationsmodus auch Formeln
und Folien.

## HedgeDoc und seine Nachbarn

- [Grist](/suite/grist) — strukturierte Tabellen und Formulare
  statt freier Text.
- [XWiki](/suite/xwiki) — bleibendes Wissen statt lebender
  Dokumente.
- [Typst](/suite/typst) — Paper mit professionellem Satz.

## Barrierefreiheit

| Aktion | Taste |
|--------|-------|
| Durch Links und Menüs bewegen | `Tab` |
| Fokussiertem Link folgen | `Enter` |

- Die Startseite ist eine gewöhnliche Seite in Lesereihenfolge:
  Navigation, Überschrift, Schaltflächen, Karten, Fuß — `Tab`
  führt hindurch, `Enter` öffnet.
- `Strg+Pos1` bringt Sie zum Seitenanfang zurück.
