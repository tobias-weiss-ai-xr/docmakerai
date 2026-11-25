---
title: "Files (Nextcloud)"
sidebar_label: "Files (Nextcloud)"
sidebar_position: 30
description: "The classic cloud: files, sharing, and apps"
---

# Files (Nextcloud)

[Nextcloud](https://nextcloud.openedusuite.org) is the classic cloud in the
openEduSuite: open the **Nextcloud** tile in the [portal](/suite/portal) and
single sign-on takes you straight in — there is no second login. This
instance speaks German; the labels below are the ones you actually see,
with a short English gloss.

![Nextcloud dashboard after SSO login](./assets/nextcloud.png)

## The Dashboard

After signing in you land on the **Dashboard**. It greets you by name and
shows widgets — **Empfohlene Dateien** (recommended files) lists recent
files with their path and when they last changed. **Anpassen** (Customize)
opens **Widgets bearbeiten**: switch **Status**, **Wetter** (weather),
**Empfohlene Dateien**, **Neueste Aktivitäten** (recent activity),
**Teams**, **Favorisierte Dateien** (favorite files), **An diesem Tag**
(on this day) and **Letzter Status** (last status) on or off as they serve
you.

An intro dialog can lie over the page ("Eine Kollaborationsplattform, mit
der Sie die Kontrolle haben"). **Vorherige**, **Weiter** and
**Überspringen** page through it.

## Apps Inside This Nextcloud

The app menu at the top left (**Apps-Menü öffnen**) holds:

- **Dashboard** — the start page above
- **Dateien** (Files) — your files and folders
- **Office** — text documents, with templates such as Leer (blank), Readme,
  Meeting notes and Product plan
- **Fotos** (Photos) — your pictures and videos: **Alle Medien**, **Alben**,
  **Favoriten**, **An diesem Tag**, **Orte** and more
- **Teams** — groups you share with; **Neues Team** starts one
- **Aktivität** (Activity) — what happened to your files
- **App Store** — the public Nextcloud app catalogue

Chat and calendar are not part of this Nextcloud. The suite runs its own
services for those: [Element Chat](/suite/chat) for messaging and
[SOGo](/suite/sogo-classic) for mail and calendars.

## Working With Files

**Dateien** opens with **Alle Dateien** (All files). The left navigation
offers:

- **Persönliche Dateien** (Personal files), **Neueste** (Recent),
  **Favoriten** (Favorites), **Schlagworte** (Tags), **Ordnerbaum** (Folder
  tree), **Gelöschte Dateien** (Deleted files)
- **Freigaben** (Shares) with **Mit Ihnen geteilt** (shared with you),
  **Von Ihnen geteilt** (shared by you) and **Über einen Link geteilt**
  (shared via link), plus **Ausstehende Freigaben** (pending shares),
  **Dateianfragen** (file requests) and **Gelöschte Freigaben** (deleted
  shares)
- below that, how much storage you use (for example "62,6 MB verwendet")
  and **Dateien-Einstellungen** (Files settings)

The list sorts by **Name**, **Aktionen** (actions), **Größe** (size) or
**Geändert** (modified); a summary line at the end counts what is in view
("6 Dateien · 3 Ordner" — 6 files · 3 folders). The button
**Zur Kachelansicht wechseln** switches to tiles.

**Neu** (New) creates and uploads: **Dateien hochladen** (upload files),
**Ordner hochladen** (upload folder), **Neuer Ordner** (new folder),
**Dateianfrage erstellen** (create a file request) and **Textdokument**
(text document).

Every row ends with two buttons: **Freigabeoptionen** (sharing options)
and **Aktionen** (actions). The **Aktionen** menu offers favorites
(**Zu den Favoriten hinzufügen**), **Details**, **Schlagworte verwalten**
(manage tags), **Umbenennen** (rename), **Verschieben oder kopieren** (move
or copy), **Erinnerung erstellen** (create reminder), **Lokal öffnen**
(open locally), **Herunterladen** (download) and **Datei löschen** (delete
file — **Ordner löschen** for folders). Files add **Ansicht** (view) and
**Datei sperren** (lock file).

## Sharing

**Freigabeoptionen** opens the panel with the tabs **Teilen** (Share),
**Aktivität** (Activity) and **Versionen** (Versions). Under **Teilen**:

- **Interne Freigaben** (internal shares) — search internal recipients
  ("Nach internen Empfängern suchen")
- **Andere mit Zugriff** (others with access) — who can already open the
  item
- **Interner Link** (internal link) — "Für Personen, die bereits Zugriff
  haben" (for people who already have access)
- **Externe Freigaben** (external shares) — enter external recipients
- **Öffentlichen Link erstellen** (create a public link) — a link anyone
  with it can use

## Activity

The **Aktivität** app lists what happened — for example "Sie haben …
erstellt" (you created …) with date and time. **Alle Aktivitäten** (all
activities), **Von Ihnen** (by you), **Von anderen** (by others) and
topics such as **Dateiänderungen** (file changes) or **Dateifreigaben**
(file shares) filter the list; **Jederzeit** (any time) and **Heute**
(today) narrow the time range.

## Nextcloud or OpenCloud

The suite runs two clouds, on purpose:

- **[OpenCloud](/suite/files)** — the suite's native file service;
  tightly integrated with the other tiles. First choice for everyday
  files.
- **Nextcloud** — the mature all-rounder with its own app ecosystem.
  First choice when you need a Nextcloud-specific app or are used to its
  workflows.

Both use the same SSO account; files live separately in each.

If the service stays closed to you, the
[helpdesk](/suite/helpdesk-create-ticket) reaches its operators.

## Accessibility

| Action | Key |
|--------|-----|
| Move through the file list and toolbar | `Tab` |
| Open the focused file or folder | `Enter` |
| Open the header search | `Strg K` |
| Back to the top of the page | `Ctrl+Home` (German keyboards: `Strg+Pos1`) |

- Keyboard users reach skip links first: "Zur App-Navigation springen"
  (skip to app navigation) and "Zum Hauptinhalt springen" (skip to main
  content), plus a "Tastatur-Navigationshilfe" (keyboard navigation help).
- The file area is a standard list with a toolbar — `Tab` walks it,
  `Enter` opens. The header search, "Apps, Dateien, Nachrichten und mehr",
  shows its shortcut right beside it.

- **High contrast and dark mode:** contrast and dark themes come from the
  operating system or browser — Windows `Win+Ctrl+C`, macOS *Increase contrast*,
  or a browser extension such as Dark Reader. If the app offers its own dark
  theme, switch it in its settings; the navigation described above still applies.
