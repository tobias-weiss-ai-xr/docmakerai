---
title: "Roadmap"
description: "Nächste Schritte für das SOGo 5 User Guide Projekt"
sidebar_label: "Roadmap"
---

# Roadmap — SOGo 5 User Guide

**Status:** ✅ Complete — 27 docs, 22 WebP animations, 14 PNG screenshots, English sidebar categories, GitHub Pages deployed

**Demo Sites:**
- SOGo 5: https://demo.sogo.nu/
- SOGo 6: https://demov6.sogo.nu/ *(Coming soon)*

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

**Status:** ✅ Basic GIFs embedded (10/10 core tutorials, 1 GIF per page).
⚠️ Annotierte Multi-Step GIFs (1-3 pro Seite) noch aus Phase 1 ausstehend.

**Ziel:** Jede Tutorial-Seite zeigt 1-3 annotierte GIFs inline an den passenden
Stellen. Die GIFs enthalten bereits Schritt-Indikatoren und UI-Markierungen
(aus Phase 1), sodass sie ohne zusätzlichen Text verständlich sind.

### Platzierungsstrategie

GIFs werden dort eingefügt, wo sie den beschriebenen Schritt visualisieren,
direkt unter der Schritt-Überschrift:

```
### Schritt 2: Doppelklick auf Zeitslot

![Schritt 2: Doppelklick öffnet Event-Dialog](./assets/calendar-create-event-dblclick.webp)

Doppelklicken Sie auf den gewünschten Zeitpunkt im Kalender.
Der Event-Dialog öffnet sich automatisch.

### Schritt 3: Formular ausfüllen

![Schritt 3: Titel und Ort eingeben](./assets/calendar-create-event-form.webp)

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
Alternativ: Zwei WebP-Sets generieren (`*-de.webp`, `*-en.webp`).

---

## Phase 4: SOGo 6 Migration & Updates

**Status:** 🟡 Planned — SOGo 6 demo available at https://demov6.sogo.nu/

### What's New in SOGo 6

**Demo Site:** [SOGo 6 Demo](https://demov6.sogo.nu/)

### Migration Tasks

| Task | Priority | Status |
|---|---|---|
| 🔍 Review SOGo 6 UI changes | High | Pending |
| 📋 Identify new/deprecated features | High | Pending |
| 🎬 Capture new UI screens | Medium | Pending |
| 📝 Update documentation for changed workflows | High | Pending |
| 🚀 Create new workflows for SOGo 6 features | Medium | Pending |

### Key Areas to Review

1. **Calendar Module**
   - Event creation dialog changes
   - New visualization options
   - Attendee management improvements

2. **Mail Module**
   - Compose interface updates
   - Folder management changes
   - Filtering and search enhancements

3. **Contacts Module**
   - Contact form modifications
   - Import/export improvements

4. **Overall UX**
   - Navigation changes
   - Settings and preferences layout updates
   - Mobile responsiveness improvements

### Timeline

- **TBD:** SOGo 6 official release announcement
- **TBD:** Full review of demo site
- **TBD:** Documentation update plan
- **TBD:** Captures for new features

---

## Phase 5: Optimierung & Automatisierung

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

| Phase | Aufwand | Schritte | Status |
|---|---|---|---|
| **Phase 1: Annotation-Engine + Capture** | ✅ Done | annotate.py → Step Tracker → run_captures.py → captcha pipeline | ✅ Complete |
| **Phase 2: GIFs einbetten** | ✅ Done | 27/27 Tutorials with WebP animations | ✅ Complete |
| **Phase 3: Sidebar Reorg & Translations** | ✅ Done | English/German categories → GitHub Pages deployment | ✅ Complete |
| **Phase 4: SOGo 6 Migration** | 🟡 TBD | Review demo → UI changes → New features → Documentation updates | 🟡 Planned |
| **Phase 5: Optimierung** | 🟡 TBD | GIF-Größen prüfen, Farben optimieren, ggf. croppen | 🟡 Planned |

---

## Completed Work ✅

- ✅ 27 documentation pages created (up from 11)
- ✅ 22 WebP animations generated for core workflows
- ✅ 14 PNG screenshots integrated, all broken references fixed
- ✅ 20 orphan assets deleted (10 GIFs + 7 PNGs + 3 images)
- ✅ Sidebars reorganized into 7 English categories: Getting Started, Basics, Calendar, Mail, Contacts, Tools, Advanced
- ✅ Frame validation added to detect blank screenshots
- ✅ Project deployed to GitHub Pages (https://tobias-weiss-ai-xr.github.io/docmakerai/sogo5/)
- ✅ Build verified for both English and German locales

---

## Next Steps

### Immediate (SOGo 5 Maintenance)

- 🔄 Monitor GitHub Pages deployment and image loading
- 📋 Review and fix any broken image references
- 🌐 Ensure all 27 docs display correctly in both en/de locales

### Coming Soon (SOGo 6)

1. 🔍 **Review SOGo 6 Demo** — Visit https://demov6.sogo.nu/ and catalog UI changes
2. 📋 **Feature Comparison** — Document what's new, changed, or deprecated in SOGo 6
3. 🎬 **Plan Captures** — Identify workflows needing new screenshots/animations
4. 📝 **Documentation Updates** — Update existing docs for SOGo 6 UI changes
5. 🚀 **New Features** — Document SOGo 6-specific features not in SOGo 5

### Future (Optimization)

- Phase 5: WebP size optimization
- Phase 5: Automatic re-captures on SOGo updates
- Phase 5: MP4 alternative evaluation if WebPs grow too large

---

**Last Updated:** 2025-06-17
**Current Version:** SOGo 5 User Guide
**Next Version:** SOGo 6 guide (coming soon!)
