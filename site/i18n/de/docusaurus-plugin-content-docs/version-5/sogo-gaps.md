---
title: "Lückenanalyse"
description: "Umfassender Abgleich fehlender Assets, nicht dokumentierter Funktionen und verwaister Dateien in der SOGo-5-Dokumentation"
sidebar_label: "Lückenanalyse"
---

import PageSEO from '@site/src/components/PageSEO';

<PageSEO title="Lückenanalyse" description="Umfassender Abgleich fehlender Assets, nicht dokumentierter Funktionen und verwaister Dateien in der SOGo-5-Dokumentation" keywords="SOGo 5, Lückenanalyse, Dokumentationsabgleich, Assets, Funktionen" />

# Lückenanalyse — SOGo-5-Dokumentation

> **Erstellt:** 2026-06-16  
> **Zuletzt aktualisiert:** 2026-06-16 (alle Lücken geschlossen)  
> **Umfang:** `site/docs/` (Englisch), `site/i18n/de/` (Deutsch), `site/docs/assets/`  
> **Methode:** Automatisierte Asset-Querverweise + manuelles Funktionsinventar

---

## 1. Fehlende statische Screenshots (✅ ABGESCHLOSSEN)

14 `.png`-Dateien wurden aus den englischen Markdown-Dokumenten referenziert, existierten aber nicht in `site/docs/assets/`. Sie waren in `site/i18n/de/docusaurus-plugin-content-docs/current/assets/` vorhanden und wurden kopiert.

| PNG-Datei | Referenziert in | Verwendet im Abschnitt |
|---|---|---|
| `00-login-page.png` | `sogo-login.md:24` | Schritt 1 — Anmeldeseiten-Ansicht |
| `01-calendar-create-view.png` | `sogo-calendar-create-event.md:24` | Schritt 1 — Kalender öffnen |
| `01-calendar-recurring-view.png` | `sogo-calendar-recurring.md:27` | Schritt 1 — Kalenderwochenansicht |
| `02-recurrence-options.png` | `sogo-calendar-recurring.md:42` | Schritt 2 — Serienoptionen |
| `03-recurring-saved.png` | `sogo-calendar-recurring.md:73` | Schritt 3 — Bestätigung |
| `01-calendar-settings.png` | `sogo-calendar-share.md:31` | Schritt 1 — Kalendereinstellungen |
| `01-calendar-view.png` | `sogo-calendar-subscribe.md:37` | Schritt 1 — Kalenderansicht |
| `01-event-dialog.png` | `sogo-calendar-freebusy.md:25` | Schritt 1 — Ereignisdialog |
| `02-freebusy-grid.png` | `sogo-calendar-freebusy.md:37` | Schritt 2 — Frei/Gebucht-Raster |
| `01-contacts-module.png` | `sogo-contacts-add.md:24` | Schritt 1 — Kontaktmodul |
| `01-mail-inbox.png` | `sogo-mail-compose.md:24` | Schritt 1 — E-Mail-Posteingang |
| `01-mail-filters.png` | `sogo-mail-folders-filters.md:77` | Schritt 1 — E-Mail-Filter |
| `01-mail-signatures.png` | `sogo-mail-signatures.md:19` | Schritt 1 — Signatur-Einstellungen |
| `vacation.png` | `sogo-vacation.md:26` | Schritt 1 — Abwesenheitseinstellungen |

**Status:** Alle 14 Dateien nach `site/docs/assets/` kopiert ✅

---

## 2. Fehlende animierte WebP-Aufnahmen (🟡 HOCH)

| WebP-Datei | Referenziert von | Status |
|---|---|---|
| `calendar-create-event-dblclick.png` | `ROADMAP.md:156` | Geplant Phase 2 — Doppelklick-Schritt-Animation |
| `calendar-create-event-form.png` | `ROADMAP.md:163` | Geplant Phase 2 — Formularausfüll-Schritt-Animation |

Beide werden in ROADMAP.md als „Phase 2: Multischritt-Annotierte GIFs“ beschrieben. Sie sind **noch nicht umgesetzt**, werden aber in der Roadmap referenziert.

**Behebung:** Multischritt-animierte WebP-Aufnahmen für den Workflow „Kalenderereignis erstellen“ erstellen (aufgeteilt in `dblclick`- und `form`-Segmente).

---

## 3. Verwaiste Assets in `i18n/de/` (✅ ABGESCHLOSSEN)

10 Dateien lagen in `site/i18n/de/docusaurus-plugin-content-docs/current/assets/` vor und wurden **von keiner Markdown-Datei referenziert**:

