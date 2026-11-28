---
title: "Performance Dashboard"
description: "Live Lighthouse scores, bundle sizes, and capture timing for the SOGo User Guide site."
sidebar_label: "Performance"
---

# Performance Dashboard

This page tracks the performance characteristics of the SOGo User Guide documentation site. Every push to `main` runs Lighthouse CI against the live site and the bundle-size check against the build artifact.

## Lighthouse Scores

Scores are measured against the live production site on every push to `main`. See the [Lighthouse CI workflow run](../../../../actions/workflows/ci.yml) for raw data.

| Metric: | Budget: | Source: |
| ------- | ------ | ------ |
| Performance score | ≥ 85 | `categories:performance` |
| Largest Contentful Paint (LCP) | ≤ 2.5 s | `largest-contentful-paint` |
| Total Blocking Time (TBT) | ≤ 300 ms | `total-blocking-time` |
| Cumulative Layout Shift (CLS) | ≤ 0.1 | `cumulative-layout-shift` |

The full configuration lives in `.lighthouserc.json` at the repo root.

## Bundle Size (gzip)

Tracked on every PR. Fails the build if budgets are exceeded. PR comments show the current sizes inline.

| Asset class: | Budget: | Source: |
| ----------- | ------ | ------ |
| Total JS | ≤ 580 KiB | summed gzip of `site/build/assets/js/*.js` |
| Total CSS | ≤ 100 KiB | summed gzip of `site/build/assets/css/*.css` |
| Largest single JS chunk | ≤ 220 KiB (raw) | max single file in `site/build/assets/js/` |

The budget configuration lives inline in `.github/workflows/ci.yml`
(`bundle-size` job).

## Bundle-Profil

Die Produktions-Builds nutzen einen Vendor-Split (`vendorSplitPlugin` in
`docusaurus.config.ts`): Die React-Laufzeit und die Suchmaschinen-Laufzeit
(lunr) sind in eigene Chunks mit stabilem Hash ausgelagert. Diese Chunks
ändern sich zwischen Deployments nicht und bleiben im Browser-Cache,
während sich `main.js` bei jedem Build ändert. The numbers below were
measured from `docusaurus build` output (`site/build/assets/js/`); gzip
sizes use `gzip -9`.

### Post-split profile (2026-11-28)

| Chunk | Raw size | Gzip size | Load behaviour |
| ----- | -------- | --------- | -------------- |
| `main.<hash>.js` (app shell) | 320 KB | 96 KB | eager on every route |
| `framework.<hash>.js` (react, react-dom, scheduler) | 190 KB | 60 KB | eager, cache-stable across deploys |
| `search.<hash>.js` (lunr, search-local runtime) | 120 KB | 38 KB | eager, cache-stable across deploys |
| Total JS (gzip) | — | 528 KB | — |

Before the split (Docusaurus 3.10.2, 2026-11-27), the shell alone was
565 KB raw / 172 KB gzip — the react runtime and the full search engine
were parsed inside `main.js` on every page. The split moved them into
independent chunks: `main.js` shrank by 43% (raw), and the extracted
chunks keep their hash as long as the pinned dependencies do not change,
so returning visitors load them from cache.

### Composition notes

- `framework.js` is the react/react-dom/scheduler runtime — fixed cost,
  rarely changes.
- `search.js` is the lunr search engine with the en/de language
  trimmers. It loads eagerly with the navbar search bar, but sits in its
  own cache-stable chunk instead of the rotating shell.
- `main.js` is the Docusaurus core and classic-theme bootstrap plus the
  Prism syntax-highlighting engine behind code blocks and small shared
  utilities such as the clipboard copy-button helper.
- Page content (each guide, the landing page) lives in route-level
  chunks and is outside these numbers.

### Why it matters

- `main.js` is parsed and executed on every navigation, not just on
  first load; at 96 KB gzip it is well under a third of its former size.
- Budget headroom: the largest chunk is now 190 KB raw against a
  220 KiB budget — drift in any single library no longer threatens the
  gate.

### Keeping the footprint small

- Route-level code-splitting keeps page-specific modules out of the
  shell (already active: every page is its own chunk).
- Lazy-loading heavy dependencies (for example a deferred search
  bootstrap) could move the `search` chunk cost out of the critical path
  entirely — candidate for a future iteration.
- A dependency audit of `@docusaurus/*` and the classic theme can drop
  unused modules before they reach the shell.
- Re-check the profile after each release using the bundle-size CI job
  so the trend stays visible on PRs.


## Accessibility

This page is designed to be accessible to all users, including those using screen readers or keyboard navigation.

### Keyboard Navigation

| Shortcut: | Action: |
| --------- | ------ |
| `Tab` | Navigate between interactive elements on the page |
| `Enter` / `Space` | Activate links and buttons |

### Screen Reader & High Contrast Support

- All tables use proper header markers for screen reader navigation
- Links use descriptive text that makes sense out of context
- Color is not used as the sole means of conveying information
- High-contrast mode and dark mode are supported via system `prefers-contrast: more` and `prefers-color-scheme: dark` media queries

## Capture Pipeline Timing

Each capture run produces a `report.json` with per-workflow durations. The slowest workflows from the last run are surfaced in CI artifacts.

The full report includes:

- `total_duration_seconds` — sum of all workflow durations
- `slowest_workflow` — the workflow that took the longest
- `slowest_duration_seconds` — its duration
- `workflows[]` — per-workflow `{name, status, duration_seconds, annotated_frames, file_size_kb}`

Tracking lives in `capture/capture_report.py` (the `duration_seconds` field added in Sprint 15).

## Why this matters

A documentation site that takes 10+ seconds to load defeats the purpose of the docs. These budgets catch regressions **before they ship** — a PR that bloats the bundle by 200 KB fails CI, not production.

## Updating budgets

Edit `.lighthouserc.json` (Lighthouse) or the inline budgets in `.github/workflows/ci.yml` (bundle size). Justify any increase in the PR description.
