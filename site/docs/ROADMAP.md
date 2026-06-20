---
title: "Roadmap"
description: "Optimization & Automation Roadmap — SOGo User Guide (5 & 6)"
sidebar_label: "Roadmap"
---

# Roadmap — SOGo User Guide (5 & 6)

**Status:** ✅ Published — 27 SOGo 5 docs (14 with valid captures, 8 with blank captures replaced, 5 conceptual), 22 WebP animations (14 valid, 8 blank), 14 PNG screenshots (11 valid, 3 blank), Docusaurus versioning configured for SOGo 5 + SOGo 6

**Demo Sites:**
- SOGo 5: https://demo.sogo.nu/
- SOGo 6: https://demov6.sogo.nu/

---

## Overview

The project has delivered a full SOGo 5 User Guide with 27 documentation pages, 36 visual assets (WebP + PNG), and Docusaurus multi-version support for SOGo 5 + SOGo 6.

This roadmap focuses on **optimization & automation** — reducing asset sizes, hardening the capture pipeline, adding CI/CD, and introducing spec-driven development.

---

## Sprint 1: Spec Foundation (OpenSpec)

**Goal:** Establish a spec-driven development workflow for the capture pipeline using OpenSpec.

### Tasks

- Initialize `openspec/specs/` directory structure
- Write specs for core capture pipeline domains:
  - `auth-login` — authentication flow, session handling, credential management
  - `calendar` — event creation, recurring events, sharing, subscriptions, free/busy
  - `mail` — compose, read, reply/forward/delete, folder management, signatures, filters
  - `contacts` — add, edit/delete, import/export
  - `preferences` — settings, password change, vacation, global search
- Each spec includes: Purpose, Requirements (RFC 2119: SHALL/MUST/SHOULD), Scenarios (Given/When/Then)
- Configure `openspec/config.yaml` with project settings
- Run `openspec validate --all` to verify spec correctness

### Outcome

- Living specification of what the capture pipeline does
- Foundation for using delta specs in subsequent sprints
- Allowed tools: `openspec` CLI, editor

---

## Sprint 2: CI/CD Pipeline

**Goal:** Set up GitHub Actions for automated build, lint, test, and deploy.

### Tasks

- Create `.github/workflows/ci.yml` — run on push/PR to `main`
- **Lint:** ruff on `capture/` Python code
- **Type check:** mypy (if types exist) or pyright on Python files
- **Test:** pytest with coverage on `capture/tests/`
- **Build:** Docusaurus build for both `en` + `de` locales
- **Deploy:** GitHub Pages deployment on `main` push
- Add status badges to README

### Outcome

- Every push triggers automated checks
- Preview builds on PRs
- Deployed docs on merge

---

## Sprint 3: Asset Optimization

**Goal:** Reduce WebP and PNG asset sizes to under 150KB average.

### Tasks

- Create `capture/optimize.py` — batch image optimizer
- WebP optimization strategies:
  - Reduce color palette to 128 colors (from 256)
  - Reduce frame rate: every 2nd frame for similar consecutive frames
  - Crop to relevant viewport region
  - Strip metadata (EXIF, ICC profiles)
- PNG optimization strategies:
  - pngquant for 256-color indexed PNGs
  - Strip metadata
- Run optimizer on all 36 assets in `site/docs/assets/`
- Report size reduction per asset
- Verify visual quality is acceptable

### Outcome

- ≤150KB average asset size
- ≤300KB max per asset
- Lossy optimization measured vs acceptable quality threshold

---

## Sprint 4: Capture Reliability

**Goal:** Eliminate blank captures and add automatic retry logic.

### Tasks

- Investigate root cause of 8 blank WebP captures (password-change, mail-read, mail-reply-forward-delete, mail-folder-management, mail-signatures, preferences, vacation, mail-filters)
- Add `capture_retry(max_attempts=3)` decorator to `capture/run_captures.py`
- Add validation step: check image is not >90% white after capture → auto-retry
- Add structured logging to capture failures
- Create `capture/capture_report.py` — generates artifact quality report (file sizes, blank detection, frame counts)
- Re-capture all 8 blank WebPs with retry logic
- Write spec delta under `openspec/changes/capture-reliability/`

### Outcome

- Zero blank captures in pipeline
- Automatic retry on failure
- Quality report for every capture run

---

## Sprint 5: Parallel Execution

**Goal:** Run independent capture workflows in parallel to reduce total capture time.

### Tasks

- Analyze workflow dependency graph in `capture/run_captures.py` — identify independent workflows (calendar, mail, contacts are independent; login is a prerequisite)
- Implement `concurrent.futures.ThreadPoolExecutor` or `asyncio` for parallel workflow execution
- Add configurable `--workers=N` flag to `run_captures.py`
- Ensure sequential ordering where dependencies exist (login → all workflows)
- Measure and report speedup factor
- Write spec update under `openspec/changes/parallel-capture/`

### Outcome

- Capture time reduced by 3-5x (workflows → parallel groups)
- Deterministic ordering maintained for dependent steps

---

## Sprint 6: Accessibility Gates

**Goal:** Move `accessibility/validate.py` into CI as a blocking gate, auto-fix common issues.

