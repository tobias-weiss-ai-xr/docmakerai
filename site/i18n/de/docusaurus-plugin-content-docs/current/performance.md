---
title: "Performance-Dashboard"
description: "Live-Lighthouse-Werte, Bundle-Größen und Erfassungszeiten für die SOGo-Benutzerhandbuch-Website."
sidebar_label: "Performance"
---

# Performance-Dashboard

Diese Seite verfolgt die Performance-Eigenschaften der SOGo-Benutzerhandbuch-Website. Bei jedem Push auf `main` wird die Lighthouse-CI gegen die Live-Website und der Bundle-Größen-Check gegen das Build-Artefakt ausgeführt.

## Lighthouse-Werte

Die Werte werden bei jedem Push auf `main` gegen die Live-Produktionswebsite gemessen. Die Rohdaten finden Sie im [Lighthouse-CI-Workflow-Lauf](../../../../actions/workflows/ci.yml).

| Metrik: | Budget: | Quelle: |
| ------- | ------ | ------ |
| Performance-Wert | ≥ 85 | `categories:performance` |
| Largest Contentful Paint (LCP) | ≤ 2,5 s | `largest-contentful-paint` |
| Total Blocking Time (TBT) | ≤ 300 ms | `total-blocking-time` |
| Cumulative Layout Shift (CLS) | ≤ 0,1 | `cumulative-layout-shift` |

Die vollständige Konfiguration befindet sich in `.lighthouserc.json` im Repository-Stammverzeichnis.

## Bundle-Größe (gzip)

Wird bei jedem PR verfolgt. Der Build schlägt fehl, wenn die Budgets überschritten werden. PR-Kommentare zeigen die aktuellen Größen inline an.

| Asset-Klasse: | Budget: | Quelle: |
| ----------- | ------ | ------ |
| Gesamtes JS | ≤ 580 KiB | Summe der gzip-Größen von `site/build/assets/js/*.js` |
| Gesamtes CSS | ≤ 100 KiB | Summe der gzip-Größen von `site/build/assets/css/*.css` |
| Größtes einzelnes JS-Chunk | ≤ 220 KiB (raw) | maximale einzelne Datei in `site/build/assets/js/` |

Die Budget-Konfiguration befindet sich inline in `.github/workflows/ci.yml`
(Job `bundle-size`).

## Bundle-Profil

Die Produktions-Builds nutzen einen Vendor-Split (`vendorSplitPlugin` in
`docusaurus.config.ts`): Die React-Laufzeit und die Suchmaschinen-Laufzeit
(lunr) sind in eigene Chunks mit stabilem Hash ausgelagert. Diese Chunks
ändern sich zwischen Deployments nicht und bleiben im Browser-Cache,
während sich `main.js` bei jedem Build ändert. Gemessen an der
Build-Ausgabe (`site/build/assets/js/`), gzip-Größen mit `gzip -9`.

### Profil nach dem Split (2026-11-28)

| Chunk | Raw-Größe | Gzip-Größe | Ladeverhalten |
| ----- | --------- | ---------- | -------------- |
| `main.<hash>.js` (App-Shell) | 320 KB | 96 KB | eager auf jeder Route |
| `framework.<hash>.js` (react, react-dom, scheduler) | 190 KB | 60 KB | eager, cache-stabil über Deployments |
| `search.<hash>.js` (lunr, Search-Laufzeit) | 120 KB | 38 KB | eager, cache-stabil über Deployments |
| Gesamtes JS (gzip) | — | 528 KB | — |

Vor dem Split (Docusaurus 3.10.2, 2026-11-27) war die Shell allein
565 KB raw / 172 KB gzip — die React-Laufzeit und die komplette
Suchmaschine wurden auf jeder Seite innerhalb von `main.js` geparst.
Der Split verkleinerte `main.js` um 43 % (raw); die ausgegliederten
Chunks behalten ihren Hash, solange sich die pinned dependencies nicht
ändern, sodass wiederkehrende Besucher sie aus dem Cache laden.

### Warum das zählt

- `main.js` wird bei jeder Navigation geparst und ausgeführt — mit
  96 KB gzip liegt es deutlich unter einem Drittel seiner früheren
  Größe.
- Budget-Puffer: Der größte Chunk liegt jetzt bei 190 KB raw gegen
  220 KiB Budget — Größen-Drift einer einzelnen Bibliothek bringt das
  Tor nicht mehr in Gefahr.

### Das Fußprint klein halten

- Route-level Code-Splitting hält seitenspezifische Module aus der
  Shell (bereits aktiv: jede Seite ist ein eigener Chunk).
- Ein verzögerter Suchstart könnte die Kosten des `search`-Chunks
  vollständig aus dem kritischen Pfad nehmen — Kandidat für eine
  künftige Iteration.
- Eine Dependency-Audit von `@docusaurus/*` und dem Classic-Theme kann
  ungenutzte Module entfernen, bevor sie die Shell erreichen.
- Prüfen Sie das Profil nach jedem Release mit dem Bundle-Size-CI-Job,
  damit der Trend auf PRs sichtbar bleibt.

## Barrierefreiheit

Diese Seite ist so gestaltet, dass sie für alle Benutzer zugänglich ist, einschließlich derer, die Screenreader oder Tastaturnavigation verwenden.

### Tastaturnavigation

| Tastenkombination: | Aktion: |
| --------- | ------ |
| `Tab` | Zwischen interaktiven Elementen auf der Seite navigieren |
| `Eingabe` / `Leertaste` | Links und Schaltflächen aktivieren |

### Screenreader- & Hochkontrast-Unterstützung

- Alle Tabellen verwenden korrekte Kopfzeilen-Marker für die Screenreader-Navigation
- Links verwenden beschreibende Texte, die auch ohne Kontext sinnvoll sind
- Farbe wird nicht als alleiniges Mittel zur Übermittlung von Informationen verwendet
- Der Hochkontrast- und Dunkelmodus werden über die Media-Queries `prefers-contrast: more` und `prefers-color-scheme: dark` des Systems unterstützt

## Zeitmessung der Erfassungs-Pipeline

Jeder Erfassungslauf erzeugt eine `report.json` mit den Dauern pro Workflow. Die langsamsten Workflows des letzten Laufs werden in den CI-Artefakten angezeigt.

Der vollständige Bericht enthält:

- `total_duration_seconds` — Summe aller Workflow-Dauern
- `slowest_workflow` — der Workflow, der am längsten gedauert hat
- `slowest_duration_seconds` — seine Dauer
- `workflows[]` — pro Workflow `{name, status, duration_seconds, annotated_frames, file_size_kb}`

Die Nachverfolgung befindet sich in `capture/capture_report.py` (das Feld `duration_seconds` wurde in Sprint 15 hinzugefügt).

## Warum das wichtig ist

Eine Dokumentationswebsite, deren Laden mehr als 10 Sekunden dauert, verfehlt den Zweck der Dokumentation. Diese Budgets fangen Regressionen **bevor sie ausgeliefert werden** — ein PR, der das Bundle um 200 KB aufbläht, lässt die CI fehlschlagen, nicht die Produktion.

## Budgets aktualisieren

Bearbeiten Sie `.lighthouserc.json` (Lighthouse) oder die Inline-Budgets in `.github/workflows/ci.yml` (Bundle-Größe). Begründen Sie jede Erhöhung in der PR-Beschreibung.
