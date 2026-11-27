---
title: "Roadmap"
description: "Optimierungs- & Automatisierungs-Roadmap — SOGo-Benutzerhandbuch (5 & 6)"
sidebar_label: "Roadmap"
---

# Roadmap — SOGo-Benutzerhandbuch (5 & 6)

**Status:** ✅ Veröffentlicht — 27 SOGo-5-Dokumente, 36 visuelle Assets (WebP + PNG), Docusaurus-Versionierung für SOGo 5 + SOGo 6, CI/CD mit selbst gehosteten Runnern, 99,34 % Testabdeckung, SEO/GEO-Ausrichtung, aufgabenorientierter Erfassungsfluss mit HTML5-Video

**Demo-Websites:**
- SOGo 5: https://demo.sogo.nu/
- SOGo 6: https://demov6.sogo.nu/

**Build-Status:** CI-Pipeline mit selbst gehostetem Runner auf einem internen Host. Builds dauern ca. 4–5 Minuten (gecacht) / ca. 10 Minuten (kalt).

**Staging:** Zurückgestellt — eigenes Preview-Bereitstellungssystem ersetzt Netlify (siehe Sprint 13).

---

## Abgeschlossen ✅

### Sprint 1: Spezifikations-Grundlage (OpenSpec)
- [x] Verzeichnisstruktur `openspec/specs/` initialisieren
- [x] Spezifikationen für die Kernbereiche der Erfassungs-Pipeline schreiben: Auth-Login, Kalender, E-Mail, Kontakte, Einstellungen
- [x] Jede Spezifikation enthält: Zweck, Anforderungen (RFC 2119), Szenarien (Gegeben/Wenn/Dann)
- [x] `openspec/config.yaml` mit Projekteinstellungen konfigurieren

### Sprint 2: CI/CD-Pipeline
- [x] `.github/workflows/ci.yml` erstellen — läuft bei Push/PR auf `main`
- [x] **Lint:** ruff für den Python-Code in `capture/`
- [x] **Test:** pytest mit 99,34 % Abdeckung in `capture/tests/` + `accessibility/tests/`
- [x] **Build:** Docusaurus-Build für beide Locales `en` + `de`
- [x] **Deploy:** GitHub-Pages-Bereitstellung bei Push auf `main`
- [x] Selbst gehosteter Runner auf einem internen Host mit Label `linux`
- [x] Runner-Dienst: `docmaker-runner`

### Sprint 3: Asset-Optimierung
- [x] `capture/optimize.py` erstellen — Stapel-Bildoptimierer
- [x] WebP-Optimierung: Reduzierung der Farbpalette, Frame-Überspringen, Entfernen von Metadaten
- [x] PNG-Optimierung: pngquant, Entfernen von Metadaten
- [x] 36 Tests für optimize.py
- [x] 54 % Größenreduzierung erreicht (2,1 MB → 976 KB pro Version)

### Sprint 4: Erfassungs-Zuverlässigkeit
- [x] Validierungsschritt hinzufügen: Leerflächen-Erkennung (>90 % Weißanteil)
- [x] Strukturierte Protokollierung von Erfassungsfehlern
- [x] `capture/capture_report.py` erstellen — Qualitätsbericht für Artefakte
- [x] Nach-Erfassungslogik mit Wiederholung

### Sprint 5: Parallele Ausführung
- [x] Parallele Workflow-Ausführung implementieren
- [x] Konfigurierbare Worker über Semaphore
- [x] Sequenzielle Reihenfolge für Abhängigkeiten (Login → Workflows)
- [x] 12 Tests für parallel_runner.py

### Sprint 6: Barrierefreiheits-Gates
- [x] `accessibility/validate.py` als CI-Schritt integrieren
- [x] Auto-Fix-Modus für behebbare Probleme hinzufügen (Überschriftenhierarchie, Tabellenköpfe)
- [x] 30 Tests für accessibility/validate.py
- [x] WCAG-2.1-Level-A-Checklisten-Generierung

### Sprint 7: Video/MP4-Pipeline
- [x] `scripts/convert_to_mp4.py` erstellen — WebP → MP4 (H.264) + WebM (VP9)
- [x] MP4: libx264, CRF 23, yuv420p, Fast-Start
- [x] WebM: libvpx-vp9, CRF 30
- [x] Thumbnail-/Poster-Generierung