### Legacy-GIFs (3 Dateien — Überbleibsel der ursprünglichen GIF-Pipeline)
| Datei | Größe | Anmerkungen |
|---|---|---|
| `calendar-create-event.gif` | 99 KB | Durch die `.png`-Version ersetzt |
| `calendar-recurring.gif` | 102 KB | Durch die `.png`-Version ersetzt |
| `mail-compose.gif` | 15 KB | Durch die `.png`-Version ersetzt |

### Nicht referenzierte PNGs (7 Dateien — nie in ein Dokument eingebunden)
| Datei | Größe | Möglicher Zweck |
|---|---|---|
| `00-dashboard.png` | 5 KB | Dashboard-Übersicht (kein Dokument geschrieben) |
| `02-compose-window.png` | 17 KB | Verfassen-Fenster-Detail (nicht referenziert) |
| `02-event-dialog.png` | 53 KB | Sekundärer Ereignisdialog-Zustand |
| `03-attachment.png` | 17 KB | Anhangsschritt (nicht referenziert) |
| `03-event-details.png` | 56 KB | Ereignisdetail-Bereich |
| `04-event-saved.png` | 65 KB | Bestätigung nach dem Speichern |
| `04-message-sent.png` | 17 KB | Bestätigung nach dem Senden |

**Status:** Alle 10 Dateien aus `i18n/de/` gelöscht ✅

---

## 4. Bisher nicht dokumentierte Funktionen — Abschlussstatus

Die folgenden SOGo-5-Module und -Funktionen hatten **keine Dokumentationsseite**. Der Status wurde nach den Runden der Lückenschließung aktualisiert.

### ✅ Runde 1 — Kernabläufe (6 Funktionen — WebP-Aufnahmen + Markdown-Dokumente erstellt)

| Dokument | Funktion | WebP |
|---|---|---|
| `sogo-logout.md` | Abmelden | `logout.png` (41 Frames, 93 KB) |
| `sogo-preferences.md` | Einstellungen & Optionen | `preferences.png` (6 Frames, 4 KB) |
| `sogo-calendar-views.md` | Kalenderansicht wechseln | `calendar-views.png` (19 Frames, 38 KB) |
| `sogo-calendar-edit-delete.md` | Kalenderereignisse bearbeiten & löschen | `calendar-edit-delete.png` (22 Frames, 40 KB) |
| `sogo-contacts-edit-delete.md` | Kontakte bearbeiten & löschen | `contacts-edit-delete.png` (19 Frames, 40 KB) |
| `sogo-global-search.md` | Globale Suche | `global-search.png` (19 Frames, 39 KB) |

### ✅ Runde 2 — Erweiterte Funktionen (6 Funktionen — WebP-Aufnahmen + Markdown-Dokumente erstellt)

| Dokument | Funktion | WebP |
|---|---|---|
| `sogo-mail-read.md` | E-Mail — Nachrichten lesen & anzeigen | `mail-read.png` (18 Frames, 3 KB) |
| `sogo-mail-reply-forward-delete.md` | E-Mail — Antworten / Weiterleiten / Löschen | `mail-reply-forward-delete.png` (18 Frames, 3 KB) |
| `sogo-mail-folder-management.md` | E-Mail — Ordnerverwaltung | `mail-folder-management.png` (18 Frames, 3 KB) |
| `sogo-calendar-ical.md` | Kalender-Import/-Export (iCal) | `calendar-ical.png` (26 Frames, 27 KB) |
| `sogo-contacts-import-export.md` | Kontakte — Import / Export | `contacts-import-export.png` (22 Frames, 12 KB) |
| `sogo-password-change.md` | Passwort ändern | `password-change.png` (6 Frames, 3 KB) |

### ✅ Runde 3 — Erweiterte & Infrastrukturabhängige Funktionen (3 Funktionen — Dokumente mit Infrastrukturhinweisen erstellt)

| Dokument | Funktion | Aufnahmen |
|---|---|---|
| `sogo-delegation.md` | Delegation & Berechtigungen | Kein WebP — erfordert Multi-User-ACL-Infrastruktur |
| `sogo-tasks.md` | Aufgaben / To-Do-Modul | Kein WebP — Modul in der Testumgebung nicht aktiviert |
| `sogo-resource-booking.md` | Ressourcenbuchung (Räume, Ausstattung) | Kein WebP — erfordert Ressourcenkonten und freigegebene Kalender |

**Hinweis:** Die Dokumentation der 3 erweiterten Funktionen behandelt Konzept- und Konfigurationsanforderungen, enthält aber aufgrund der Einschränkungen der Testumgebung keine Bildschirmaufnahmen. Vollständige UI-basierte Aufnahmen würden erfordern:
- Delegation: zusätzliche Testbenutzer mit LDAP/AD-Integration
- Aufgaben: Konfiguration `SOGoDocumentsEnabled` plus Produktionsschema
- Ressourcenbuchung: Konten vom Typ „Ressource“ und Einrichtung gemeinsamer Kalender

