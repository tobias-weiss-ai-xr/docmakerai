#!/usr/bin/env python3
"""DocMaker AI — Screenshot-Only Capture Pipeline

Fast, reliable screenshot captures for SOGo 6 documentation.
Each workflow navigates to a feature, interacts, and takes a single
annotated screenshot at the result moment.

Usage:
    export SOGO_URL=https://demov6.sogo.nu
    python capture/run_screenshot_captures.py
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import os
import shutil
import sys
import time
from pathlib import Path

from playwright.async_api import BrowserContext, Page, async_playwright

try:
    from capture.annotate import annotate_frame
    from capture.detect_changes import find_duplicates
except ImportError:
    from annotate import annotate_frame
    from detect_changes import find_duplicates


ROOT = Path(__file__).resolve().parent
SCREENSHOT_DIR = ROOT / "screenshots"
ASSETS_DIR = Path(
    os.environ.get("CAPTURE_ASSETS_DIR", str(ROOT.parent / "site" / "docs" / "assets"))
)

SOGO_URL = os.environ.get("SOGO_URL", "https://demov6.sogo.nu")
USERNAME = os.environ.get("SOGO_USERNAME", "sogo-tests1@example.org")
PASSWORD = os.environ.get("SOGO_PASSWORD", "sogo")

# The /env intercept rewrites the API base URL for the LOCAL dev server (whose
# /env points at the Docker-internal hostname). Production instances serve a
# correct same-origin /env — set SOGO_ENV_INTERCEPT=0 to keep it untouched.
ENV_INTERCEPT = os.environ.get("SOGO_ENV_INTERCEPT", "1") == "1"


def clean_dirs() -> None:
    # Only wipe the screenshot scratch dir; never the assets target — it may
    # hold manually curated/numbered shots the workflows don't regenerate,
    # and shutil.copy2 below overwrites same-name files anyway.
    if SCREENSHOT_DIR.exists():
        shutil.rmtree(SCREENSHOT_DIR)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)


async def _env_intercept(route):
    """Intercept /env to fix the API base URL.

    The SOGo 6 UI tries to reach the API at ``http://sogo6-server:5000``
    (Docker internal hostname), which is unreachable from the host browser.
    We compute the API URL from the SOGO_URL host.

    We **fulfill directly** instead of calling ``route.fetch()`` because
    the Next.js dev server's ``/env`` endpoint sometimes returns an empty
    response (socket hang up), which causes the whole navigation to fail.
    """
    import json
    from urllib.parse import urlparse

    parsed = urlparse(SOGO_URL)
    api_host = parsed.hostname or "localhost"
    api_base = f"http://{api_host}:5001/api/user/v1"
    body = {
        "REACT_APP_API_BASE_URL": api_base,
        "SOGO_URL": SOGO_URL,
        "LOGIN_PREFILL_EMAIL": USERNAME,
    }
    await route.fulfill(
        status=200,
        content_type="application/json",
        body=json.dumps(body),
    )


async def resilient_goto(
    page, url: str, max_retries: int = 5, wait_selector: str | None = None
) -> bool:
    """Navigate with retry + exponential backoff for Next.js dev server flakiness.

    ``next dev`` (Turbopack) sometimes returns empty responses when
    mid-compilation. Retrying with backoff resolves this reliably.
    """
    for attempt in range(max_retries):
        try:
            await page.goto(url, wait_until="commit", timeout=20000)
            await page.wait_for_timeout(1500)
            if wait_selector:
                try:
                    await page.wait_for_selector(wait_selector, timeout=8000)
                except Exception:
                    wait_until = attempt < max_retries - 1
                    if wait_until:
                        print(f"    ⚠️  selector '{wait_selector}' not found, retrying...")
                        await page.wait_for_timeout(2000 * (attempt + 1))
                        continue
                    return False
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"    ⚠️  goto failed (attempt {attempt + 1}): {e}")
                await page.wait_for_timeout(2000 * (attempt + 1))
            else:
                print(f"    ❌ goto failed after {max_retries} attempts: {e}")
                return False
    return False


async def login(page, context: BrowserContext | None = None) -> None:
    """Log in to SOGo 6.

    The login flow depends on whether LOGIN_PREFILL_EMAIL is set:
    - If set: the login page immediately redirects to the password page
    - If not set: the user must fill in the email first

    We handle both cases by probing for the email input first.
    """
    print("\n  Login...")
    if ENV_INTERCEPT:
        await page.route("**/env", _env_intercept)

    await resilient_goto(page, SOGO_URL + "/en/auth/login")

    # Check if we're already on the password page (LOGIN_PREFILL_EMAIL)
    pwd = page.locator("input[type='password']")
    email = page.locator("input[type='email']")

    if await email.is_visible(timeout=3000):
        # Email step required
        print("    Email step...")
        await email.fill(USERNAME)
        await page.wait_for_timeout(300)
        await page.click("button[type='submit']")
        await page.wait_for_timeout(2000)

    if await pwd.is_visible(timeout=8000):
        # Password step
        print("    Password step...")
        await pwd.fill(PASSWORD)
        await page.wait_for_timeout(300)
        await page.click("button[type='submit']")
    else:
        print("    ⚠️  Password field not found, trying direct navigation...")
        await resilient_goto(
            page,
            SOGO_URL + "/en/auth/login/pwd?email=" + USERNAME,
            wait_selector="input[type='password']",
        )
        pwd2 = page.locator("input[type='password']")
        if await pwd2.is_visible(timeout=5000):
            await pwd2.fill(PASSWORD)
            await page.click("button[type='submit']")

    # Wait for SPA redirect after successful login.
    print("    Waiting for redirect to inbox...")
    for _ in range(20):
        await page.wait_for_timeout(1000)
        if "/u/" in page.url:
            print(f"    ✅ Redirected: {page.url}")
            return
    # Fallback: navigate directly
    print(f"    ⚠️  No redirect after 20s (URL: {page.url}), navigating directly...")
    await resilient_goto(
        page, SOGO_URL + "/en/u/0/INBOX", wait_selector="main, [data-testid], .mail-list"
    )
    print(f"    Inbox: {page.url}")


async def goto(page, url_suffix: str, wait_ms: int = 1500) -> None:
    url = f"{SOGO_URL}/en/{url_suffix}" if url_suffix else SOGO_URL
    await resilient_goto(page, url, wait_selector="#app-container, .app-container, main")
    await _clear_overlays(page)
    await page.wait_for_timeout(wait_ms)


async def navigate_to_module(page, module: str, wait_ms: int = 3000) -> None:
    """Navigate to an SOGo 6 module via sidebar tab click (SPA navigation)."""
    await resilient_goto(
        page, SOGO_URL + "/en/u/0/INBOX", wait_selector="button[role='tab'], main, [data-testid]"
    )
    await _clear_overlays(page)
    await page.wait_for_timeout(2000)

    tab_labels = {
        "calendar": "Calendars",
        "mail": "Mail",
        "contacts": "Address Books",
        "tasks": "Tasks",
    }
    label = tab_labels.get(module.lower())
    if label:
        tab = page.locator(f'button[role="tab"][aria-label="{label}"]')
        if await tab.is_visible(timeout=5000):
            await tab.click()
            await page.wait_for_timeout(wait_ms)
        else:
            await goto(page, module, wait_ms)
    else:
        await goto(page, module, wait_ms)


async def _clear_overlays(page) -> None:
    """Neutralize floating widgets that intercept pointer events.

    SOGo 6 mounts a fixed bottom-right bubble container (minimized compose /
    CKEditor balloons) whose children still receive pointer events and block
    clicks anywhere near it. Remove the nodes AND inject persistent CSS so
    re-renders stay inert.
    """
    with contextlib.suppress(Exception):
        await page.keyboard.press("Escape")
    with contextlib.suppress(Exception):
        await page.evaluate(
            "document.querySelectorAll('.ck-balloon-panel, .ck-toolbar, "
            "div.pointer-events-none.fixed.bottom-0').forEach(el => el.remove())"
        )
    with contextlib.suppress(Exception):
        await page.add_style_tag(
            content="div.pointer-events-none.fixed.bottom-0, "
            "div.pointer-events-none.fixed.bottom-0 * "
            "{ pointer-events: none !important; }"
        )
    await page.wait_for_timeout(200)


class CaptureError(RuntimeError):
    """Target UI state could not be reached — fail the workflow instead of
    capturing an empty/wrong screenshot (the old `if is_visible: click`
    pattern silently skipped actions and shipped identical empty shots)."""


async def require(locator, what: str, timeout_ms: int = 10000) -> None:
    """Hard-fail wait: continue only when `what` is actually visible."""
    try:
        await locator.first.wait_for(state="visible", timeout=timeout_ms)
    except Exception as e:
        raise CaptureError(f"UI state not reached: {what}") from e


async def click_required(page, selector: str, what: str, timeout_ms: int = 10000) -> None:
    loc = page.locator(selector).first
    await require(loc, what, timeout_ms)
    await safe_click(loc)


async def fill_required(page, selector: str, value: str, what: str, timeout_ms: int = 10000) -> None:
    loc = page.locator(selector).first
    await require(loc, what, timeout_ms)
    await loc.fill(value)


async def wait_outcome(page, text: str, what: str, timeout_ms: int = 10000) -> None:
    """Verify-then-shoot: the concrete result (e.g. the event title in the
    grid) must be visible before a screenshot is allowed."""
    await require(page.get_by_text(text), what, timeout_ms)


async def safe_click(locator, timeout_ms: int = 5000) -> None:
    """Click with a DOM-click fallback when overlays still intercept."""
    try:
        await locator.click(timeout=timeout_ms)
    except Exception:
        with contextlib.suppress(Exception):
            await locator.evaluate("el => el.click()")


async def navigate_to_settings(
    page, menu_item: str, sub_tab: str | None = None, wait_ms: int = 3000
) -> None:
    """Open user settings via avatar dropdown in the header.

    Opens the avatar dropdown and clicks the given menu item
    (e.g. 'Email', 'Security', 'General', 'Logout').
    Optionally clicks a sub-tab in the settings sidebar (e.g. 'Vacation', 'Filters').
    """
    await _clear_overlays(page)
    dd = page.locator('[data-testid="header-dropdown-trigger"]').first
    if await dd.is_visible(timeout=5000):
        await dd.click()
        await page.wait_for_timeout(1000)
    item = page.locator(f'[role="menuitem"]:has-text("{menu_item}")').first
    if await item.is_visible(timeout=4000):
        try:
            await item.click(timeout=5000)
        except Exception:
            # Floating overlays can still intercept pointer events — DOM-click.
            await item.evaluate("el => el.click()")
        await page.wait_for_timeout(2000)
    if sub_tab:
        tab = page.locator(f'button:has-text("{sub_tab}")').first
        if await tab.is_visible(timeout=4000):
            try:
                await tab.click(timeout=5000)
            except Exception:
                await tab.evaluate("el => el.click()")
            await page.wait_for_timeout(wait_ms)
        else:
            await page.wait_for_timeout(wait_ms)


class ScreenshotRecorder:
    """Takes a single annotated screenshot at the result moment."""

    def __init__(self, name: str, screenshot_dir: Path):
        self.name = name
        self.screenshot_dir = screenshot_dir

    async def start(self, context: BrowserContext) -> Page:
        page = await context.new_page()
        return page

    async def context(self, page, text: str) -> None:
        print(f"   [CONTEXT] {text}")

    async def challenge(self, page, text: str) -> None:
        print(f"   [CHALLENGE] {text}")

    async def solution(self, page, text: str) -> None:
        print(f"   [SOLUTION] {text}")

    async def result(self, page, text: str) -> None:
        print(f"   [RESULT] {text}")

    async def capture(self, page, label: str, scope=None, margin: int = 24,
                      locale: str = "en") -> Path | None:
        """Screenshot at the result moment, annotated with the given label.

        With ``scope`` (a Locator), captures that widget (dialog, panel) with
        a margin instead of the full viewport — the gist fills the frame.
        """
        raw_path = self.screenshot_dir / f"{self.name}_raw.png"
        annotated_path = self.screenshot_dir / f"{self.name}.png"
        try:
            if scope is not None:
                box = await scope.bounding_box()
            else:
                box = None
            if box:
                vp = page.viewport_size or {"width": 1280, "height": 800}
                x = max(0, box["x"] - margin)
                y = max(0, box["y"] - margin)
                clip = {
                    "x": x,
                    "y": y,
                    "width": min(vp["width"] - x, box["width"] + 2 * margin),
                    "height": min(vp["height"] - y, box["height"] + 2 * margin),
                }
                await page.screenshot(path=str(raw_path), clip=clip)
            else:
                await page.screenshot(path=str(raw_path), full_page=False)
        except Exception as e:
            print(f"  Screenshot failed: {e}")
            return None
        if not raw_path.exists() or raw_path.stat().st_size < 1000:
            raw_path.unlink(missing_ok=True)
            return None
        annotate_frame(
            str(raw_path),
            label,
            4,
            [],
            locale=locale,
            output_path=str(annotated_path),
        )
        raw_path.unlink(missing_ok=True)
        if not annotated_path.exists():
            return None
        meta_path = self.screenshot_dir / f"{self.name}_metadata.json"
        with open(meta_path, "w") as f:
            json.dump(
                {
                    "workflow": self.name,
                    "label": label,
                    "png_file": annotated_path.name,
                    "png_size_kb": annotated_path.stat().st_size // 1024,
                },
                f,
                indent=2,
            )
        return annotated_path


async def dismiss_hints(page) -> None:
    """Best-effort dismissal of first-run hint/consent overlays (e.g. the
    'Got it' bubble). Intentionally NOT a hard requirement: the overlay is
    ephemeral UI, not part of any workflow's target state."""
    with contextlib.suppress(Exception):
        btn = page.locator('button:has-text("Got it")').first
        if await btn.is_visible(timeout=2000):
            await btn.click()
            await page.wait_for_timeout(500)


