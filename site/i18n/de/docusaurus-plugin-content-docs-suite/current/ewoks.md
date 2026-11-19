---
title: "Workflows (EWOKS)"
sidebar_label: "Workflows (EWOKS)"
sidebar_position: 28
description: "Wissenschaftliche Workflows im Browser bauen und ihre Ausführung verfolgen"
---

# Workflows (EWOKS)

[EWOKS](https://ewoks.openedusuite.org) ist der Workflow-Editor der
openEduSuite, aufbauend auf dem Workflow-System
[ewoks](https://ewoks.readthedocs.io) des ESRF. Öffnen Sie die
Portalkachel **Scientific Workflows (EWOKS)** und melden Sie sich per
SSO an — der Editor startet in der Ansicht **Edit**. Die Kopfzeile
nennt die Anwendung **EwoksWeb** und bietet zwei Reiter:

- **Edit** — einen Workflow als Graphen zusammenbauen: Aufgaben
  (Tasks) sind Knoten, Verbindungen tragen die Daten von einer Aufgabe
  zur nächsten.
- **Monitor** — die Ausführungsansicht: sie liest die
  Ausführungsereignisse, die der Server protokolliert. Dazu muss
  dieses Ereignis-Backend laufen; ist es nicht erreichbar, meldet die
  Ansicht eine fehlgeschlagene Anfrage, statt Ausführungen
  aufzulisten.

![Der Workflow-Editor von EWOKS](./assets/ewoks.png)

## Einen Workflow in Edit bauen

Die Überschrift über der Fläche nennt den Workflow — ein neuer beginnt
als **Untitled workflow (unsaved)**. Die Werkzeugleiste daneben
enthält:

- **Quick Open** — ein Suchfeld, das die auf dem Server gespeicherten
  Workflows nach Kategorie gruppiert auflistet; das Symbol **Open** in
  der Werkzeugleiste führt dasselbe Feld herbei. Diese Instanz bietet
  den Workflow **demo** unter **No category**: wer ihn auswählt, lädt
  ihn in den Editor, und die Überschrift zeigt dann seinen Namen.
- die Schaltfläche zum Speichern — ein Symbol, das seinen Zustand im
  zugänglichen Namen trägt: **no changes**, oder **changes pending**,
  sobald Sie etwas geändert haben.
- ein Menü mit weiteren Aktionen: **New workflow**
  (`Strg+Umschalt+N`), **Open from disk**, **Download**,
  **Execute workflow** (`Strg+Umschalt+X`), **Save as...**,
  **Delete workflow**, **Manage icons** und **Create new task**.

**DISCOVER TASKS** listet links die Task-Pakete, zum Aufklappen.
**ewokscore** hält Rechenaufgaben (etwa `add`, `append` oder
`SumTask`); **General** hält die Bausteine `graphInput`,
`graphOutput`, `taskSkeleton`, `note` und `subworkflow`. Die
Schaltfläche **DISCOVER TASKS** öffnet einen gleichnamigen Dialog:
Geben Sie einen **Module name** ein — oder kreuzen Sie
**Discover from all modules in the current Python environment** an —
und drücken Sie **Discover**, um weitere Pakete in die Liste zu holen.

Ziehen Sie eine Aufgabe aus der Liste auf die Fläche; der Knoten
erscheint mit einer erzeugten Bezeichnung wie `SumTask0`, und die
leere Fläche sagt es selbst: „Drag and drop tasks here to start
building your workflow". Verbinden Sie die Knoten, damit die Daten
einen Weg haben. Symbol-Schaltflächen am Rand der Fläche bieten
**Zoom In**, **Zoom Out**, **Fit View** und **Toggle Interactivity**.

Das Panel rechts bearbeitet, was gerade ausgewählt ist:

- Nichts ausgewählt — Eigenschaften des **Workflow**: Label, Comment,
  Category und Canvas Background Color.
- Knoten ausgewählt — Eigenschaften des **Node**: Label und Comment,
  **Default Inputs** (Spalten Name, Type, Value, dazu **ADD**),
  **Advanced** mit **Force start node** und **Default Error Node**,
  **Task Info** (Task-Bezeichner, Knoten-ID, Task-Typ, Kategorie,
  Pflicht- und optionale Eingaben, Ausgaben) sowie **Appearance**.

## Wann EWOKS — und wann nicht

- **Ja** — wiederkehrende, mehrstufige Datenverarbeitung: „wenn
  neue Daten ankommen, führe diese Schritte in dieser Reihenfolge
  aus" — reproduzierbar und beobachtbar statt ein Haufen Skripte.
- **Nein** — einmalige Ad-hoc-Auswertung (dafür passt ein
  Arbeitsbereich in [OpenScience](/suite/openscience)) oder
  simple Automatisierungen zwischen Suite-Diensten — das ist
  Terrain von [n8n](/suite/n8n).

EWOKS-Auswertungen laufen oft in den Arbeitsbereichen von
[OpenScience](/suite/openscience); beide Kacheln nutzen dasselbe
SSO-Konto.

## Barrierefreiheit

| Aktion | Taste |
|--------|-------|
| Durch Reiter, Schaltflächen und Dialoge bewegen | `Tab` |
| Fokussierten Link oder Schaltfläche öffnen | `Enter` |

- Beide Reiter sind gewöhnliche Links; Werkzeugleiste, Task-Liste,
  Canvas-Steuerung und Dialoge sind Schaltflächen — `Tab` erreicht
  sie der Reihe nach.
- Der Editor nennt seine Tasten für die Fläche selbst: Knoten mit
  Enter oder Leertaste auswählen, mit den Pfeiltasten verschieben,
  mit Entfernen löschen, mit Escape abbrechen. Verbindungen
  verhalten sich genauso.
- Das Aktionsmenü zeigt seine Kürzel: `Strg+Umschalt+N` für
  **New workflow**, `Strg+Umschalt+X` für **Execute workflow**.
- `Strg+Pos1` springt zum Seitenanfang zurück.