### Tasks

- Integrate `accessibility/validate.py` as a CI step in `.github/workflows/ci.yml`
- Add auto-fix mode for fixable issues (heading hierarchy, table headers)
- Add WCAG 2.1 Level A checklist generation to each doc's frontmatter
- Add accessibility section template to docs that are missing it (keyboard navigation, screen reader workflow, high contrast)
- Fix all 98 currently detected violations across SOGo tutorial pages
- Write OpenSpec task delta under `openspec/changes/accessibility-gates/`

### Outcome

- Zero accessibility violations in docs
- CI blocks PRs with new violations
- Every doc has keyboard + screen reader section

---

## Sprint 7: Video/MP4 Pipeline

**Goal:** Add MP4 fallback for large animations with `<video>` tag support.

### Tasks

- Create `capture/webp_to_mp4.py` — convert WebP sequences to MP4 with ffmpeg
- Determine threshold: assets >300KB after optimization → generate MP4 fallback
- Create Docusaurus component: `<VideoFallback webp={...} mp4={...} />` that uses `<picture>` or `<video>` with WebP source + MP4 fallback
- Implement composable layout: `<video>` with play/pause controls for large animations, inline `<img>` for small ones
- Update doc templates to use the new component
- Measure size comparison (WebP vs MP4 per asset)
- Write spec delta under `openspec/changes/video-pipeline/`

### Outcome

- Large animations use efficient MP4 with play controls
- Small animations remain inline WebP
- ~50% size reduction for large assets

---

## Sprint 8: SOGo Change Detection

**Goal:** Automatically detect SOGo demo changes and trigger re-capture.

### Tasks

- Create `capture/detect_changes.py` — diff SOGo demo pages against cached baseline
- Baseline strategies:
  - Screenshot hash comparison (perceptual hashing with `ImageHash`)
  - DOM structure comparison (count elements, classes, text content)
  - Timestamp / version header check from SOGo response
- On detected change → trigger re-capture for affected workflow(s)
- Add `openspec/changes/sogo-change-detection/` with updated auth-login spec
- Generate report of what changed and what was re-captured

### Outcome

- Automated notification when SOGo UI changes
- Targeted re-capture of affected workflows only
- No stale documentation

---

## Sprint 9: Performance Benchmarks

**Goal:** Establish performance baselines and monitoring.

### Tasks

- Add Lighthouse CI to `.github/workflows/ci.yml` — measure:
  - Performance score
  - Accessibility score
  - Best practices score
  - SEO score
  - Largest Contentful Paint (LCP)
  - Cumulative Layout Shift (CLS)
- Add bundle size tracking (Docusaurus JS/CSS output)
- Add capture timing metrics to `capture_report.py` — per-workflow timing, retry counts
- Set up performance budgets (LCP <2.5s, total bundle <500KB gzip)
- Create performance dashboard page at `site/docs/performance.md`
- Write spec delta under `openspec/changes/performance-monitoring/`

### Outcome

- Performance regression detected on PR
- Historical performance data tracked
- Capture pipeline timing visible

---

## Sprint 10: Spec-to-Docs Pipeline

**Goal:** Auto-generate documentation pages from OpenSpec specs and capture metadata.

### Tasks

- Create `capture/spec_to_docs.py` — reads OpenSpec specs and generates:
  - Tutorial structure from spec scenarios (Given/When/Then → doc sections)
  - Asset embedding from capture metadata
  - Code blocks from spec requirements
- Integrate with Docusaurus `sidebars.js` generation
- Add `--from-spec` flag to `run_captures.py` that auto-generates docs alongside captures
- Document the pipeline in CONTRIBUTING.md
- Write spec delta under `openspec/changes/spec-to-docs/`

### Outcome

- New features get documentation automatically when specs + captures exist
- Reduced manual doc writing effort
- Living docs that stay in sync with spec changes

---

## Legend

| Icon | Meaning |
|------|---------|
| ✅ | Completed |
| 🔵 | In Progress |
| 🟡 | Planned |
| ❌ | Blocked |

---

## Completed Work ✅

- ✅ 27 documentation pages created
- ✅ 22 WebP animations generated (14 valid captures, 8 blank — replaced with PNGs or removed)
- ✅ 14 PNG screenshots integrated (11 valid, 3 blank)
- ✅ 20 orphan assets deleted (GIFs, PNGs, images)
- ✅ 8 orphan blank WebP assets deleted
- ✅ Sidebars reorganized into 7 English categories: Getting Started, Basics, Calendar, Mail, Contacts, Tools, Advanced
- ✅ Frame validation added to detect blank screenshots
- ✅ Docusaurus versioning configured for SOGo 5 + SOGo 6 with version dropdown
- ✅ Project deployed to GitHub Pages (`/docmakerai/`) with `/5/` and `/6/` routes
- ✅ Build verified for both English and German locales
- ✅ 15 gap closure rounds completed (all known SOGo 5 gaps addressed)
- ✅ 8 blank captures identified and replaced with PNG screenshots or text descriptions

---

**Last Updated:** 2025-06-20
**Next Sprint:** Sprint 1 — Spec Foundation (OpenSpec)
