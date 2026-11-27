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
| Gesamtes JS | ≤ 500 KB | Summe der gzip-Größen von `site/build/assets/js/*.js` |
| Gesamtes CSS | ≤ 100 KB | Summe der gzip-Größen von `site/build/assets/css/*.css` |
| Größtes einzelnes JS-Chunk | ≤ 500 KB | maximale einzelne Datei in `site/build/assets/js/` |

Die Budget-Konfiguration befindet sich in `.github/bundle-budget.json`.

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
