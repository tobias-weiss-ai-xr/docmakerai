# openEduSuite Documentation Program Plan

> **For agentic workers:** This is a PROGRAM plan covering multiple independent
> subsystems (one per product family). Do NOT implement it as one plan — break
> it into per-wave implementation plans (see "Wave plans") using the
> writing-plans skill, then execute each via subagent-driven-development or
> executing-plans.

**Goal:** Extend docmakerai from a SOGo-only docs site into the complete
end-user documentation platform for the whole openEduSuite (openedusuite.org),
under the established truthful-docs doctrine (live-verified captures, EN+DE,
accessibility sections, regression-tested claims).

**Architecture:** Docusaurus multi-section site — the existing versioned SOGo
docs stay untouched; a second docs-plugin instance ("suite") hosts per-product
categories. The capture pipeline generalizes from `SOGO_*` env to per-product
login profiles; since the suite is Keycloak-SSO-federated, one capture login
unlocks every app.

**Tech Stack:** Docusaurus 3 (existing site), Playwright capture pipeline
(existing `capture/`), pytest quality suite (existing `scripts/tests/`),
provenance manifest + clips conventions (existing).

---

## 0. Decision Gates (blocking — need user answers before Wave 1 starts)

| # | Question | Recommendation |
|---|----------|----------------|
| G1 | **Audience:** end users only, or also staff/admin? | End users (students/staff as users). Admin/ops docs stay in openEduSuite-hrz `docs/` — link out, don't duplicate. |
| G2 | **Component scope:** which apps are *user-facing in production* on openedusuite.org? E.g. is grommunio an evaluation parallel to SOGo? ILIAS vs Moodle — both? BookStack and XWiki share `wiki.` host — what's the split? | Take the portal entries (LDIF, `odApplicationOrder`) as the source of truth: what appears in the portal gets documented. |
| G3 | **Capture target:** production portal.openedusuite.org (read-only flows, real accounts?) or the eval cluster / a dedicated docs-tenant? | Dedicated test tenant on the eval cluster if available; production only for flows that are safe read-only (portal, file listing). SOGo precedent: public demo, disposable accounts. |
| G4 | **Docs URL/home:** stay under graphwiz GH Pages (`/docmakerai/`) or move to docs.openedusuite.org later? | Stay now (no infra work), design URLs so a future domain move is config-only (`baseUrl` + asset prefix). |
| G5 | **Languages:** EN+DE from day one (as SOGo)? | Yes — existing i18n pipeline and DE-own-assets policy apply unchanged. |
| G6 | **Versioning:** per-product versions like SOGo v5/v6? | No versioning for wave 1+2 products (single current). SOGo keeps its versioned instance. Revisit when a product does a breaking major. |

## 1. Component Inventory (from portal-entries LDIF + helmfile/apps/edu)

Wave assignment by user impact (portal order = visibility):

**Wave 1 — Core journey (every user, day one)**
| App | Host | Why first |
|-----|------|-----------|
| Portal | portal.openedusuite.org | Entry point; app overview doc |
| Login/SSO (Keycloak) | id.openedusuite.org | Everyone logs in; session behavior |
| Passwort ändern (SSP) | ssp.openedusuite.org | Password self-service; pairs with SSO |
| Meine Dateien (OpenCloud) | files.openedusuite.org | Files: upload/share/share-links — high value |
| Helpdesk (Zammad) | helpdesk.openedusuite.org | Ticket creation — users need it when stuck |
| SOGo Mail ✓ | mail.openedusuite.org | DONE (28 pages, 19 workflows) — cross-link only |

**Wave 2 — Collaboration**
Wiki & Projekte (XWiki + OpenProject, projects./wiki.), Etherpad, Planka,
draw.io, Excalidraw, BookStack (split vs XWiki per G2).

**Wave 3 — Teaching & learning**
LMS (Moodle and/or ILIAS per G2), BigBlueButton, JupyterHub, RStudio,
Overleaf, Slidev/Typst (if user-facing).

**Wave 4 — Specialist & staff**
LimeSurvey, Paperless-ngx, Mayan EDMS, Open WebUI/LLM services, n8n (staff),
eudi-issuer, Discourse/Indico (seeds exist — confirm prod status per G2).

**Explicit non-goals:** infra/ops/admin documentation (stays in
openEduSuite-hrz), internal services (seaweedfs, mariadb, kasmvnc/ttyd/
code-server unless users see them), evaluations not in the portal.