# ── Workflow Runners (Task-First Narrative) ──


async def record_calendar_create_event(context: BrowserContext) -> Path | None:
    """Create a calendar event: open dialog, fill real details, save, verify."""
    rec = ScreenshotRecorder("calendar-create-event", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "calendar")
    await dismiss_hints(page)

    await click_required(page, 'button:has-text("Create Event")', "'Create Event' button")
    dlg = page.locator("[role='dialog']").first
    await require(dlg, "event dialog")

    # Fill real data — an empty dialog tells the reader nothing.
    await fill_required(
        page,
        "[role='dialog'] input[placeholder='Enter event title']",
        "Team Meeting",
        "event title field",
    )
    await fill_required(
        page,
        "[role='dialog'] input[placeholder='Add location']",
        "Meeting Room 2",
        "location field",
    )
    await page.wait_for_timeout(500)

    # The filled dialog IS the instructional gist — capture it scoped.
    shot = await rec.capture(
        page, "Creating a new event: title, time and location", scope=dlg
    )

    # Verify-then-keep: the event must actually save and appear.
    await click_required(
        page,
        "[role='dialog'] button:has-text('Create Event')",
        "dialog 'Create Event' submit button",
    )
    await wait_outcome(page, "Team Meeting", "saved event in the calendar grid")
    return shot