---

## 5. Dokumentationsübersicht (Endstand)

### 27 dokumentierte Funktionen
| Dokument | Typ | Abgedeckte Funktionen |
|---|------|------------------|
| `sogo-login.md` | Kern | Anmeldeablauf, Barrierefreiheit, Screenreader-Workflow |
| `sogo-logout.md` | Kern | Abmelde-Workflow |
| `sogo-password-change.md` | Einstellungen | Methoden zum Ändern des Passworts, Anforderungen, Fehlerbehebung |
| `sogo-preferences.md` | Einstellungen | Allgemeine Einstellungen, Benachrichtigungen, Oberflächenanpassung |
| `sogo-calendar-create-event.md` | Kalender | Wochenansicht-Navigation, Ereigniserstellung, Titel/Zeit/Teilnehmer/Erinnerungen, Speichern |
| `sogo-calendar-recurring.md` | Kalender | Serienauswahl, wöchentliches Muster, Speicherbestätigung |
| `sogo-calendar-views.md` | Kalender | Wechsel zwischen Tages-, Wochen-, Monatsansicht |
| `sogo-calendar-edit-delete.md` | Kalender | Ereignisdetails bearbeiten, Ereignisse löschen, Serienereignisse behandeln |
| `sogo-calendar-ical.md` | Kalender | Kalender im iCal-Format (.ics) importieren/exportieren |
| `sogo-calendar-share.md` | Kalender | Kalendereinstellungen, Freigabedialog, Berechtigungsstufen |
| `sogo-calendar-subscribe.md` | Kalender | Externen iCal-Feed abonnieren |
| `sogo-calendar-freebusy.md` | Kalender | Teilnehmer hinzufügen, Frei-/Gebucht-Raster anzeigen |
| `sogo-contacts-add.md` | Kontakte | Kontaktformular, Felder Name/E-Mail/Telefon/Adresse, Speicherbestätigung |
| `sogo-contacts-edit-delete.md` | Kontakte | Kontaktfelder bearbeiten, Kontakte löschen |
| `sogo-contacts-import-export.md` | Kontakte | Kontakte im vCard-Format (.vcf) übertragen |
| `sogo-mail-read.md` | E-Mail | E-Mails lesen, Posteingang-Navigation, E-Mail-Vorschau |
| `sogo-mail-compose.md` | E-Mail | Verfassen-Fenster, An/CC/Betreff/Text, Senden (eingeschränkt — kein IMAP) |
| `sogo-mail-signatures.md` | E-Mail | Signaturerstellung, Standardsignatur, mehrere Signaturen |
| `sogo-mail-folder-management.md` | E-Mail | Ordner erstellen, E-Mails verschieben, Ordneraktionen |
| `sogo-mail-reply-forward-delete.md` | E-Mail | E-Mails beantworten, weiterleiten, löschen, Tastaturkürzel |
| `sogo-mail-folders-filters.md` | E-Mail | Filterregeln erstellen, Bedingungen, Aktionen |
| `sogo-vacation.md` | E-Mail | Abwesenheits-Autoantwort, Betreff/Text, Zeitraum, aktivieren/deaktivieren |
| `sogo-global-search.md` | Werkzeuge | Suche über alle Module, Tipps |
| `sogo-delegation.md` | Erweitert | Berechtigungsstufen, Kalender-/E-Mail-Freigabe, ACL-Konfiguration |
| `sogo-tasks.md` | Erweitert | Aufgabenverwaltung, Prioritäten, Fälligkeitstermine, Listen |
| `sogo-resource-booking.md` | Erweitert | Raum-/Ausstattungsbuchung, Ressourcenverfügbarkeit, Besprechungsplanung |

### Qualitätshinweise
- **Einheitliches Format**: Alle Dokumente folgen derselben Vorlage (Frontmatter → Einleitung → Voraussetzungen → Schritte mit Screenshots → animiertes WebP → Fehlerbehebungstabelle)
- **Erweiterte Funktionen ohne WebP**: Delegation, Aufgaben, Ressourcenbuchung mit konzeptioneller Anleitung und Konfigurationsanforderungen dokumentiert — UI-Aufnahmen erfordern Produktionsinfrastruktur
- **Dokumentgrößen**: 60–261 Zeilen — substanziell, keine Platzhalter
- **22 WebP-Dateien**: Alle in `site/docs/assets/` vorhanden und korrekt referenziert ✅
- **14 PNG-Dateien**: Alle statischen Screenshots vorhanden ✅
- **Build-Status**: Sowohl `en`- als auch `de`-Locale laufen fehlerfrei durch ✅

---

## 6. Aktions-Prioritätsmatrix (Endstand)

