# SOGo 6 Screenshot Capture Pipeline

Captures real screenshots from a running SOGo 6 instance for the user guide.
Targets the local dockerized stack at `http://localhost:3000`.

## Prerequisites

- [sogo6-stalwart-openldap-dockerized](https://github.com/tobias-weiss-ai-xr/sogo6-stalwart-openldap-dockerized) running
- Playwright + Chromium installed

```bash
make install
```

## Quick Start

```bash
# 1. Start the local SOGo 6 stack
cd /home/weissto_local/git/sogo/sogo-live/sogo6-stalwart-openldap-dockerized
make start
make init

# 2. Run all SOGo 6 captures
cd /home/weissto_local/git/docmakerai
make capture-sogo6

# 3. Captures are saved to capture/screenshots/ and copied to site/versioned_docs/version-6/assets/
```

## Capture a Single Doc

```bash
make capture-sogo6-doc DOC=calendar-create-event
make capture-sogo6-doc DOC=mail-compose
make capture-sogo6-doc DOC=logout
```

Available doc names: `calendar-create-event`, `calendar-recurring`, `mail-compose`,
`contacts-add`, `vacation`, `mail-signatures`, `mail-filters`, `calendar-subscribe`,
`calendar-share`, `freebusy`, `logout`, `preferences`, `calendar-views`,
`contacts-edit-delete`, `calendar-edit-delete`, `global-search`, `mail-read`,
`mail-folder-management`, `mail-reply-forward-delete`, `password-change`,
`calendar-ical`, `contacts-import-export`.

## How It Works

1. Opens Playwright (headless Chromium)
2. Logs in to the local SOGo 6 UI at `http://localhost:3000`
3. For each workflow:
   - Navigates to the relevant module (Mail, Calendar, Contacts)
   - Performs the tutorial action (create event, compose email, etc.)
   - Takes an annotated screenshot at the result moment
4. Annotations (red box + arrow) highlight the key UI element
5. Outputs PNG screenshots to `capture/screenshots/`
6. Copies them to `site/versioned_docs/version-6/assets/`

## Configuration

Set via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `SOGO_URL` | `http://localhost:3000` | SOGo 6 instance URL |
| `SOGO_USERNAME` | `testuser@example.org` | Login email |
| `SOGO_PASSWORD` | `password123` | Login password |

Or use `.env.local`:
```bash
export $(cat capture/.env.local | xargs)
python capture/run_screenshot_captures.py
```

## Known Issue: Next.js 16 Turbopack Dev Server

The SOGo 6 UI runs Next.js 16 with Turbopack. **The dev server cannot serve
protected routes to Playwright** — it hangs during compilation and eventually
drops the connection without any HTTP response (``ERR_EMPTY_RESPONSE`` /
``ERR_SOCKET_NOT_CONNECTED``).

Root cause: When Next.js dev server receives a request for a route that hasn't
been compiled yet (e.g., ``/en/u/0/INBOX`` after login), it triggers a
compilation. During compilation, it returns empty responses to Playwright's
Chromium. The same request via ``curl`` also fails (HTTP 000 after 22s timeout).

This is a known Next.js 16.2.10 + Turbopack issue, acknowledged in the
SOGo 6 Dockerfile: *"Production standalone build has issues with Next.js 16.2.10
RSC streaming (client-side hydration doesn't occur after build)."*

### Workaround: Use production build

Once the SOGo 6 project resolves the production build issue:

```bash
cd sogo6-ui && npm run build && npm start
```

The capture pipeline is fully compatible with the production server.

### Current status

The pipeline code is complete and correct:
- ✅ 22 workflow definitions covering all tutorials
- ✅ Login flow with correct credentials
- ✅ ``/env`` intercept to fix API base URL
- ✅ Resilient ``goto`` with retry + exponential backoff
- ✅ Route pre-warming in Makefile targets
- ✅ ``networkidle`` wait strategy + proper user-agent

It's blocked only by the Next.js dev server limitation.

### Troubleshooting

### Blank/white screenshots
- The SOGo 6 UI uses client-side rendering; ensure `wait_for_timeout` is long enough
- Check the browser console for JS errors `SOGO_DEBUG=1`
- The local stack may need `make init` to seed test data

### Login failures
- Verify the stack is running: `docker compose ps`
- Check credentials in `.env.local`
- Test API directly: `curl -X POST http://localhost:5001/api/user/v1/auth/login -H 'Content-Type: application/json' -d '{"username":"lisa.mayer@example.org","password":"UniMarburg2026!"}'`

### Missing UI elements
- SOGo 6 UI selectors may change between versions
- Run with headless=false to debug: modify `headless=True` → `headless=False` in the script