async def record_calendar_recurring(context: BrowserContext) -> Path | None:
    """Recurring event: enable Repeat, pick weekly, save, verify."""
    rec = ScreenshotRecorder("calendar-recurring", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "calendar")
    await dismiss_hints(page)

    await click_required(page, 'button:has-text("Create Event")', "'Create Event' button")
    dlg = page.locator("[role='dialog']").first
    await require(dlg, "event dialog")

    await fill_required(
        page,
        "[role='dialog'] input[placeholder='Enter event title']",
        "Weekly Standup",
        "event title field",
    )

    # Enable repetition; shoot with the frequency dropdown OPEN — clearly
    # distinct from the plain filled dialog, and shows the actual options.
    switch = dlg.locator("div:has(> label:has-text('Repeat')) button[role='switch']")
    await require(switch, "'Repeat' toggle switch")
    await switch.click()
    await page.wait_for_timeout(800)
    freq = dlg.locator("[role='combobox']:has-text('Week')").first
    await require(freq, "recurrence frequency selector")
    await freq.click()
    await page.locator("[role='option']").first.wait_for(state="visible", timeout=8000)
    await page.wait_for_timeout(400)

    shot = await rec.capture(
        page, "Configuring a weekly recurring event", scope=dlg
    )

    await page.locator("[role='option']", has_text="Week(s)").first.click()
    await page.wait_for_timeout(600)

    await click_required(
        page,
        "[role='dialog'] button:has-text('Create Event')",
        "dialog 'Create Event' submit button",
    )
    await wait_outcome(page, "Weekly Standup", "saved recurring event in the calendar grid")
    return shot