### Sprint 8: User Journeys & SEO
- [x] Aufgabenorientierter Erfassungsfluss mit 4-Schritt-Erzählung (Kontext, Herausforderung, Lösung, Ergebnis)
- [x] Menschenähnliche Eingabe (120 ms Verzögerung bei Formularfeldern)
- [x] SEO-Komponenten: Open Graph, Twitter Cards, Schema.org (SoftwareApplication, HowTo, TechArticle)
- [x] GEO-Ausrichtung: geo.region="DE", geo.placename="Berlin", ICBM
- [x] Pfad-Umstrukturierung: sogo5/sogo6 statt /5//6/
- [x] Sidebar in 7 Kategorien mit Emoji-Icons neu organisiert

### Sprint 2b: CI-Zuverlässigkeit
- [x] Optimierung der Docusaurus-Buildzeit (4–5 Min. gecacht, ~10 Min. kalt — gegenüber 30+ reduziert)
- [x] Stabilität von Python-Lint/Test (PEP-668-Kompatibilität mit --break-system-packages)
- [x] Node.js-Versionskompatibilität (Node 20 vs. Node 24 auf Arch-Rolling)
- [x] Branch-Schutzregeln: getrennte CI-Statusprüfungen vom Deploy-Gate
- [x] Runner-Ressourcenkonflikte: Lastverteilung zwischen CI/Deploy/Preview-Workflows

### Sprint 9: Performance-Benchmarks
- [x] Lighthouse-CI in `.github/workflows/ci.yml` hinzufügen
- [x] Bundle-Größen-Tracking hinzufügen
- [x] Erfassungs-Zeitmesswerte zu `capture_report.py` hinzufügen
- [x] Performance-Budgets festlegen (LCP `&lt;2,5 s`, Gesamt-Bundle `&lt;500 KB` gzip)
- [x] Performance-Dashboard-Seite unter `site/docs/performance.md` erstellen

### Sprint 12: Spec-to-Docs-Pipeline
- [x] Dokumentationsseiten automatisch aus OpenSpec-Spezifikationen generieren
- [x] Tutorial-Struktur aus Spezifikationsszenarien
- [x] Asset-Einbettung aus Erfassungsmetadaten
- [x] Automatische Docusaurus-Sidebar-Generierung
- [x] `scripts/generate_docs_from_specs.py` (593 Zeilen) im Commit `25bed47` ausgeliefert

### Sprint 14: Repo-Hygiene
- [x] `.github-pages-trace`-Debug-Artefakt aus der Versionskontrolle nehmen
- [x] Leeres Verzeichnis `docs/` entfernen
- [x] ROADMAP mit dem tatsächlichen Stand abgleichen
- [x] CI-Wächter für Abdeckungsschwellen-Regression (>0,5 % Abfall schlägt PR fehl)

### Sprint 11: SOGo-Änderungserkennung
- [x] `capture/detect_changes.py` erstellen — Wahrnehmungshash-UI-Diff
- [x] ImageHash-basierter Screenshot-Vergleich (pHash, 64-Bit)
- [x] Hamming-Distanz-Schwelle (Standard: 10 Bits)
- [x] Automatische Baseline-Aktualisierung bei Drift-Erkennung
- [x] Nächtlicher CI-Workflow (`.github/workflows/change-detection.yml`) erstellt GitHub-Issue bei Drift
- [x] `capture/run_captures.py` integriert Drift-Prüfung pro Workflow
- [ ] DOM-Strukturvergleich (zurückgestellt — pHash deckt die meisten Fälle ab)

### Infrastruktur
- [x] Selbst gehosteter Runner auf einem internen Host
- [x] Runner-Name: docmaker-runner
- [x] Labels: linux
- [x] SSH-Konfiguration aktualisiert
- [x] Testabdeckung: 99,34 % (192/192 Tests bestanden)
- [x] coverage.xml-Artefakt-Upload in CI

---

## In Arbeit 🔵

_Keine — alle erfassten Sprints sind entweder abgeschlossen oder geplant._

---

## Abgeschlossen ✅

_Alle Sprints abgeschlossen. DOM-Strukturvergleich in Sprint 11 zurückgestellt (pHash deckt die meisten Fälle ab)._

