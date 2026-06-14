---
title: "Roadmap"
description: "Nächste Schritte für das SOGo 5 User Guide Projekt"
sidebar_label: "Roadmap"
---

# Roadmap — SOGo 5 User Guide

**Ziel:** Alle 10 Tutorials mit kurzen (5-10s) animierten GIF-Clips ergänzen, die
Schlüsselschritte zeigen und direkt in die Markdown-Seiten eingebettet sind.

---

## Phase 1: Annotation-Engine + Capture-Pipeline

**Problem:** Aktuell 3 Workflows mit GIFs, aber nur 2 Frames (Vorher/Nachher).
Keine Zwischenschritte sichtbar, keine Markierungen.

**Lösung:** Action-Driven Captures mit Mikro-Capture-Punkten + Post-Processing
Annotation-Engine, die Schritt-Indikatoren und UI-Highlights auf die Frames zeichnet.

### Komponenten

#### A) Step Tracker — Metadaten während des Captures sammeln

Jede Capture-Funktion dokumentiert pro Frame:
- **step_label**: z.B. `"Doppelklick auf Zeitslot 10:00"`
- **highlights**: Liste von Element-Positionen für Pfeile/Kreise
  - via `bounding_box()` auf Playwright-Locators
  - Farbe (z.B. `"red"` für Klick-Ziele, `"blue"` für Ergebnisse)

```python
# Beispiel-Struktur
capture_context = {
    'frames': [
        {
            'file': '01-calendar-view.png',
            'step': 'Kalender in Wochenansicht',
            'highlights': []
        },
        {
            'file': '02-dblclick.png',
            'step': 'Doppelklick auf Montag 10:00',
            'highlights': [
                {'bbox': {'x': 200, 'y': 300, 'w': 100, 'h': 30}, 'color': 'red', 'type': 'circle'},
            ]
        },
        {
            'file': '03-event-dialog.png',
            'step': 'Event-Dialog: Titel eingeben',
            'highlights': [
                {'bbox': {'x': 400, 'y': 150, 'w': 300, 'h': 40}, 'color': 'green', 'type': 'arrow'},
            ]
        },
    ]
}
```

#### B) Post-Processor — Overlays auf Frames zeichnen (Pillow/PIL)

Nach dem Capture-Durchlauf werden alle Frames annotiert:

- **Step-Header**: Halbtransparenter Balken oben im Bild
  - Schrift: Schrittnummer + Label (z.B. `"① Doppelklick auf Zeitslot"`)
  - Hintergrund: dunkel mit weisser Schrift
- **UI-Highlights**: Rote Kreise oder Pfeile auf UI-Elemente
  - Position aus den im Step Tracker gespeicherten `bounding_box`-Koordinaten
  - `type='circle'` → roter Kreis um das Element
  - `type='arrow'` → Pfeil vom oberen Bildrand auf das Element
- **Fade-Hintergrund**: Optionale Abdunklung des nicht-relevanten Bereichs

Beispiel-Visualisierung eines annotierten Frames:

```
┌─────────────────────────────────────────────────────┐
│ ████████████████████████████████████████████████████ │  ← Step-Header
│ ██ ① Doppelklick auf Montag 10:00            ██ │  ← Schritt-Titel
│ ████████████████████████████████████████████████████ │
│                                                     │
│   ┌─────────────────────────────────────────┐       │
│   │   Wochenansicht                          │       │
│   │    Mo  Di  Mi  Do  Fr                   │       │
│   │    ┌──┐                                  │       │
│   │    │🔴│ ← roter Kreis auf Element        │       │
│   │    └──┘                                  │       │
│   │    10:00                                 │       │
│   └─────────────────────────────────────────┘       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

Technisch: `PIL.ImageDraw` + `PIL.ImageFont` für Text, `ellipse()` für Kreise,
und `polygon()` für Pfeile.

### Workflow-GIF-Plan

Jeder Workflow bekommt 1-3 kurze GIF-Sequenzen (je 5-10s, ca. 8-15 Frames):

| Workflow | GIFs | Inhalt |
|---|---|---|
| Calendar Create Event | 3 | (1) Doppelklick → Dialog (2) Formular ausfüllen (3) Speichern → OK |
| Calendar Recurring | 2 | (1) Repeat → Weekly (2) Serie gespeichert |
| Mail Compose | 2 | (1) Inbox → Compose (2) Felder + Anhang |
| Contacts Add | 1 | Kontakt anlegen + speichern |
| Vacation | 1 | Auto-Reply aktivieren |
| Mail Signatures | 1 | Signatur erstellen |
| Mail Folders & Filters | 2 | (1) Ordner anlegen (2) Filter-Regel |
| Calendar Subscribe | 1 | iCal-Feed abonnieren |
| Calendar Share | 1 | Kalender teilen |
| Free/Busy | 2 | (1) Event mit Attendees (2) Verfügbarkeitsgrid |

### Timing-Strategie (pro GIF 5-10s)

| Frame-Typ | Verweildauer | Einsatz |
|---|---|---|
| Nach Seitenwechsel | 1200ms | Ladevorgang sichtbar |
| Nach Klick | 800ms | Dialog öffnet sich |
| Nach Formular-Eingabe | 600ms | Text erscheint |
| Ruhezustand / Lesepause | 1500ms | Wichtiger Zustand, Nutzer soll lesen |
| Abschluss / Bestätigung | 2000ms | Letzter Frame, länger sichtbar |

### Datei-Struktur

```
capture/
  run_captures.py        ← Step Tracker + Capture-Logik
  annotate.py            ← Post-Processor (Pillow Overlays)
  segments/              ← Roh-Screenshots + Metadaten (temporär)
    calendar-create-event/
      step01.json
      step01.png
      ...
  screenshots/           ← Annotierte Frames (Output)
  gifs/                  ← Fertige GIFs (Output)