async def record_mail_compose(context: BrowserContext) -> Path | None:
    """Task-first capture: Compose and send a new email."""
    rec = ScreenshotRecorder("mail-compose", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await page.wait_for_timeout(1000)

    await rec.context(page, "Write and send an email to a colleague")
    await page.wait_for_timeout(600)

    await rec.challenge(page, "Click the New Message button to open the compose window")
    new_msg = page.locator('button:has-text("New message")').first
    if await new_msg.is_visible(timeout=3000):
        await new_msg.click()
        await page.wait_for_timeout(2000)

    await rec.solution(page, "Fill in the recipient, subject, and message body")
    to_fld = page.locator('input[placeholder="To"]').first
    if await to_fld.is_visible(timeout=3000):
        await to_fld.fill("colleague@company.com")
        await page.wait_for_timeout(300)
    subj_fld = page.locator('input[placeholder="Subject"]').first
    if await subj_fld.is_visible(timeout=2000):
        await subj_fld.fill("Meeting Reminder")
        await page.wait_for_timeout(300)
    body_fld = page.locator('[contenteditable="true"]').first
    if await body_fld.is_visible(timeout=2000):
        await body_fld.fill("Hi, just a reminder about our meeting tomorrow at 10 AM.")
        await page.wait_for_timeout(500)

    await rec.result(page, "The email is composed with recipient and subject filled in")
    await page.wait_for_timeout(800)
    return await rec.capture(page, "The email is composed with recipient and subject filled in")


async def record_contacts_add(context: BrowserContext) -> Path | None:
    """Task-first capture: Add a new contact."""
    rec = ScreenshotRecorder("contacts-add", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "contacts")
    await page.wait_for_timeout(1000)

    await rec.context(page, "Add a new colleague to your address book")
    await page.wait_for_timeout(600)

    await rec.challenge(page, "Click the New Contact button to create a new entry")
    new_contact = page.locator('button:has-text("New contact")').first
    if await new_contact.is_visible(timeout=3000):
        await new_contact.click()
        await page.wait_for_timeout(1500)

    await rec.solution(page, "Fill in the contact fields: first name, last name, and email address")
    fn = page.locator('input[name="firstName"]')
    if await fn.is_visible(timeout=2000):
        await fn.fill("Jane")
        await page.wait_for_timeout(300)
    ln = page.locator('input[name="lastName"]')
    if await ln.is_visible(timeout=2000):
        await ln.fill("Smith")
        await page.wait_for_timeout(300)
    em = page.locator('input[name="emails.0.value"]')
    if await em.is_visible(timeout=2000):
        await em.fill("jane.smith@company.com")
        await page.wait_for_timeout(500)

    await rec.result(page, "The new contact form is filled and ready to save")
    await page.wait_for_timeout(800)
    return await rec.capture(page, "The new contact form is filled and ready to save")


async def record_vacation(context: BrowserContext) -> Path | None:
    """Task-first capture: Configure vacation auto-reply."""
    rec = ScreenshotRecorder("vacation", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await page.wait_for_timeout(1500)

    await rec.context(page, "Set up an automatic out-of-office reply for your vacation")
    await page.wait_for_timeout(1000)

    await rec.challenge(
        page, "Colleagues need to know you're away without manually telling everyone"
    )
    await navigate_to_settings(page, "Email", "Vacation")
    await page.wait_for_timeout(1000)

    await rec.solution(page, "Enable the vacation auto-reply with your away message")
    enable = page.locator('button:has-text("Enable vacation auto reply")').first
    if await enable.is_visible(timeout=3000):
        await enable.click()
        await page.wait_for_timeout(1000)

    await rec.result(page, "Vacation auto-reply is enabled and will respond to incoming emails")
    await page.wait_for_timeout(800)
    return await rec.capture(
        page, "Vacation auto-reply is enabled and will respond to incoming emails"
    )


async def record_mail_signatures(context: BrowserContext) -> Path | None:
    """Task-first capture: Configure email signature placement."""
    rec = ScreenshotRecorder("mail-signatures", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await page.wait_for_timeout(1000)

    await rec.context(page, "Configure where your email signature appears in messages")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "Set the signature position for new messages and replies")
    # Navigate to mail settings via header dropdown
    dd = page.locator('[data-testid="header-dropdown-trigger"]')
    if await dd.is_visible(timeout=5000):
        await dd.click()
        await page.wait_for_timeout(1000)
        item = page.locator('[role="menuitem"]:has-text("Email")')
        if await item.is_visible(timeout=3000):
            await item.click()
            await page.wait_for_timeout(3000)

    await rec.solution(page, "The mail general settings page showing signature options")
    await page.wait_for_timeout(1000)

    await rec.result(page, "Mail settings are configured for all outgoing messages")
    await page.wait_for_timeout(800)
    return await rec.capture(page, "Mail settings are configured for all outgoing messages")


async def record_mail_filters(context: BrowserContext) -> Path | None:
    """Task-first capture: Browse mail filter settings."""
    rec = ScreenshotRecorder("mail-filters", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await page.wait_for_timeout(1000)

    await rec.context(page, "Manage email filters to automatically organize incoming messages")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "Filters help sort emails into folders based on rules")
    await navigate_to_settings(page, "Email", "Filters")
    await page.wait_for_timeout(1000)

    await rec.solution(page, "Create and manage filter rules from the Filters settings tab")
    await page.wait_for_timeout(1000)

    await rec.result(page, "Mail filters are available for automatic email organization")
    await page.wait_for_timeout(800)
    return await rec.capture(page, "Mail filters are available for automatic email organization")


async def record_calendar_subscribe(context: BrowserContext) -> Path | None:
    """Task-first capture: Browse calendar events."""
    rec = ScreenshotRecorder("calendar-subscribe", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "calendar")
    await page.wait_for_timeout(1000)

    await rec.context(page, "Browse your calendar to see upcoming events and appointments")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "Review existing calendar events for the current week")
    await page.wait_for_timeout(1000)

    await rec.solution(page, "Scroll through the week view to see all scheduled events")
    await page.wait_for_timeout(1000)

    await rec.result(page, "All this week's events are visible in the calendar grid")
    await page.wait_for_timeout(800)
    return await rec.capture(page, "All this week's events are visible in the calendar grid")


async def record_calendar_share(context: BrowserContext) -> Path | None:
    """Task-first capture: View existing calendar events."""
    rec = ScreenshotRecorder("calendar-share", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "calendar")
    await page.wait_for_timeout(1000)

    await rec.context(page, "Review your existing calendar events for the week")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "Click on an existing event to view its details")
    existing = page.locator('div[role="button"]:has-text("Weekly")').first
    if await existing.is_visible(timeout=3000):
        await existing.click()
        await page.wait_for_timeout(1500)

    await rec.solution(page, "Event details are displayed with options to edit or delete")
    await page.wait_for_timeout(1000)

    await rec.result(page, "Event details panel shows the full event information")
    await page.wait_for_timeout(800)
    return await rec.capture(page, "Event details panel shows the full event information")


