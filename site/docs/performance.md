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
| Total JS | ≤ 500 KB | summed gzip of `site/build/assets/js/*.js` |
| Total CSS | ≤ 100 KB | summed gzip of `site/build/assets/css/*.css` |
| Largest single JS chunk | ≤ 500 KB | max single file in `site/build/assets/js/` |

The budget configuration lives in `.github/bundle-budget.json`.

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
