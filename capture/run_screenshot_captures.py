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

from playwright.async_api import BrowserContext, Locator, Page, async_playwright

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


async def click_required(page, selector: str | Locator, what: str, timeout_ms: int = 10000) -> None:
    # Accept an existing Locator too — passing str(locator) is a repr, never a selector.
    loc = selector if isinstance(selector, Locator) else page.locator(selector).first
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
    """Compose new message: compose panel filled with To, Subject, Body.

    SOGo 6 opens compose as a floating panel, NOT a [role=dialog] (probe
    2026-09-14). Selectors therefore stay page-level."""
    rec = ScreenshotRecorder("mail-compose", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await dismiss_hints(page)

    await click_required(page, 'button:has-text("New message")', "compose button")
    await fill_required(
        page, 'input[placeholder="To"]', "team@example.org", "To field"
    )
    # The To field is a tag input — the value only registers as a chip on Enter.
    await page.keyboard.press("Enter")
    await fill_required(
        page, 'input[placeholder="Subject"]', "Team Meeting Agenda", "Subject field"
    )
    body = page.locator('[contenteditable="true"]').first
    await require(body, "Email body field")
    await body.fill("Hi team,\n\nHere is the agenda for tomorrow's meeting...\n")
    await page.wait_for_timeout(500)

    # Filled compose panel IS the instructional gist — actual sending not needed.
    return await rec.capture(page, "Compose panel: To, Subject, and body filled")


async def record_contacts_add(context: BrowserContext) -> Path | None:
    """New contact form: create button clicked and fields filled."""
    rec = ScreenshotRecorder("contacts-add", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "contacts")
    await dismiss_hints(page)

    await click_required(page, 'button:has-text("New contact")', "New contact button")
    dlg = page.locator("[role='dialog']").first
    await require(dlg, "New contact dialog")
    await page.wait_for_timeout(500)

    await fill_required(page, 'input[name="firstName"]', "John", "First Name field")
    await fill_required(page, 'input[name="lastName"]', "Doe", "Last Name field")
    em = dlg.locator('input[name="emails.0.value"]')
    await require(em, "Email field")
    await em.fill("john.doe@company.com")
    await page.wait_for_timeout(500)

    return await rec.capture(
        page, "New contact dialog with First Name, Last Name, Email filled", scope=dlg
    )


async def record_vacation(context: BrowserContext) -> Path | None:
    """Vacation settings: Email -> Vacation page with fields visible."""
    rec = ScreenshotRecorder("vacation", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await navigate_to_settings(page, "Email", "Vacation")

    await wait_outcome(page, "Vacation", "Vacation settings tab")
    section = page.locator("form, section").filter(has_text="Vacation").first
    await require(section, "Vacation settings section")
    await page.wait_for_timeout(400)

    return await rec.capture(page, "Vacation auto-reply settings page")


async def record_mail_signatures(context: BrowserContext) -> Path | None:
    """Mail signatures settings: Email settings page with signature section."""
    rec = ScreenshotRecorder("mail-signatures", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await navigate_to_settings(page, "Email")

    await require(page.get_by_text("Signature"), "Signature settings section")
    await page.wait_for_timeout(400)

    return await rec.capture(page, "Email settings page showing the Signature configuration section")


async def record_mail_filters(context: BrowserContext) -> Path | None:
    """Mail filters settings: Email -> Filters page."""
    rec = ScreenshotRecorder("mail-filters", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await navigate_to_settings(page, "Email", "Filters")

    await wait_outcome(page, "Add filter", "Filters list with 'Add filter' button")
    await page.wait_for_timeout(400)

    return await rec.capture(page, "Mail Filters settings page")


async def record_calendar_subscribe(context: BrowserContext) -> Path | None:
    """Calendar subscribe: Add -> Subscribe to Calendar form."""
    rec = ScreenshotRecorder("calendar-subscribe", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "calendar")
    await dismiss_hints(page)

    btn = page.locator('button:has-text("Subscribe")').first
    await click_required(page, btn, "Subscribe to Calendar button")

    modal = page.locator("[role='dialog'], [role='alertdialog']").filter(has_text="Subscribe").first
    await require(modal, "Calendar Subscribe dialog")
    await page.wait_for_timeout(400)

    return await rec.capture(page, "Subscribe to Calendar dialog", scope=modal)


# NOTE: record_calendar_share was removed — the SOGo 6 demo UI has no Share
# entry point (no context menu on events, none on sidebar calendars; probed
# 2026-09-14). The sogo-calendar-share docs page is SOGo 5 content.

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
    """Logout: post logout, back to login screen."""
    rec = ScreenshotRecorder("logout", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await dismiss_hints(page)

    # Open header menu and click Logout
    dd = page.locator('[data-testid="header-dropdown-trigger"]').first
    await click_required(page, dd, "Header dropdown")
    logout = page.locator('[role="menuitem"]:has-text("Logout")').first
    await click_required(page, logout, "Logout menu item")

    # Wait for redirect to login page. SOGo 6 uses a 2-step login: after
    # logout only the email step is shown (no password field — probe 2026-09-14).
    await page.wait_for_selector('input[type="email"]', timeout=8000)
    await require(page.locator('input[placeholder*="mail"]'), "Email field on login page")
    await page.wait_for_timeout(500)

    return await rec.capture(page, "Post-logout: SOGo login screen")


async def record_preferences(context: BrowserContext) -> Path | None:
    """Preferences: General settings page."""
    rec = ScreenshotRecorder("preferences", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await navigate_to_settings(page, "General")

    await require(page.get_by_text("Timezone"), "Timezone setting")
    await page.wait_for_timeout(400)

    return await rec.capture(page, "General Preferences settings page")


async def record_calendar_views(context: BrowserContext) -> Path | None:
    """Calendar views: view toggle open showing Day/Week/Month/Schedule."""
    rec = ScreenshotRecorder("calendar-views", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "calendar")
    await dismiss_hints(page)

    view_btn = page.locator('button:has-text("Week")').first
    await click_required(page, view_btn, "View toggle button")

    # The view switcher is a listbox, not a menu (probe 2026-09-14).
    menu = page.locator("[role='listbox']").first
    if not await menu.is_visible(timeout=3000):
        # A first click can be swallowed while the toolbar hydrates — retry.
        await safe_click(view_btn)
    await require(menu, "Calendar view listbox")
    await require(page.locator('[role="option"]:has-text("Day")'), "Day option")
    await require(page.locator('[role="option"]:has-text("Month")'), "Month option")
    await require(page.locator('[role="option"]:has-text("Schedule")'), "Schedule option")
    await page.wait_for_timeout(300)

    return await rec.capture(page, "Calendar view selector: Day, Week, Month, Schedule", scope=menu)


async def record_contacts_edit_delete(context: BrowserContext) -> Path | None:
    """Contact editor: editing phone number field in edit dialog."""
    rec = ScreenshotRecorder("contacts-edit-delete", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "contacts")
    await dismiss_hints(page)

    # Create a contact, click it to open view, then go to edit URL
    await click_required(page, 'button:has-text("New contact")', "New contact")
    dlg = page.locator("[role='dialog']").first
    await require(dlg, "contact dialog")
    await fill_required(page, 'input[name="firstName"]', "Tests", "First Name")
    await fill_required(page, 'input[name="lastName"]', "Two", "Last Name")
    em = page.locator('input[name="emails.0.value"]')
    await require(em, "Email field")
    await em.fill("tests.two@company.com")

    # Add phone number
    phone_btn = dlg.locator('button:has-text("Add phone")').first
    await require(phone_btn, "Add phone button")
    await phone_btn.click()
    await page.wait_for_timeout(500)
    phone_in = dlg.locator('input[type="tel"], input[name*="phone"]').first
    await require(phone_in, "phone input field")
    await phone_in.fill("+1 555-1234")
    await page.wait_for_timeout(400)

    # Full page, not scope=dlg: a scoped contact dialog is visually near-
    # identical to the calendar event dialogs (phash dist=8 → duplicate gate
    # flags it). Full page keeps the address-book context and stays distinct.
    return await rec.capture(page, "Contact dialog: editing phone number in new contact")


async def record_calendar_edit_delete(context: BrowserContext) -> Path | None:
    """Calendar event popover: click event to see Edit/Delete buttons."""
    rec = ScreenshotRecorder("calendar-edit-delete", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "calendar")
    await dismiss_hints(page)

    # Click an existing event — the demo's create-event API intermittently
    # returns 'Creation failed' (probed 2026-09-14), and the popover with
    # Edit/Delete is the instructional gist regardless of who created it.
    event = page.locator(".rbc-event-content").first
    await require(event, "event in calendar grid")
    await safe_click(event)
    await page.wait_for_timeout(800)

    # Wait for details/popover with Edit/Delete
    await require(page.locator('button:has-text("Edit"), [role="button"][aria-label*="Edit"]').first, "Edit button")
    await page.wait_for_timeout(400)

    return await rec.capture(page, "Calendar event detailed view with Edit and Delete options")


async def record_global_search(context: BrowserContext) -> Path | None:
    """Global search: search bar focused with results dropdown."""
    rec = ScreenshotRecorder("global-search", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await dismiss_hints(page)

    search_in = page.locator('input[placeholder*="earch"]').first
    await click_required(page, search_in, "Search input")
    await search_in.fill("Team")

    # Search executes on Enter; a filter popover (role=dialog) opens (probe
    # 2026-09-14). Wait for it as the visible outcome.
    await page.keyboard.press("Enter")
    await require(page.locator("[role='dialog']").first, "Search filter popover")
    await page.wait_for_timeout(400)

    return await rec.capture(page, "Global search: search term entered and results shown")


async def record_mail_read(context: BrowserContext) -> Path | None:
    """Mail read: message opened in reading pane with From/Subject/body.

    Opens an existing demo message — self-sent mail is not delivered by the
    demo server (probed 2026-09-14), so no compose-and-send machinery."""
    rec = ScreenshotRecorder("mail-read", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await dismiss_hints(page)

    msg = page.locator('main div[role="button"]').first
    await require(msg, "Message in inbox")
    # Read row text BEFORE clicking — the click hides the inbox list.
    lines = sorted((await msg.inner_text()).split("\n"), key=len, reverse=True)
    await msg.click()
    await page.wait_for_timeout(1200)

    # Reading pane is the nested <main>; verify From header and the subject
    # (the longest row line that actually renders in the pane).
    pane = page.locator("main").last
    await require(pane.get_by_text("From"), "From header in reading pane")
    subject = ""
    for line in lines:
        candidate = line.strip()
        if len(candidate) > 8 and await pane.get_by_text(candidate).count():
            subject = candidate
            break
    await require(pane.get_by_text(subject), "Subject in reading pane")
    await page.wait_for_timeout(400)

    return await rec.capture(page, "Message opened in reading pane")


async def record_mail_folder_management(context: BrowserContext) -> Path | None:
    """Mail folder management: sidebar folder list with Sent selected."""
    rec = ScreenshotRecorder("mail-folder-management", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await dismiss_hints(page)

    # Click Sent folder
    sent = page.locator('button:has-text("Sent")').first
    await require(sent, "Sent folder button")
    await sent.click()
    await page.wait_for_timeout(1000)

    # Ensure selected state
    await require(page.get_by_text("Sent"), "Sent folder content context")
    await page.wait_for_timeout(400)

    return await rec.capture(page, "Mail folder sidebar with Sent folder open")


# NOTE: record_mail_reply_forward_delete was removed — the SOGo 6 demo reading
# pane has no Reply/Forward/Delete buttons (only 'Move to folder' and a
# 'More actions' menu with Archive/Download/Print/…; probed 2026-09-14). The
# sogo-mail-reply-forward-delete docs page is SOGo 5 content.

async def record_password_change(context: BrowserContext) -> Path | None:
    """Password change: Security settings page with password fields filled."""
    rec = ScreenshotRecorder("password-change", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await navigate_to_settings(page, "Security")

    await wait_outcome(page, "Password", "Password settings section")
    # Fill the fields so the form is visually complete
    current = page.locator('input[name="password"], input[type="password"]').nth(0)
    await require(current, "Current password field")
    # Use dummy values — screenshot, not action
    await current.fill("old-password")
    new_pw = page.locator('input[name="newPassword"], input[type="password"]').nth(1)
    await require(new_pw, "New password field")
    await new_pw.fill("new-password")
    confirm = page.locator('input[name="confirmPassword"], input[type="password"]').nth(2)
    if await confirm.is_visible(timeout=3000):
        await confirm.fill("new-password")
    await page.wait_for_timeout(400)

    return await rec.capture(page, "Security page: Password change form filled")


# NOTE: record_calendar_ical and record_contacts_import_export were removed —
# the SOGo 6 demo UI exposes no iCal/Export option in Calendar settings and no
# Import/Export for address books (probed 2026-09-14). The corresponding doc
# pages are SOGo 5 content with SOGo 5 screenshots.


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
    ("freebusy", "record_freebusy"),
    ("logout", "record_logout"),
    ("preferences", "record_preferences"),
    ("calendar-views", "record_calendar_views"),
    ("contacts-edit-delete", "record_contacts_edit_delete"),
    ("calendar-edit-delete", "record_calendar_edit_delete"),
    ("global-search", "record_global_search"),
    ("mail-read", "record_mail_read"),
    ("mail-folder-management", "record_mail_folder_management"),
    ("password-change", "record_password_change"),
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