## 2. Site Architecture (Task basis for the wave-0 implementation plan)

**Files (create/modify):**
- Modify `site/docusaurus.config.ts` — register second docs instance
  `id: 'suite'`, `routeBasePath: 'suite'`, own sidebar path; keep SOGo
  instance as-is at `/`.
- Create `site/suite-docs/` — new instance root with `_category_.json`
  per product (`files/`, `portal/`, `helpdesk/`, `projects/`, `wiki/`, …).
- Create `site/suite-sidebars.ts` (or extend `sidebars.ts`).
- Modify `site/i18n/de/docusaurus-plugin-content-docs/` — add `suite/`
  subtree for DE (same structure; DE-own-assets policy applies).
- Create `site/src/pages/index.ux`-level landing? No — SOGo docs root stays
  the home; add a prominent "openEduSuite" section link in the navbar.

**URL shape:** `/suite/files/share-folder`, `/suite/portal/overview`, …
Future domain move = `baseUrl` change only (G4).

**Verification:** build produces both instances (sitemap grows), existing
127 URLs keep their paths (no SOGo regression), i18n locale switch works
for both instances.

## 3. Capture Infrastructure Generalization

**Files:**
- Modify `capture/run_screenshot_captures.py` — introduce per-product login
  profiles: `LOGIN_PROFILES = {"sogo": {...}, "suite": {"kind": "keycloak-sso",
  "username_env": "SUITE_USERNAME", "start_url": "<G3 host>"}}`. Suite login
  is Keycloak SSO — one `suite_login(page)` helper, then `goto(app_url)`.
- All existing doctrine transfers unchanged: hard-fail scoped captures,
  phash dedup, scene-scoping, `--only` scratch safety, webm→mp4 clips,
  provenance manifest entries, `preload="none"` embeds.

**Probe-first rule (from the SOGo rounds):** every page set starts with a
UI-dump probe of the real app; no page ships claims the probe didn't verify.
Unknown/unreachable UI → hedge honestly (delegation-page precedent).

## 4. Per-Wave Process (each wave = own implementation plan via writing-plans)

1. **Inventory probe** — Playwright dump of the app's real UI (labels,
   buttons, views); record ground-truth memory entry.
2. **Page set definition** — 3–8 tutorial pages per app (SOGo scale was 28
   pages for 6 modules; apps here are smaller).
3. **Content + captures** — EN first, DE mirror, per-page accessibility
   sections (repo policy, AGENTS.md rules), stills + clips + provenance.
4. **Tests** — extend `scripts/tests/test_docs_quality.py` doc-dir list with
   `suite-docs` EN+DE; forbidden-keyboard patterns apply automatically;
   clip-embed↔disk check applies automatically.
5. **Build + crawl** — 127-URL baseline grows; full resource crawl stays at
   0 failed requests.
6. **Commit + push** — one commit per wave per product family.

## 5. Quality Gates (carried over verbatim from the SOGo program)

- Truthful-docs: no invented UI, no unverified matrices, no admin-config
  leaks into user docs (`sogo-ealarms-notify` precedent).
- Every fixed fabrication → regression test (keyboard purge precedent:
  tests caught 10 stragglers the manual pass missed).
- Accessibility section on every tutorial page (test-enforced).
- DE assets owned by DE tree; provenance manifest current (test-enforced).
- Build green with zero warnings; sitemap + resource crawl verified.

## 6. Wave Plans (to be written with writing-plans when each wave starts)

- [ ] Wave 0: site architecture + capture profiles (G1–G6 answered)
- [ ] Wave 1: portal, sso+ssp, files, helpdesk (+ SOGo cross-links)
- [ ] Wave 2: wiki/projects, etherpad, planka, drawio, excalidraw, bookstack
- [ ] Wave 3: LMS, BBB, jupyter, rstudio, overleaf
- [ ] Wave 4: specialist/staff apps (confirm prod status first)

## Self-Review

- Coverage: audience/scope/instances (G1–G3), architecture, infra reuse,
  process, gates, wave breakdown — all addressed; detailed TDD task
  breakdowns deliberately deferred to per-wave plans (scope check).
- No placeholders: every section names files, commands, or decisions.
- Gaps by design: component list needs G2 confirmation; capture hosts need
  G3 credentials/tenant decision.