```

---

## Phase 2: GIFs in Tutorial-Seiten einbetten

**Ziel:** Jede Tutorial-Seite zeigt 1-3 annotierte GIFs inline an den passenden
Stellen. Die GIFs enthalten bereits Schritt-Indikatoren und UI-Markierungen
(aus Phase 1), sodass sie ohne zusätzlichen Text verständlich sind.

### Platzierungsstrategie

GIFs werden dort eingefügt, wo sie den beschriebenen Schritt visualisieren,
direkt unter der Schritt-Überschrift:

```
### Schritt 2: Doppelklick auf Zeitslot

![Schritt 2: Doppelklick öffnet Event-Dialog](./assets/calendar-create-event-dblclick.gif)

Doppelklicken Sie auf den gewünschten Zeitpunkt im Kalender.
Der Event-Dialog öffnet sich automatisch.

### Schritt 3: Formular ausfüllen

![Schritt 3: Titel und Ort eingeben](./assets/calendar-create-event-form.gif)

Geben Sie den Titel und optional den Ort des Events ein.
```

### Annotierte GIFs vs. statische Screenshots

- **GIFs** zeigen die **Aktion** (Klick, Eingabe, Übergang)
- **Screenshots** zeigen den **Zustand** (das fertige Formular, die Ansicht)
- Beide existieren parallel — GIFs ergänzen, ersetzen nicht

### i18n-Hinweis

Annotierte GIFs enthalten deutschen Text (Schritt-Indikatoren), da die
Tutorials auf Deutsch primär sind. Englische Variante: Die Overlay-Texte
werden via Konfiguration umgeschaltet (`locale='de' | 'en'` im Annotator).
Alternativ: Zwei GIF-Sets generieren (`*-de.gif`, `*-en.gif`).

---

## Phase 3: Optimierung & Automatisierung

- **GIF-Größe optimieren**: Max 300KB pro GIF durch
  - Farbpalette auf 128 Farben reduzieren
  - Bei ähnlichen aufeinanderfolgenden Frames: nur jeden 2. Frame ins GIF
  - Viewport ggf. auf relevanten Bereich croppen
- **Automatische Re-Captures**: CI/CD-Workflow, der bei SOGo-Updates
  neu captured (benötigt `workflow` Scope für GitHub Token)
- **MP4-Alternative**: Falls GIFs zu groß werden, auf `<video>`-Tag mit
  MP4 umstellen (deutlich kleinere Dateien, Play/Pause-Steuerung)

---

## Zeitplan (Schätzung)

| Phase | Aufwand | Schritte |
|---|---|---|
| **Phase 1: Annotation-Engine + Capture** | ~3h | annotate.py schreiben → Step Tracker → run_captures.py refaktorieren → alle Workflows → Captures laufen lassen → GIFs erzeugen |
| **Phase 2: GIFs einbetten** | ~1h | Markdowns editieren, GIF-Referenzen pro Schritt einfügen |
| **Phase 3: Optimierung** | ~1h | GIF-Größen prüfen, Farben optimieren, ggf. croppen |

---

## Nächster Schritt

Phase 1 umsetzen:
1. `capture/annotate.py` schreiben (Pillow Overlay-Engine)
2. `run_captures.py` mit Step-Tracker-Metadaten erweitern
3. Alle 10 Workflows mit GIF-Segmenten ausstatten
4. Capture-Durchlauf + GIF-Erzeugung
5. GIFs nach `site/docs/assets/` kopieren

Dann Phase 2: GIFs in Tutorial-Markdowns einbinden.
