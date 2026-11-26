# docmakerai — Documentation site

Docusaurus site for the SOGo user guide (multi-version: SOGo 5 + SOGo 6) and
the openEduSuite section. Built by [DocMaker AI](../../README.md).

## Prerequisites

- Node.js >= 20 and npm
- Playwright browsers for the e2e tests (`npx playwright install`)

## Local Development

```bash
npm install
npm run start        # dev server, http://localhost:3000 (base path /docmakerai/)
```

Most changes are reflected live without restarting the server.

## Build

```bash
npm run build        # dual-locale (en + de) production build into build/
npm run serve        # serve the built site locally
```

The npm `postbuild` hook regenerates `build/sitemap.xml` with en/de
hreflang alternates (`tools/generate_sitemap.py`).

## Code Quality

```bash
npm run typecheck    # tsc --noEmit
npm test             # (none wired; python tooling lives at ../scripts, ../accessibility)
npm run test:e2e     # Playwright suite — runs against the live deploy by default;
                     # use PLAYWRIGHT_BASE_URL=http://localhost:3000 for local runs
```

Docs/table/content regressions are guarded by pytest in the repo root:

```bash
cd .. && python3 -m pytest scripts/tests/ accessibility/tests/ -q
```

## Structure

| Path | What it is |
|------|------------|
| `docs/` | Current (unversioned) SOGo tutorials — EN source of truth |
| `versioned_docs/version-5/`, `version-6/` | Deployed tutorial versions |
| `i18n/de/` | German mirrors (docs + suite), localized by content folder |
| `suite-docs/` | openEduSuite app guides (EN) |
| `src/pages/`, `src/components/LandingPage.tsx` | Root landing page (en/de) |
| `e2e/` | Playwright end-to-end tests |
| `tools/`, `plugins/` | Build tooling |

## Search

The site ships offline local search (`@easyops-cn/docusaurus-search-local`) at
`/search/` (and `/de/search/`), reachable from the navbar and via `Ctrl+K` /
`Cmd+K`. It indexes the tutorials, versioned docs, suite pages and the landing
page without a backend.

## Accessibility

The site ships an accessibility-validation gate (`../accessibility/validate.py`)
and the guides follow the writing guidelines in `../AGENTS.md` (screen-reader
workflows, keyboard navigation, high-contrast notes). All pages support
keyboard navigation and browser/OS-level high-contrast and dark mode.

## Deploy

GitHub Pages via `.github/workflows/deploy.yml` on `main`; PR previews are
built under `/preview/pr-<N>/`.
