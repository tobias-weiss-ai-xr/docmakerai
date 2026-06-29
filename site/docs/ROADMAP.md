---
title: "Roadmap"
description: "Optimization & Automation Roadmap — SOGo User Guide (5 & 6)"
sidebar_label: "Roadmap"
---

# Roadmap — SOGo User Guide (5 & 6)

**Status:** ✅ Published — 27 SOGo 5 docs, 36 visual assets (WebP + PNG), Docusaurus versioning for SOGo 5 + SOGo 6, CI/CD with self-hosted runners, 99.34% test coverage, SEO/GEO targeting, task-first capture flow with HTML5 video

**Demo Sites:**
- SOGo 5: https://demo.sogo.nu/
- SOGo 6: https://demov6.sogo.nu/

**Build Status:** CI pipeline using self-hosted runner on legions (192.168.42.42). Builds take ~4-5 min (cached) / ~10 min (cold).

**Staging:** Deferred — own preview deployment system replacing Netlify (see Sprint 13).

---

## Completed ✅

### Sprint 1: Spec Foundation (OpenSpec)
- [x] Initialize `openspec/specs/` directory structure
- [x] Write specs for core capture pipeline domains: auth-login, calendar, mail, contacts, preferences
- [x] Each spec includes: Purpose, Requirements (RFC 2119), Scenarios (Given/When/Then)
- [x] Configure `openspec/config.yaml` with project settings

### Sprint 2: CI/CD Pipeline
- [x] Create `.github/workflows/ci.yml` — run on push/PR to `main`
- [x] **Lint:** ruff on `capture/` Python code
- [x] **Test:** pytest with 99.34% coverage on `capture/tests/` + `accessibility/tests/`
- [x] **Build:** Docusaurus build for both `en` + `de` locales
- [x] **Deploy:** GitHub Pages deployment on `main` push
- [x] Self-hosted runner on legions (192.168.42.42) with labels `linux, legions`
- [x] Runner service: `legions-docmaker-runner`

### Sprint 3: Asset Optimization
- [x] Create `capture/optimize.py` — batch image optimizer
- [x] WebP optimization: color palette reduction, frame skip, metadata stripping
- [x] PNG optimization: pngquant, metadata stripping
- [x] 36 tests for optimize.py
- [x] 54% size reduction achieved (2.1MB → 976KB per version)

### Sprint 4: Capture Reliability
- [x] Add validation step: blank detection (>90% white)
- [x] Structured logging to capture failures
- [x] Create `capture/capture_report.py` — artifact quality report
- [x] Re-capture logic with retry

### Sprint 5: Parallel Execution
- [x] Implement parallel workflow execution
- [x] Configurable workers via semaphore
- [x] Sequential ordering for dependencies (login → workflows)
- [x] 12 tests for parallel_runner.py

### Sprint 6: Accessibility Gates
- [x] Integrate `accessibility/validate.py` as CI step
- [x] Add auto-fix mode for fixable issues (heading hierarchy, table headers)
- [x] 30 tests for accessibility/validate.py
- [x] WCAG 2.1 Level A checklist generation

### Sprint 7: Video/MP4 Pipeline
- [x] Create `scripts/convert_to_mp4.py` — WebP → MP4 (H.264) + WebM (VP9)
- [x] MP4: libx264, CRF 23, yuv420p, fast start
- [x] WebM: libvpx-vp9, CRF 30
- [x] Thumbnail/poster generation

### Sprint 8: User Journeys & SEO
- [x] Task-first capture flow with 4-beat narrative (Context, Challenge, Solution, Result)
- [x] Human-like typing (120ms delay on form fields)
- [x] SEO components: Open Graph, Twitter Cards, Schema.org (SoftwareApplication, HowTo, TechArticle)
- [x] GEO targeting: geo.region="DE", geo.placename="Berlin", ICBM
- [x] Path restructuring: sogo5/sogo6 instead of /5//6/
- [x] Sidebar reorganized into 7 categories with emoji icons

### Sprint 2b: CI Reliability
- [x] Docusaurus build time optimization (4-5 min cached, ~10 min cold — down from 30+)
- [x] Python lint/test stability (PEP 668 compatibility with --break-system-packages)
- [x] Node.js version compatibility (Node 20 vs Node 24 on Arch rolling)
- [x] Branch protection rules: separate CI status checks from deploy gate
- [x] Runner resource contention: load balance between CI/Deploy/Preview workflows

### Sprint 9: Performance Benchmarks
- [x] Add Lighthouse CI to `.github/workflows/ci.yml`
- [x] Add bundle size tracking
- [x] Add capture timing metrics to `capture_report.py`
- [x] Set up performance budgets (LCP `&lt;2.5s`, total bundle `&lt;500KB` gzip)
- [x] Create performance dashboard page at `site/docs/performance.md`