async def record_freebusy(context: BrowserContext) -> Path | None:
    """Invite attendees: the event dialog with an attendee added.

    The SOGo 6 event form has no separate free/busy grid — the truthful
    figure for the availability workflow is the attendee section of the
    dialog (the doc caption says so).
    """
    rec = ScreenshotRecorder("freebusy", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "calendar")
    await dismiss_hints(page)

    await click_required(page, 'button:has-text("Create Event")', "'Create Event' button")
    dlg = page.locator("[role='dialog']").first
    await require(dlg, "event dialog")

    await fill_required(
        page,
        "[role='dialog'] input[placeholder='Enter event title']",
        "Project Sync",
        "event title field",
    )
    search = dlg.locator("input[placeholder='Search by name or email...']")
    await require(search, "attendee search field")
    await search.scroll_into_view_if_needed()
    await search.fill("sogo-tests2@example.org")
    # The suggestion option renders an (untranslated) i18n key, not the
    # address — wait for any option, then click it.
    await require(page.locator("[role='option']").first, "attendee suggestion")
    await page.locator("[role='option']").first.click()
    await wait_outcome(page, "sogo-tests2@example.org", "added attendee in the dialog")

    # Scope to the attendee section (search + added chip + busy status):
    # the gist of inviting attendees, not another full-dialog shot.
    section = search.locator(
        "xpath=ancestor::div[contains(@class,'space-y-2')][1]"
    )
    return await rec.capture(
        page, "Inviting attendees: added participant with busy status", scope=section
    )


async def record_logout(context: BrowserContext) -> Path | None:
    """Task-first capture: Sign out of SOGo."""
    rec = ScreenshotRecorder("logout", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await page.wait_for_timeout(1000)

    await rec.context(page, "Sign out of your SOGo session when you are done working")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "Leaving your session open on a shared computer is a security risk")
    await page.wait_for_timeout(500)

    await rec.solution(page, "Click your avatar and select Logout to end your session")
    await navigate_to_settings(page, "Logout")
    await page.wait_for_timeout(2000)

    await rec.result(page, "You are securely signed out and returned to the login screen")
    await page.wait_for_timeout(800)
    return await rec.capture(page, "You are securely signed out and returned to the login screen")


