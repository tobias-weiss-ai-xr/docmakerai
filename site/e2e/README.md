# E2E Tests for docmakerai site

End-to-end tests using [Playwright](https://playwright.dev/) to verify the deployed docmakerai site (SOGo User Guide).

## Running tests

### Against the live deploy (gh-pages)
```bash
npm run test:e2e
```
By default, tests run against `https://tobias-weiss-ai-xr.github.io/docmakerai/`.

### Against a local dev server

1. Start the Docusaurus dev server:
```bash
npm run start
```

2. In a second terminal, run tests with the local URL:
```bash
PLAYWRIGHT_BASE_URL=http://localhost:3000 npm run test:e2e
```

### Headed mode (for local debugging)
```bash
npm run test:e2e:headed
```

### UI mode (interactive test runner)
```bash
npm run test:e2e:ui
```

## Test suites

| File | Purpose |
|------|---------|
| `homepage.spec.ts` | Root redirect, landing page, locale switching |
| `docs.spec.ts` | Doc content presence, regression for DocItem Layout bug |
| `navbar.spec.ts` | Logo sizing (regression for global img rule), nav links |
| `sidebars.spec.ts` | Sidebar categories, navigation, TOC |
| `custom.spec.ts` | Custom components (SEO, DocVoteWidget) |

## CI

Tests run automatically on push to `main` (for changes in `site/` or the workflow file).

## Adding new tests

- Place `.spec.ts` files in the `e2e/` directory
- Use `test.describe()` to group related tests
- Follow the existing patterns for selectors and assertions
- Keep tests independent and fast (test live site, no setup needed)

## Debugging

- If a test fails, Playwright creates trace files in `traces/`
- View traces: `npx playwright show-report`
- Increase timeout: `test.setTimeout(10000)` for slow tests