### Sprint 10: Inhaltserweiterung
- [x] Kritische Workflows mit aufgabenorientiertem Ansatz neu erfasst (3 vorhandene WebM in MP4 konvertiert)
- [x] Aufgabenorientierte WebP-Aufnahmen in MP4 konvertiert (3 Videos optimiert, 6–11 % kleiner)
- [x] VideoFallback-Komponente und WebVTT-Untertitel hinzugefügt (Komponente erstellt + 1 Tutorial aktualisiert)
- [x] PageSEO zu wichtigen Tutorial-Seiten hinzugefügt (Compose, Kontakt hinzufügen, Antworten/Weiterleiten, Bearbeiten/Löschen)
- [x] Vollständige deutsche Übersetzung von `/sogo5/de/`

### Sprint 13: PR-Preview-Bereitstellungen
- [x] `preview-deploy.yml` neu geschrieben — Build mit dynamischem baseUrl, Bereitstellung unter `gh-pages/preview/pr-<N>/`
- [x] Preview-URL wird bei PRs als Kommentar eingefügt (ersetzt vorhandenen Kommentar statt zu spammen)
- [x] Teardown-Workflow (`preview-cleanup.yml`) — löscht Preview-Verzeichnis beim Schließen des PR
- [x] Workflow-README mit Preview-URL-Informationen aktualisieren
- [x] Entscheidung: gh-pages-Unterverzeichnis `/preview/` (gewählt statt Staging-Branch)

---

## Barrierefreiheit

Diese Dokumentationswebsite unterstützt Tastaturnavigation, Screenreader und den Hochkontrastmodus.

### Tastaturnavigation

| Tastenkombination: | Aktion: |
| --------- | ------ |
| `Tab` | Zwischen Links und interaktiven Elementen navigieren |
| `Eingabe` / `Leertaste` | Links und Schaltflächen aktivieren |
| `Strg + F` | Innerhalb der aktuellen Seite suchen |

### Screenreader & Hochkontrast

- Alle Tabellen verwenden korrekte Kopfzeilen-Marker (Format `| Kopfzeile |`) für die Spaltennavigation mit dem Screenreader
- Status-Icons enthalten Textalternativen (z. B. „✅ Abgeschlossen“ und nicht nur ein Emoji)
- Der Hochkontrastmodus wird über die Media-Queries `prefers-contrast: more` des Systems unterstützt
- Farbe ist niemals das alleinige Mittel zur Übermittlung von Informationen

## Bekannte Probleme

| Problem: | Status: | Anmerkungen: |
| ----- | ------ | ----- |
| Docusaurus-Build dauert 30+ Min. auf dem internen Runner | 🔵 | Node 24 vs. Node 20, npm-Cache kalt |
| Python PEP 668 blockiert pip | ✅ Behoben | `--break-system-packages` hinzugefügt |
| Unendliche Schleife von `@docusaurus/remark-plugin-content-docs` | ✅ Behoben | Plugin entfernt, manuelle PageSEO-Imports verwendet |
| Intermittierende GitHub-API-Konnektivität | ⚠️ | Verbindungsprobleme zu `api.github.com` |
| Deploy-Workflow hängt beim Deutschen-Locale-Build | 🔵 | Vermutlich Node.js-Versionskonflikt |

---

## Legende

| Icon: | Bedeutung: |
| ---- | ------- |
| ✅ | Abgeschlossen |
| 🔵 | In Arbeit |
| 🟡 | Geplant |
| ❌ | Blockiert |
| ⚠️ | Beeinträchtigt |

---

**Zuletzt aktualisiert:** 2026-06-29
**Nächster Sprint:** Keiner — Roadmap abgeschlossen. Zukünftige Arbeiten werden über GitHub-Issues verfolgt.

---

## Anhang: Wichtige Kennzahlen

| Kennzahl: | Wert: |
| ------- | ----- |
| Testabdeckung | 99,34 % (192/192 bestanden) |
| CI-Runner | Selbst gehostet auf einem internen Host |
| Runner-Labels | linux |
| Runner-Version | 2.335.1 |
| SEO-Geo-Tags | geo.region=DE, geo.placename=Berlin, ICBM |
| Größenreduzierung der Assets | 54 % (2,1 MB → 976 KB) |
| Dokumentationsseiten | 27 SOGo-5- + 30-SOGo-6-Dokumente |
| Pfadstruktur | /sogo5/, /sogo6/ |