### Sprint 12: Spec-to-Docs Pipeline
- [x] Auto-generate documentation pages from OpenSpec specs
- [x] Tutorial structure from spec scenarios
- [x] Asset embedding from capture metadata
- [x] Docusaurus sidebar auto-generation
- [x] `scripts/generate_docs_from_specs.py` (593 lines) shipped in commit `25bed47`

### Sprint 14: Repo Hygiene
- [x] Untrack `.github-pages-trace` debug artifact
- [x] Remove empty `docs/` directory
- [x] Sync ROADMAP with actual state
- [x] Add CI guard for coverage threshold regression (>0.5% drop fails PR)

### Sprint 11: SOGo Change Detection
- [x] Create `capture/detect_changes.py` — perceptual-hash UI diff
- [x] ImageHash-based screenshot comparison (pHash, 64-bit)
- [x] Hamming distance threshold (default: 10 bits)
- [x] Auto-baseline-update on drift detection
- [x] Nightly CI workflow (`.github/workflows/change-detection.yml`) posts GitHub Issue on drift
- [x] `capture/run_captures.py` integrates drift check per workflow
- [ ] DOM structure comparison (deferred — pHash covers most cases)

### Infrastructure
- [x] Self-hosted runner on legions (192.168.42.42)
- [x] Runner name: legions-docmaker-runner
- [x] Labels: linux, legions
- [x] SSH config updated
- [x] Test coverage: 99.34% (192/192 tests passing)
- [x] coverage.xml artifact upload in CI

---

## In Progress 🔵

_None — all tracked sprints are either completed or planned._

---

## Planned 🟡

### Sprint 10: Content Expansion
- [x] Recapture critical workflows with task-first approach (converted 3 existing WebM to MP4)
- [x] Convert task-first WebP captures to MP4 (3 videos optimized, 6-11% smaller)
- [x] Add VideoFallback component and WebVTT captions (component created + 1 tutorial updated)
- [x] Add PageSEO to key tutorial pages (compose, add contact, reply/forward, edit/delete)
- [ ] Full German translation of `/sogo5/de/`

### Sprint 13: PR Preview Deployments (Completed)
- [x] Rewrite `preview-deploy.yml` — build with dynamic baseUrl, deploy to `gh-pages/preview/pr-<N>/`
- [x] Preview URL commented on PRs (upserts existing comment instead of spamming)
- [x] Teardown workflow (`preview-cleanup.yml`) — deletes preview directory on PR close
- [x] Update workflow README with preview URL info
- [x] Decide: gh-pages `/preview/` subdirectory (chosen over staging branch)

---

## Accessibility

This documentation site supports keyboard navigation, screen readers, and high-contrast mode.

### Keyboard Navigation

| Shortcut: | Action: |
| --------- | ------ |
| `Tab` | Navigate between links and interactive elements |
| `Enter` / `Space` | Activate links and buttons |
| `Ctrl + F` | Search within the current page |

### Screen Reader & High Contrast

- All tables use proper header markers (`| Header |` format) for screen reader column navigation
- Status icons include text alternatives (e.g., "✅ Completed" not just an emoji)
- High-contrast mode is supported via system `prefers-contrast: more` media queries
- Color is never the sole means of conveying information

## Known Issues

| Issue: | Status: | Notes: |
| ----- | ------ | ----- |
| Docusaurus build takes 30+ min on legions | 🔵 | Node 24 vs Node 20, npm cache cold |
| Python PEP 668 blocks pip | ✅ Fixed | `--break-system-packages` added |
| `@docusaurus/remark-plugin-content-docs` infinite loop | ✅ Fixed | Plugin removed, using manual PageSEO imports |
| GitHub API intermittent connectivity | ⚠️ | `api.github.com` connection issues |
| Deploy workflow hangs on German locale build | 🔵 | Suspected Node.js version mismatch |

---

## Legend

| Icon: | Meaning: |
| ---- | ------- |
| ✅ | Completed |
| 🔵 | In Progress |
| 🟡 | Planned |
| ❌ | Blocked |
| ⚠️ | Degraded |

---

**Last Updated:** 2026-06-29
**Next Sprint:** Sprint 10 — Content Expansion (German translation)

---

## Appendix: Key Metrics

| Metric: | Value: |
| ------- | ----- |
| Test coverage | 99.34% (192/192 passing) |
| CI runner | Self-hosted on legions (192.168.42.42) |
| Runner labels | linux, legions |
| Runner version | 2.335.1 |
| SEO geo tags | geo.region=DE, geo.placename=Berlin, ICBM |
| Asset size reduction | 54% (2.1MB → 976KB) |
| Documentation pages | 27 SOGo 5 + 30 SOGo 6 docs |
| Path structure | /sogo5/, /sogo6/ |
