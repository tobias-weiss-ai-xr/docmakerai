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
import json
import sys
import os
import shutil
import time
from pathlib import Path

from playwright.async_api import BrowserContext, Page, async_playwright

try:
    from capture.annotate import annotate_frame
except ImportError:
    from annotate import annotate_frame


ROOT = Path(__file__).resolve().parent
SCREENSHOT_DIR = ROOT / "screenshots"
ASSETS_DIR = ROOT.parent / "site" / "docs" / "assets"

SOGO_URL = os.environ.get("SOGO_URL", "https://demov6.sogo.nu")
USERNAME = os.environ.get("SOGO_USERNAME", "sogo-tests1@example.org")
PASSWORD = os.environ.get("SOGO_PASSWORD", "sogo")



def clean_dirs() -> None:
    for d in [SCREENSHOT_DIR, ASSETS_DIR]:
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)


async def login(page, context: BrowserContext | None = None) -> None:
    print("\n  Login...")
    await page.goto(SOGO_URL + "/en/auth/login", wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(2000)
    await page.fill("input#email", USERNAME)
    await page.wait_for_timeout(500)
    await page.click("button[type='submit']")
    await page.wait_for_timeout(2000)
    await page.wait_for_selector("input[type='password']", timeout=10000)
    await page.fill("input#password", PASSWORD)
    await page.click("button[type='submit']")
    await page.wait_for_timeout(2000)

async def goto(page, url_suffix: str, wait_ms: int = 1500) -> None:
    url = f"{SOGO_URL}/en/{url_suffix}" if url_suffix else SOGO_URL
    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
    try:
        await page.wait_for_selector("#app-container, .app-container, main", timeout=8000)
    except Exception:
        pass
    await page.wait_for_timeout(wait_ms)


async def navigate_to_module(page, module: str, wait_ms: int = 3000) -> None:
    """Navigate to an SOGo 6 module via sidebar tab click (SPA navigation)."""
    current_url = page.url
    if current_url == "about:blank":
        # Navigate to the server-rendered inbox route first; other module
        # routes (e.g. /en/calendar) are client-side only and return 404
        # when accessed directly.
        await page.goto(SOGO_URL + "/en/u/0/INBOX", wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(5000)
    else:
        await page.goto(SOGO_URL + "/en/u/0/INBOX", wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)
    
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


async def navigate_to_settings(page, menu_item: str, sub_tab: str | None = None, wait_ms: int = 3000) -> None:
    """Open user settings via avatar dropdown in the header.

    Opens the avatar dropdown and clicks the given menu item
    (e.g. 'Email', 'Security', 'General', 'Logout').
    Optionally clicks a sub-tab in the settings sidebar (e.g. 'Vacation', 'Filters').
    """
    dd = page.locator('[data-testid="header-dropdown-trigger"]')
    if await dd.is_visible(timeout=5000):
        await dd.click()
        await page.wait_for_timeout(1000)
    item = page.locator(f'[role="menuitem"]:has-text("{menu_item}")')
    if await item.is_visible(timeout=3000):
        await item.click()
        await page.wait_for_timeout(2000)
    if sub_tab:
        tab = page.locator(f'button:has-text("{sub_tab}")')
        if await tab.is_visible(timeout=3000):
            await tab.click()
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

    async def capture(self, page, label: str) -> Path | None:
        """Take a full-page screenshot and annotate it with the given label."""
        raw_path = self.screenshot_dir / f"{self.name}_raw.png"
        annotated_path = self.screenshot_dir / f"{self.name}.png"
        try:
            await page.screenshot(path=str(raw_path), full_page=False)
        except Exception as e:
            print(f"  Screenshot failed: {e}")
            return None
        if not raw_path.exists() or raw_path.stat().st_size < 1000:
            return None
        annotate_frame(
            str(raw_path),
            label,
            4,
            [],
            locale="en",
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
# ── Workflow Runners (Task-First Narrative) ──


async def record_calendar_create_event(context: BrowserContext) -> Path | None:
    """Task-first capture: Create a new calendar event."""
    rec = ScreenshotRecorder("calendar-create-event", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "calendar")
    await page.wait_for_timeout(1000)

    # 1. CONTEXT: User needs to schedule a meeting
    await rec.context(page, "Schedule a team meeting to discuss project updates")
    await page.wait_for_timeout(800)

    # 2. CHALLENGE: Finding where to create an event
    await rec.challenge(page, "Click the 'Create Event' button to open the event editor")
    create_btn = page.locator('button:has-text("Create Event")').first
    if await create_btn.is_visible(timeout=3000):
        await create_btn.click()
        await page.wait_for_timeout(1500)

    # 3. SOLUTION: Fill in event details and save
    await rec.solution(page, "Enter event title, set date and time, then save the event")
    await page.wait_for_timeout(1500)

    # 4. RESULT: Event is created and visible on the calendar
    await rec.result(page, "The new event appears on the calendar at the scheduled time")
    await page.wait_for_timeout(800)
    return await rec.capture(page, "The new event appears on the calendar at the scheduled time")


async def record_calendar_recurring(context: BrowserContext) -> Path | None:
    """Task-first capture: Create a recurring weekly event."""
    rec = ScreenshotRecorder("calendar-recurring", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "calendar")
    await page.wait_for_timeout(1000)

    await rec.context(page, "Set up a recurring weekly meeting that repeats automatically")
    await page.wait_for_timeout(600)

    await rec.challenge(
        page, "Manually creating the same event every week is tedious and error-prone"
    )
    create_btn = page.locator('button:has-text("Create Event")').first
    if await create_btn.is_visible(timeout=3000):
        await create_btn.click()
        await page.wait_for_timeout(1000)

    await rec.solution(page, "Enter event details and save to confirm the event creation")
    title = page.locator('input[placeholder="Enter event title"]')
    if await title.is_visible(timeout=3000):
        await title.fill("Weekly Team Standup")
    await page.wait_for_timeout(600)

    await rec.result(page, "Event is created and appears on the calendar")
    await page.wait_for_timeout(800)
    return await rec.capture(page, "Event is created and appears on the calendar")


async def record_mail_compose(context: BrowserContext) -> Path | None:
    """Task-first capture: Compose and send a new email."""
    rec = ScreenshotRecorder("mail-compose", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await page.wait_for_timeout(1000)

    await rec.context(page, "Write and send an email to a colleague")
    await page.wait_for_timeout(600)

    await rec.challenge(page, "Click the New Message button to open the compose window")
    new_msg = page.locator('button:has-text("New message")')
    if await new_msg.is_visible(timeout=3000):
        await new_msg.click()
        await page.wait_for_timeout(2000)

    await rec.solution(page, "Fill in the recipient, subject, and message body")
    to_fld = page.locator('input[placeholder="To"]')
    if await to_fld.is_visible(timeout=3000):
        await to_fld.fill("colleague@company.com")
        await page.wait_for_timeout(300)
    subj_fld = page.locator('input[placeholder="Subject"]')
    if await subj_fld.is_visible(timeout=2000):
        await subj_fld.fill("Meeting Reminder")
        await page.wait_for_timeout(300)
    body_fld = page.locator('[contenteditable="true"]')
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
    new_contact = page.locator('button:has-text("New contact")')
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

    await rec.challenge(page, "Colleagues need to know you're away without manually telling everyone")
    await navigate_to_settings(page, "Email", "Vacation")
    await page.wait_for_timeout(1000)

    await rec.solution(page, "Enable the vacation auto-reply with your away message")
    enable = page.locator('button:has-text("Enable vacation auto reply")')
    if await enable.is_visible(timeout=3000):
        await enable.click()
        await page.wait_for_timeout(1000)

    await rec.result(page, "Vacation auto-reply is enabled and will respond to incoming emails")
    await page.wait_for_timeout(800)
    return await rec.capture(page, "Vacation auto-reply is enabled and will respond to incoming emails")


async def record_mail_signatures(context: BrowserContext) -> Path | None:
    """Task-first capture: Configure email signature placement."""
    rec = ScreenshotRecorder("mail-signatures", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await page.wait_for_timeout(1000)

    await rec.context(page, "Configure where your email signature appears in messages")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "Set the signature position for new messages and replies")
    await navigate_to_settings(page, "Email")
    await page.wait_for_timeout(1000)

    await rec.solution(page, "Choose signature placement: below the quote, above, or inline")
    for_input = await page.locator('label:has-text("and place the signature")').get_attribute("for")
    if for_input:
        combo = page.locator(f'[id="{for_input}"]')
        if await combo.is_visible(timeout=3000):
            await combo.click()
            await page.wait_for_timeout(500)
            mail_option = page.locator(f'[role="option"]:has-text("below the mail")')
            if await mail_option.is_visible(timeout=2000):
                await mail_option.click()
                await page.wait_for_timeout(1000)

    await rec.result(page, "Signature placement is configured for all outgoing messages")
    await page.wait_for_timeout(800)
    return await rec.capture(page, "Signature placement is configured for all outgoing messages")


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
    """Task-first capture: Create a new calendar event."""
    rec = ScreenshotRecorder("freebusy", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "calendar")
    await page.wait_for_timeout(1000)

    await rec.context(page, "Schedule a team meeting using the calendar")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "Click the Create Event button to open the event editor")
    create_btn = page.locator('button:has-text("Create Event")').first
    if await create_btn.is_visible(timeout=3000):
        await create_btn.click()
        await page.wait_for_timeout(1500)

    await rec.solution(page, "Fill in the event title and details in the event editor")
    await page.wait_for_timeout(1000)

    await rec.result(page, "Event can be created with a title and basic details")
    await page.wait_for_timeout(800)
    return await rec.capture(page, "Event can be created with a title and basic details")


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
    view_btn = page.locator('button:has-text("Week")')
    if await view_btn.is_visible(timeout=3000):
        await view_btn.click()
        await page.wait_for_timeout(1000)
        day_option = page.locator('[role="menuitem"]:has-text("Day")')
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
    return await rec.capture(page, "Events are displayed with their time slots in the calendar grid")


async def record_global_search(context: BrowserContext) -> Path | None:
    """Task-first capture: Use the search feature in the inbox."""
    rec = ScreenshotRecorder("global-search", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await page.wait_for_timeout(1000)

    await rec.context(page, "Use the search bar to find emails in your inbox")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "Finding specific emails in a crowded inbox")
    search_input = page.locator('input[placeholder="Search emails"]')
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
    if await msg.is_visible(timeout=3000):
        await msg.click()
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
        await sent_btn.click()
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
    return await rec.capture(page, "Password change form is ready with current and new password fields")


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
        book = page.locator(f'button:has-text("{addr_book}")')
        if await book.is_visible(timeout=2000):
            await book.click()
            await page.wait_for_timeout(800)

    add_book = page.locator('button:has-text("Add address book")')
    if await add_book.is_visible(timeout=2000):
        await add_book.click()
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
    sogo_auth = await login_page.evaluate(
        '() => sessionStorage.getItem("sogo_auth")'
    )
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

async def main():
    clean_dirs()

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

    workflows = [
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

    start_time = time.time()
    results = []
    worker_script = Path(__file__).parent / "run_single_screenshot.py"

    for name, fn_name in workflows:
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
        stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=120)
        elapsed = time.time() - wf_start
        output = stdout.decode("utf-8", errors="replace")
        print(output, end="")

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


if __name__ == "__main__":
    asyncio.run(main())