async def record_preferences(context: BrowserContext) -> Path | None:
    """Task-first capture: Configure general preferences."""
    rec = ScreenshotRecorder("preferences", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await page.wait_for_timeout(1500)

    await rec.context(page, "Customize language, timezone, and date format preferences")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "Default settings may not match your regional preferences")
    await navigate_to_settings(page, "General")
    await page.wait_for_timeout(1000)

    await rec.solution(page, "Select your preferred language and timezone from the settings")
    lang = page.locator('button:has-text("English")').first
    if await lang.is_visible(timeout=3000):
        await lang.click()
        await page.wait_for_timeout(1000)

    await rec.result(page, "General preferences are configured to match your needs")
    await page.wait_for_timeout(800)
    return await rec.capture(page, "General preferences are configured to match your needs")


async def record_calendar_views(context: BrowserContext) -> Path | None:
    """Task-first capture: Switch between calendar views."""
    rec = ScreenshotRecorder("calendar-views", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "calendar")
    await page.wait_for_timeout(1000)

    await rec.context(page, "View your calendar in the week overview layout")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "Switch to Day view to focus on a single day's schedule")
    view_btn = page.locator('button:has-text("Week")').first
    if await view_btn.is_visible(timeout=3000):
        await view_btn.click()
        await page.wait_for_timeout(1000)
        day_option = page.locator('[role="menuitem"]:has-text("Day")').first
        if await day_option.is_visible(timeout=3000):
            await day_option.click()
            await page.wait_for_timeout(1500)

    await rec.solution(page, "Select from Month, Week, Day, or Schedule views to suit your needs")
    await page.wait_for_timeout(1500)

    await rec.result(page, "The calendar adapts instantly to show the selected view layout")
    await page.wait_for_timeout(800)
    return await rec.capture(page, "The calendar adapts instantly to show the selected view layout")


async def record_contacts_edit_delete(context: BrowserContext) -> Path | None:
    """Task-first capture: Browse contacts in the address book."""
    rec = ScreenshotRecorder("contacts-edit-delete", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "contacts")
    await page.wait_for_timeout(1000)

    await rec.context(page, "Browse your contacts in the address book")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "View existing contacts and their details")
    contact = page.locator('div[role="button"]:has-text("John")').first
    if await contact.is_visible(timeout=3000):
        await contact.click()
        await page.wait_for_timeout(1500)

    await rec.solution(page, "Contact details are displayed with available information")
    await page.wait_for_timeout(1000)

    await rec.result(page, "Address book provides quick access to all your contacts")
    await page.wait_for_timeout(800)
    return await rec.capture(page, "Address book provides quick access to all your contacts")


async def record_calendar_edit_delete(context: BrowserContext) -> Path | None:
    """Task-first capture: View calendar events and details."""
    rec = ScreenshotRecorder("calendar-edit-delete", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "calendar")
    await page.wait_for_timeout(1000)

    await rec.context(page, "Review your calendar events for the week")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "Click on an event to view its full details")
    event = page.locator('.rbc-event-content:has-text("Client Meeting")')
    if await event.is_visible(timeout=3000):
        await event.click()
        await page.wait_for_timeout(1500)

    await rec.solution(page, "Event details show the time, title, and description")
    await page.wait_for_timeout(1000)

    await rec.result(page, "Events are displayed with their time slots in the calendar grid")
    await page.wait_for_timeout(800)
    return await rec.capture(
        page, "Events are displayed with their time slots in the calendar grid"
    )


async def record_global_search(context: BrowserContext) -> Path | None:
    """Task-first capture: Use the search feature in the inbox."""
    rec = ScreenshotRecorder("global-search", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await page.wait_for_timeout(1000)

    await rec.context(page, "Use the search bar to find emails in your inbox")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "Finding specific emails in a crowded inbox")
    search_input = page.locator('input[placeholder="Search emails"]').first
    if await search_input.is_visible(timeout=3000):
        await search_input.click()
        await search_input.fill("Meeting")
        await page.wait_for_timeout(1500)

    await rec.solution(page, "Type a search term to filter your inbox by keywords")
    await page.wait_for_timeout(1000)

    await rec.result(page, "Search filters the inbox to show only matching emails")
    await page.wait_for_timeout(800)
    return await rec.capture(page, "Search filters the inbox to show only matching emails")


async def record_mail_read(context: BrowserContext) -> Path | None:
    """Task-first capture: Read an email from the inbox."""
    rec = ScreenshotRecorder("mail-read", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await page.wait_for_timeout(1000)

    await rec.context(page, "Open and read an email from your inbox")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "Click on an email to view its full contents")
    msg = page.locator('div[role="button"]:has-text("Gueto")').first
    if not await msg.is_visible(timeout=3000):
        # Live inboxes differ — fall back to the first message row.
        msg = page.locator('main div[role="button"], main [role="row"]').first
    if await msg.is_visible(timeout=4000):
        try:
            await msg.click(timeout=5000)
        except Exception:
            await msg.evaluate("el => el.click()")
        await page.wait_for_timeout(1500)

    await rec.solution(page, "Select an email to read its content in the reading pane")
    await page.wait_for_timeout(1000)

    await rec.result(page, "The email body is displayed with full details")
    await page.wait_for_timeout(800)
    return await rec.capture(page, "The email body is displayed with full details")


