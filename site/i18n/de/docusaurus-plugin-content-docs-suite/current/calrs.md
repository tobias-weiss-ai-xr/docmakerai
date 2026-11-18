---
title: "Kalender-Dienst (calrs)"
sidebar_label: "Kalender (calrs)"
sidebar_position: 27
description: "Ein eigener Kalender-Dienst — derzeit nur per Link erreichbar, Zugang über die Verwaltung"
---

# Kalender-Dienst (calrs)

Auf
[calendar.openedusuite.org](https://calendar.openedusuite.org) läuft
**calrs** — „Powered by calrs 🦀", wie der Seitenfuß sagt — der
Open-Source-Buchungsdienst von [cal.rs](https://cal.rs):
Terminbuchung nach Cal.com-Art, die gebuchten Slots verwaltet ein
Kalender-Backend. Er ist von den
[SOGo-Kalendern](/sogo6/sogo-calendar-views) getrennt, ließe sich
aber mit ihnen verbinden: Buchungen erscheinen in SOGo als
abonnierter Kalender. Beachten Sie: Er hat derzeit keine Kachel im
**Portal** — Sie erreichen ihn nur über einen Link, und der Zugang
wird von der Verwaltung gepflegt.

![calrs-Anmeldung: SSO oder E-Mail](./assets/calrs-login.png)

## Anmelden

Die Anmeldeseite bietet zwei Wege:

- **Sign in with SSO** — über das openEduSuite-Konto
- **Sign in with email** — mit einem calrs-eigenen Konto

### Die aktuelle SSO-Hürde

Die Anmeldung über SSO kann in einem Konto-Fehler enden:

> Account error: An account with this email already exists. The
> identity provider has not verified that you own this address, so
> we cannot link them automatically. Contact an administrator.

Sehen Sie diese Meldung, ist auf Ihrer Seite nichts schiefgelaufen
— der Dienst kennt Ihre E-Mail-Adresse bereits, kann sie aber noch
nicht von selbst mit Ihrem openEduSuite-Konto verbinden. Wenden Sie
sich **an die Verwaltung** (siehe
[Helpdesk](/suite/helpdesk-create-ticket)), um beide zu verknüpfen
oder E-Mail-Zugangsdaten zu erhalten.

Die Selbstregistrierung ist deaktiviert („Registration is
disabled") — auch neue Konten legt die Verwaltung an. Die
öffentlichen Buchungsseiten (`/booking`) existieren zwar, antworten
jedoch so lange „Event type not found", bis ein Buchungstyp
veröffentlicht ist.

## Bis der Zugang eingerichtet ist

Ihr Arbeitskalender bleibt [SOGo](/sogo6/sogo-calendar-views): Post,
Kalender und Aufgaben an einem Ort, mit
[Einladungen](/sogo6/sogo-calendar-create-event) und
[Delegation](/sogo6/sogo-delegation).

## Barrierefreiheit

| Aktion | Taste |
|--------|-------|
| Durch Formularfelder und Schaltflächen bewegen | `Tab` |
| Fokussiertes Feld bestätigen | `Enter` |

- Die Anmeldeseite ist ein kleines, gewöhnliches Formular: `Tab`
  bewegt Sie zwischen SSO-Schaltfläche, E-Mail, Passwort und
  Anmeldung; `Enter` bestätigt.
- Verlieren Sie die Orientierung, bringt Sie `Strg+Pos1` zum
  Seitenanfang zurück.
