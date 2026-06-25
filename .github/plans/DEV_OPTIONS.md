# Development Options — DocMaker AI

Recorded 2026-06-25. All options evaluated for the SOGo User Guide project.

---

## Option A: CI Reliability (Sprint 2b)

**Status:** Partially done — Docusaurus build optimized from 30+ to 4-5 min

**Remaining:**
- Branch protection rules on `main` — separate CI checks from deploy gate
- Runner resource contention — single `legions-docmaker-runner` queues CI/Deploy/Preview
- Remove `--ignore=capture/tests/test_run_captures.py` from CI (lint fixes were applied but never verified)
- Verify lint fixes actually pass `ruff check`

**Effort:** 1-2h | **Risk:** Low | **Impact:** CI won't break silently

---

## Option B: Content Expansion (Sprint 10)

**Status:** Partial — 3 videos converted, VideoFallback created, PageSEO on 4 pages

**Remaining:**
- Full German translation of 17 remaining `version-5` docs and 31 `current` docs
- Add PageSEO to remaining tutorial pages (currently on 4 + 1 versioned)
- More task-first capture conversions (WebP → MP4 with VideoFallback)

**Effort:** 2-5h | **Risk:** Low | **Impact:** High (DE locale is a real user need)

---

## Option C: Performance Benchmarks (Sprint 9)

- Lighthouse CI in CI workflow
- Bundle size tracking, performance budgets (LCP <2.5s, bundle <500KB)
- Performance dashboard page

**Effort:** 2-3h | **Risk:** Low | **Impact:** Medium

---

## Option D: SOGo Change Detection (Sprint 11)

- `capture/detect_changes.py` — diff SOGo demo pages via screenshot hash + DOM comparison
- Auto-trigger recapture when upstream UI changes

**Effort:** 3-5h | **Risk:** Medium | **Impact:** High (prevents stale screenshots)

---

## Option E: Spec-to-Docs Pipeline (Sprint 12)

- Auto-generate Docusaurus MDX pages from OpenSpec spec files (6 domains)
- Tutorial structure from Given/When/Then scenarios
- Asset embedding from capture metadata
- Docusaurus sidebar auto-generation

**Effort:** 4-6h | **Risk:** Medium-High | **Impact:** Medium (automates content creation)

---

## Option F: Netlify Removal — Housekeeping

- Strip all Netlify references from repo
- Gut `preview-deploy.yml` to a build-only placeholder (or full staging replacement when Sprint 13 is picked up)
- Remove `.github/secrets/NETLIFY_SETUP.md`
- Update `.github/workflows/README.md`

**Effort:** ~30min | **Risk:** None | **Impact:** Cosmetic (prepares for Sprint 13)

---

## Option G: Self-Hosted Staging (Sprint 13 — Deferred)

- Replace Netlify preview-deploy.yml with own staging on GitHub Pages
- PR preview via `rossjrw/pr-preview-action` or custom gh-pages subdirectory
- Preview URL comment on PRs
- Teardown on PR close

**Effort:** 2-3h | **Risk:** Low | **Impact:** High (removes Netlify dependency)