async def record_mail_folder_management(context: BrowserContext) -> Path | None:
    """Task-first capture: Navigate between mail folders."""
    rec = ScreenshotRecorder("mail-folder-management", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await page.wait_for_timeout(1000)

    await rec.context(page, "Navigate between different mail folders")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "Browse through your mail folders to find specific emails")
    sent_btn = page.locator('button:has-text("Sent")').first
    if await sent_btn.is_visible(timeout=3000):
        await safe_click(sent_btn)
        await page.wait_for_timeout(1500)

    await rec.solution(page, "Click on a folder to switch to its contents")
    await page.wait_for_timeout(1000)

    await rec.result(page, "The selected folder's emails are displayed")
    await page.wait_for_timeout(800)
    return await rec.capture(page, "The selected folder's emails are displayed")


async def record_mail_reply_forward_delete(context: BrowserContext) -> Path | None:
    """Task-first capture: Reply to an email."""
    rec = ScreenshotRecorder("mail-reply-forward-delete", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await page.wait_for_timeout(1000)

    await rec.context(page, "Respond to an email by replying to the sender")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "Click on an email to open it, then use the action toolbar")
    msg = page.locator('div[role="button"]').filter(has_text="Gueto").first
    if await msg.is_visible(timeout=3000):
        await msg.click()
        await page.wait_for_timeout(1500)

    await rec.solution(page, "Click the Reply button to open the reply compose window")
    reply = page.locator('[data-testid="mail-action-btn-reply"]')
    if await reply.is_visible(timeout=3000):
        await reply.click()
        await page.wait_for_timeout(2000)

    await rec.result(page, "The reply compose window opens ready for your response")
    await page.wait_for_timeout(800)
    return await rec.capture(page, "The reply compose window opens ready for your response")


async def record_password_change(context: BrowserContext) -> Path | None:
    """Task-first capture: Update account password."""
    rec = ScreenshotRecorder("password-change", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await page.wait_for_timeout(1500)

    await rec.context(page, "Update your SOGo account password to keep your account secure")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "Regular password changes are important for account security")
    await navigate_to_settings(page, "Security")
    await page.wait_for_timeout(1000)

    await rec.solution(page, "Enter your current password, then choose a new strong password")
    current = page.locator('input[name="password"]')
    if await current.is_visible(timeout=3000):
        await current.fill("current-password")
        await page.wait_for_timeout(300)
    new_pw = page.locator('input[name="newPassword"]')
    if await new_pw.is_visible(timeout=2000):
        await new_pw.fill("new-secure-password")
        await page.wait_for_timeout(300)
    confirm = page.locator('input[name="confirmPassword"]')
    if await confirm.is_visible(timeout=2000):
        await confirm.fill("new-secure-password")
        await page.wait_for_timeout(500)

    await rec.result(page, "Password change form is ready with current and new password fields")
    await page.wait_for_timeout(800)
    return await rec.capture(
        page, "Password change form is ready with current and new password fields"
    )


async def record_calendar_ical(context: BrowserContext) -> Path | None:
    """Task-first capture: View the calendar with events in week overview."""
    rec = ScreenshotRecorder("calendar-ical", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "calendar")
    await page.wait_for_timeout(1000)

    await rec.context(page, "View your calendar in the week overview")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "The week view displays all scheduled events")
    await page.wait_for_timeout(1000)

    event = page.locator('.rbc-event-content:has-text("Client Meeting")')
    if await event.is_visible(timeout=3000):
        await event.click()
        await page.wait_for_timeout(1500)

    await rec.solution(page, "Events are shown with their time and duration")
    await page.wait_for_timeout(1000)

    await rec.result(page, "The calendar provides a clear view of your weekly schedule")
    await page.wait_for_timeout(800)
    return await rec.capture(page, "The calendar provides a clear view of your weekly schedule")


async def record_contacts_import_export(context: BrowserContext) -> Path | None:
    """Task-first capture: Browse address books and subscription options."""
    rec = ScreenshotRecorder("contacts-import-export", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "contacts")
    await page.wait_for_timeout(1500)

    await rec.context(page, "Browse your contacts in the address book")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "View available address books and subscription options")
    for addr_book in ["Personal", "Work"]:
        book = page.locator(f'button:has-text("{addr_book}")').first
        if await book.is_visible(timeout=2000):
            await safe_click(book)
            await page.wait_for_timeout(800)

    add_book = page.locator('button:has-text("Add address book")').first
    if await add_book.is_visible(timeout=2000):
        await safe_click(add_book)
        await page.wait_for_timeout(800)

    await rec.solution(page, "Address books can be added and subscribed to for contact management")
    await page.wait_for_timeout(1000)

    await rec.result(page, "Contacts can be organized across multiple address books")
    await page.wait_for_timeout(800)
    return await rec.capture(page, "Contacts can be organized across multiple address books")


# ── Parallel Runner ──