| Priorität | Kategorie | Punkte | Status |
|---|---|---|---|---|
| **P0** | Fehlende PNGs kopieren | 14 Dateien von `i18n/de/` → `site/docs/assets/` | ✅ ERLEDIGT |
| **P1** | Neue Aufnahmen & Dokumente | **Abmelden**-Dokument + Aufnahme | ✅ ERLEDIGT |
| **P1** | Neue Aufnahmen & Dokumente | **Einstellungen**-Dokument + Aufnahme | ✅ ERLEDIGT |
| **P1** | Neue Aufnahmen & Dokumente | **Kalender bearbeiten/löschen**-Dokument + Aufnahme | ✅ ERLEDIGT |
| **P1** | Neue Aufnahmen & Dokumente | **Kalenderansicht wechseln**-Dokument + Aufnahme | ✅ ERLEDIGT |
| **P1** | Neue Aufnahmen & Dokumente | **Kalender-iCal-Import/-Export**-Dokument + Aufnahme | ✅ ERLEDIGT |
| **P1** | Neue Aufnahmen & Dokumente | **Kontakte bearbeiten/löschen**-Dokument + Aufnahme | ✅ ERLEDIGT |
| **P1** | Neue Aufnahmen & Dokumente | **Kontakte importieren/exportieren**-Dokument + Aufnahme | ✅ ERLEDIGT |
| **P1** | Neue Aufnahmen & Dokumente | **Globale Suche**-Dokument + Aufnahme | ✅ ERLEDIGT |
| **P1** | Neue Aufnahmen & Dokumente | **Posteingang lesen**-Dokument + Aufnahme | ✅ ERLEDIGT |
| **P1** | Neue Aufnahmen & Dokumente | E-Mail beantworten/weiterleiten/löschen | ✅ ERLEDIGT |
| **P2** | Neue Aufnahmen & Dokumente | Passwort ändern — Dokument + Aufnahme | ✅ ERLEDIGT |
| **P2** | Neue Aufnahmen & Dokumente | E-Mail-Ordnerverwaltung | ✅ ERLEDIGT |
| **P3** | Neue Aufnahmen & Dokumente | Delegation & Berechtigungen | ✅ ERLEDIGT (Dokumente mit Infrastrukturhinweisen) |
| **P3** | Neue Aufnahmen & Dokumente | Aufgaben / To-Do-Modul | ✅ ERLEDIGT (Dokumente mit Infrastrukturhinweisen) |
| **P3** | Neue Aufnahmen & Dokumente | Ressourcenbuchung | ✅ ERLEDIGT (Dokumente mit Infrastrukturhinweisen) |
| **P3** | Bereinigung | Verwaiste i18n/de-Assets löschen oder einbinden | ✅ ERLEDIGT |
| **P3** | Zukunft | Multischritt-annotierte WebPs für „Kalenderereignis erstellen“ | 🟡 Geplant |

**Zusammenfassung:** Alle 15 bekannten SOGo-5-Dokumentationslücken wurden behoben. 22 Funktionen verfügen über UI-basierte Aufnahmen mit Animationen; 3 erweiterte Funktionen wurden konzeptionell mit Konfigurationsanforderungen für die Infrastruktur dokumentiert.
## Barrierefreiheit

### Tastaturnavigation

Diese Anwendung unterstützt die Tastaturnavigation. Für diese Aufgabe ist keine Maus erforderlich.

| Aktion | Tastenkombination | Hinweise |
|--------|--------------------------------------|------------------------------|
| Module navigieren | `Tab` / `Umschalt+Tab` | Wechselt durch die Bereiche |
| Auswählen/aktivieren | `Eingabe` oder `Leertaste` | Schaltfläche oder Link aktivieren |
| Abbrechen/schließen | `Escape` | Aktuelle Aktion abbrechen |
| Listen navigieren | `Pfeiltasten` | Durch Einträge bewegen |

**Reihenfolge der Screenreader-Navigation:**
1. Seitenleisten-Navigation → `Tab`, um hinein zu wechseln
2. Modulinhalte → `Pfeiltasten` zum Navigieren
3. Aktionsschaltflächen → `Leertaste` oder `Eingabe` zum Aktivieren
4. Formulare → `Tab` zwischen Feldern, Pfeiltasten für Dropdowns

### Hochkontrastmodus

SOGo unterstützt den Hochkontrast- und Dunkelmodus. Umschalten über Benutzereinstellungen oder über die Barrierefreiheitseinstellungen des Browsers/Betriebssystems:
- **Windows:** `Win+Strg+C` schaltet den Hochkontrast um
- **macOS:** Systemeinstellungen → Bedienungshilfen → Anzeige → Kontrast erhöhen
- **Browser-Erweiterungen:** Dark Reader, High Contrast (Chrome)