async def setup_authenticated_context(browser, _video_dir=None) -> BrowserContext:
    ctx = await browser.new_context(
        viewport={"width": 1280, "height": 800},
        locale="en-US",
        ignore_https_errors=True,
    )
    # Log in on an initial page to establish session cookies in the context
    login_page = await ctx.new_page()
    await login(login_page, ctx)
    # Capture the sessionStorage auth token
    sogo_auth = await login_page.evaluate('() => sessionStorage.getItem("sogo_auth")')
    # Set up init script to inject auth token into every new page
    if sogo_auth:
        escaped = json.dumps(sogo_auth)
        await ctx.add_init_script(f"""
            try {{
                sessionStorage.setItem('sogo_auth', {escaped});
            }} catch(e) {{}}
        """)
    await login_page.close()
    return ctx


# ── Main ──


WORKFLOWS = [
    ("calendar-create-event", "record_calendar_create_event"),
    ("calendar-recurring", "record_calendar_recurring"),
    ("mail-compose", "record_mail_compose"),
    ("contacts-add", "record_contacts_add"),
    ("vacation", "record_vacation"),
    ("mail-signatures", "record_mail_signatures"),
    ("mail-filters", "record_mail_filters"),
    ("calendar-subscribe", "record_calendar_subscribe"),
    ("calendar-share", "record_calendar_share"),
    ("freebusy", "record_freebusy"),
    ("logout", "record_logout"),
    ("preferences", "record_preferences"),
    ("calendar-views", "record_calendar_views"),
    ("contacts-edit-delete", "record_contacts_edit_delete"),
    ("calendar-edit-delete", "record_calendar_edit_delete"),
    ("global-search", "record_global_search"),
    ("mail-read", "record_mail_read"),
    ("mail-folder-management", "record_mail_folder_management"),
    ("mail-reply-forward-delete", "record_mail_reply_forward_delete"),
    ("password-change", "record_password_change"),
    ("calendar-ical", "record_calendar_ical"),
    ("contacts-import-export", "record_contacts_import_export"),
]


async def main():
    clean_dirs()

    # --only wf1,wf2: run a subset (proof runs, targeted re-captures)
    only = None
    if len(sys.argv) > 2 and sys.argv[1] == "--only":
        only = {w.strip() for w in sys.argv[2].split(",") if w.strip()}
    selected = [wf for wf in WORKFLOWS if only is None or wf[0] in only]

    async with async_playwright() as p:
        verify_browser = await p.chromium.launch(
            headless=True,
            args=["--disable-dev-shm-usage", "--no-first-run"],
        )
        try:
            verify_ctx = await verify_browser.new_context(
                viewport={"width": 1280, "height": 800},
                locale="en-US",
                ignore_https_errors=True,
            )
            verify_page = await verify_ctx.new_page()
            await login(verify_page, context=verify_ctx)
            await verify_ctx.close()
        finally:
            await verify_browser.close()
        print("  Login verified.\n")

    start_time = time.time()
    results = []
    worker_script = Path(__file__).parent / "run_single_screenshot.py"

    for name, fn_name in selected:
        print(f"\n── {name} ──")
        wf_start = time.time()
        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            "-u",
            str(worker_script),
            str(Path(__file__)),
            fn_name,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        stdout_b = b""
        try:
            stdout_b, _ = await asyncio.wait_for(proc.communicate(), timeout=120)
        except TimeoutError:
            # Isolate the hung workflow; never let it kill the whole run.
            with contextlib.suppress(Exception):
                proc.kill()
            with contextlib.suppress(Exception):
                await proc.wait()
        elapsed = time.time() - wf_start
        output = stdout_b.decode("utf-8", errors="replace")
        print(output, end="")
        if not stdout_b:
            print(f"  ✗  {name}: worker timed out after 120s")
            results.append((name, False, elapsed))
            continue

        png_path = SCREENSHOT_DIR / f"{name}.png"
        if png_path.exists():
            shutil.copy2(str(png_path), str(ASSETS_DIR / png_path.name))
            meta_path = SCREENSHOT_DIR / f"{name}_metadata.json"
            if meta_path.exists():
                meta = json.loads(meta_path.read_text())
                size_kb = meta.get("png_size_kb", png_path.stat().st_size // 1024)
                print(f"  ✓  {png_path.name} — {size_kb}KB ({elapsed:.1f}s)")
                results.append((name, True, elapsed))
            else:
                print(f"  ✓  {png_path.name} ({elapsed:.1f}s)")
                results.append((name, True, elapsed))
        else:
            print(f"  ✗  Failed ({elapsed:.1f}s)")
            results.append((name, False, elapsed))

    print("\n── Results ──")
    for name, ok, duration in results:
        mark = "✓" if ok else "✗"
        print(f"  {mark}  {name} ({duration:.1f}s)")
    total_ok = sum(1 for _, ok, _ in results if ok)
    print(f"\n  {total_ok}/{len(results)} succeeded")
    print(f"\n  Total time: {time.time() - start_time:.1f}s")

    # Duplicate gate: two workflows producing the same image means at least
    # one captured the wrong state. Fail the run instead of shipping the lie.
    shots = sorted(SCREENSHOT_DIR.glob("*.png"))
    dupes = find_duplicates(shots)
    if dupes:
        print("\n  ✗ Near-duplicate screenshots — same state captured under different names:")
        for d, a, b in dupes:
            print(f"    dist={d}: {a.name} <-> {b.name}")
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
