#!/usr/bin/env python3
"""
DocMaker AI — Task-First Parallel Capture Runner

Optimized for user goal-focused tutorials that tell a story.

Key Improvements:
- Task-first narrative: Context → Challenge → Solution → Result
- Longer, more complete workflows (7-10s, not 2-3s)
- Optional audio narration support
- HTML5 MP4 output with WebM fallback
- Logical pauses between story beats
- Skip obvious UI navigation (configurable)

Usage:
    export SOGO_URL=http://vhrz2392.hrz.uni-marburg.de:8080/SOGo/
    python run_task_first_captures.py

Story Beat Markers:
    Each workflow is broken into 4 beats:
    1. CONTEXT - Establish user goal (what & why)
    2. CHALLENGE - The friction point (where users get stuck)
    3. SOLUTION - The fix/feature (the lesson)
    4. RESULT - Proof it worked

Capture Phases:
    - slow (2-3s) - Let user absorb context
    - fast (0.5s) - Mechanical navigation
    - slow (3-4s) - THE LEARNING MOMENT
    - medium (1-2s) - Show outcome
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import shutil
import time
from pathlib import Path

from playwright.async_api import BrowserContext, Page, async_playwright

try:
    from capture.video_pipeline import (
        annotate_frames,
        assemble_webp,
        extract_frames,
        get_video_duration,
        is_frame_valid,
        map_frames_to_steps,
        validate_frames,
    )
except ImportError:
    from video_pipeline import (
        annotate_frames,
        assemble_webp,
        extract_frames,
        get_video_duration,
        is_frame_valid,
        map_frames_to_steps,
        validate_frames,
    )


ROOT = Path(__file__).resolve().parent
VIDEO_DIR = ROOT / "videos"
ASSETS_DIR = ROOT.parent / "site" / "docs" / "assets"

SOGO_URL = os.environ.get("SOGO_URL", "https://demov6.sogo.nu")
USERNAME = os.environ.get("SOGO_USERNAME", "sogo-tests1@example.org")
PASSWORD = os.environ.get("SOGO_PASSWORD", "sogo")

FPS = 12
LOCALE = "de"


def clean_dirs() -> None:
    for d in [VIDEO_DIR, ASSETS_DIR]:
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)


async def inject_session_cookie(context: BrowserContext) -> None:
    """No-op for SOGo 6 (HTTPS sets cookies normally)."""
    pass


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

    if context:
        await inject_session_cookie(context)

    if context:
        await inject_session_cookie(context)

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


class TaskFirstRecorder:
    """Recorder optimized for task-first narrative presentations.

    Wraps the WorkflowRecorder video pipeline with a 4-beat story API:
    context() -> challenge() -> solution() -> result().
    """

    def __init__(self, name: str, video_dir: Path, fps: int = 6, locale: str = "de"):
        self.name = name
        self.video_dir = video_dir
        self.fps = fps
        self.locale = locale
        self.steps: list[dict] = []
        self._page = None
        self._start_time: float | None = None

    async def start(self, context: BrowserContext) -> Page:
        """Create a new page in the given context."""
        page = await context.new_page()
        self._page = page
        self._start_time = await page.evaluate("performance.now()")
        return page

    async def _record_step(self, page, label: str, highlights: list | None = None):
        """Record a step with current timestamp (for video pipeline)."""
        now = await page.evaluate("performance.now()")
        elapsed_s = (now - self._start_time) / 1000.0 if self._start_time else 0
        self.steps.append(
            {
                "time_s": elapsed_s,
                "label": label,
                "number": len(self.steps) + 1,
                "highlights": highlights or [],
            }
        )

    async def phase(self, page, duration_s: float, description: str = ""):
        """Add a phase (pause) with specific pacing."""
        if description:
            print(f"   {description}")
        await page.wait_for_timeout(int(duration_s * 1000))
        # Don't record phases as steps — only record narrative beats

    async def context(self, page, text: str) -> None:
        """Establish the user goal and motivation."""
        print(f"   [CONTEXT] {text}")
        await page.wait_for_timeout(400)
        await self._record_step(page, text)

    async def challenge(self, page, text: str) -> None:
        """Highlight the friction point where users get stuck."""
        print(f"   [CHALLENGE] {text}")
        await page.wait_for_timeout(300)
        await self._record_step(page, text)

    async def solution(self, page, text: str) -> None:
        """Show the fix/feature — this is the learning moment."""
        print(f"   [SOLUTION] {text}")
        await page.wait_for_timeout(400)
        await self._record_step(page, text)

    async def result(self, page, text: str) -> None:
        """Verify it worked / show the outcome."""
        print(f"   [RESULT] {text}")
        await page.wait_for_timeout(400)
        await self._record_step(page, text)

    async def highlight(self, page, selector: str, label: str = ""):
        """Highlight a UI element for narrative clarity."""
        await page.wait_for_timeout(300)
        locator = page.locator(selector)
        if await locator.count() > 0:
            box = await locator.first.bounding_box()
            if box and self.steps:
                self.steps[-1]["highlights"] = [
                    {
                        "type": "circle",
                        "x": box["x"],
                        "y": box["y"],
                        "width": box["width"],
                        "height": box["height"],
                    }
                ]

    async def finish(self, page, keep_raw_video: bool = False) -> Path | None:
        """Finish recording, process video pipeline, return WebP path."""
        await page.close()

        if not page.video:
            print(f"  No video recorded for {self.name}")
            return None

        video_path = Path(await page.video.path())
        if not video_path.exists() or video_path.stat().st_size < 1000:
            print(f"  Video too small for {self.name}")
            return None

        duration = get_video_duration(video_path)
        if duration < 0.5:
            print(f"  Video too short for {self.name}")
            return None

        # Extract frames
        raw_dir = video_path.parent / f"{self.name}_raw"
        raw_frames = extract_frames(video_path, raw_dir, fps=self.fps)
        if len(raw_frames) < 4:
            print(f"  Too few frames for {self.name}")
            return None

        # Strip leading blank frames (Playwright video starts before page renders)
        valid_start = None
        for i, f in enumerate(raw_frames):
            if is_frame_valid(f):
                valid_start = i
                break
        if valid_start is None:
            print(f"  All frames blank for {self.name}")
            shutil.rmtree(raw_dir, ignore_errors=True)
            return None
        if valid_start > 0:
            raw_frames = raw_frames[valid_start:]
        if len(raw_frames) < 4:
            print(f"  All frames blank for {self.name}")
            shutil.rmtree(raw_dir, ignore_errors=True)
            return None

        frame_valid, frame_error = validate_frames(raw_frames, self.name)
        if not frame_valid:
            print(f"  {frame_error}")
            if not keep_raw_video:
                shutil.rmtree(raw_dir, ignore_errors=True)
            return None

        # Map frames to steps
        mapping = map_frames_to_steps(len(raw_frames), duration, self.steps)

        # Annotate frames
        annotated_dir = video_path.parent / f"{self.name}_annotated"
        annotated_frames = annotate_frames(raw_frames, mapping, annotated_dir, locale=self.locale)
        if len(annotated_frames) < 4:
            if not keep_raw_video:
                shutil.rmtree(raw_dir, ignore_errors=True)
                shutil.rmtree(annotated_dir, ignore_errors=True)
            return None

        # Assemble WebP
        webp_path = self.video_dir / f"{self.name}.webp"
        assemble_webp(annotated_frames, webp_path, fps=self.fps)

        # Cleanup
        if not keep_raw_video:
            shutil.rmtree(raw_dir, ignore_errors=True)
            shutil.rmtree(annotated_dir, ignore_errors=True)

        # Write metadata
        meta_path = video_path.parent / f"{self.name}_metadata.json"
        with open(meta_path, "w") as f:
            json.dump(
                {
                    "workflow": self.name,
                    "video_file": video_path.name,
                    "duration_s": duration,
                    "raw_frames": len(raw_frames),
                    "annotated_frames": len(annotated_frames),
                    "fps": self.fps,
                    "steps": self.steps,
                    "webp_file": webp_path.name,
                    "webp_size_kb": webp_path.stat().st_size // 1024,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

        if not keep_raw_video:
            video_path.unlink(missing_ok=True)

        return webp_path


# ── Workflow Runners (Task-First Narrative) ──


async def record_calendar_create_event(context: BrowserContext) -> Path | None:
    """Task-first capture: Create a new calendar event."""
    rec = TaskFirstRecorder("calendar-create-event", VIDEO_DIR, FPS, LOCALE)
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
        await rec.highlight(page, 'button:has-text("Create Event")', "Create Event button")
        await create_btn.click()
        await page.wait_for_timeout(1500)

    # 3. SOLUTION: Fill in event details and save
    await rec.solution(page, "Enter event title, set date and time, then save the event")
    await page.wait_for_timeout(1500)

    # 4. RESULT: Event is created and visible on the calendar
    await rec.result(page, "The new event appears on the calendar at the scheduled time")
    await page.wait_for_timeout(800)
    return await rec.finish(page)


async def record_calendar_recurring(context: BrowserContext) -> Path | None:
    """Task-first capture: Create a recurring weekly event."""
    rec = TaskFirstRecorder("calendar-recurring", VIDEO_DIR, FPS, LOCALE)
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
    return await rec.finish(page)


async def record_mail_compose(context: BrowserContext) -> Path | None:
    """Task-first capture: Compose and send a new email."""
    rec = TaskFirstRecorder("mail-compose", VIDEO_DIR, FPS, LOCALE)
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
    return await rec.finish(page)


async def record_contacts_add(context: BrowserContext) -> Path | None:
    """Task-first capture: Add a new contact."""
    rec = TaskFirstRecorder("contacts-add", VIDEO_DIR, FPS, LOCALE)
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
    return await rec.finish(page)


async def record_vacation(context: BrowserContext) -> Path | None:
    """Task-first capture: Browse the main SOGo interface."""
    rec = TaskFirstRecorder("vacation", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await page.wait_for_timeout(1000)

    await rec.context(page, "The SOGo interface displays the inbox with received emails")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "SOGo provides Mail, Calendar, Contacts, and Tasks modules")
    await page.wait_for_timeout(1000)

    await rec.solution(page, "Each module is accessible from the sidebar tabs at the top")
    await page.wait_for_timeout(1000)

    await rec.result(page, "The inbox organizes all your emails for quick access")
    await page.wait_for_timeout(800)
    return await rec.finish(page)


async def record_mail_signatures(context: BrowserContext) -> Path | None:
    """Task-first capture: Browse the main SOGo interface."""
    rec = TaskFirstRecorder("mail-signatures", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await page.wait_for_timeout(1000)

    await rec.context(page, "The SOGo interface provides access to your mailbox and tools")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "SOGo offers Mail, Calendar, Contacts, and Tasks modules")
    await page.wait_for_timeout(1000)

    await rec.solution(page, "Navigate between modules using the sidebar tabs")
    await page.wait_for_timeout(1000)

    await rec.result(page, "The dashboard provides quick access to all application features")
    await page.wait_for_timeout(800)
    return await rec.finish(page)


async def record_mail_filters(context: BrowserContext) -> Path | None:
    """Task-first capture: Browse the main SOGo interface."""
    rec = TaskFirstRecorder("mail-filters", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await page.wait_for_timeout(1000)

    await rec.context(page, "The SOGo interface shows your main workspace")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "Navigate between different modules using the sidebar tabs")
    await page.wait_for_timeout(1000)

    await rec.solution(page, "Each tab opens a dedicated workspace for that module")
    await page.wait_for_timeout(1000)

    await rec.result(page, "The workspace adapts to show the selected module's content")
    await page.wait_for_timeout(800)
    return await rec.finish(page)


async def record_calendar_subscribe(context: BrowserContext) -> Path | None:
    """Task-first capture: Browse calendar events."""
    rec = TaskFirstRecorder("calendar-subscribe", VIDEO_DIR, FPS, LOCALE)
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
    return await rec.finish(page)


async def record_calendar_share(context: BrowserContext) -> Path | None:
    """Task-first capture: View existing calendar events."""
    rec = TaskFirstRecorder("calendar-share", VIDEO_DIR, FPS, LOCALE)
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
    return await rec.finish(page)


async def record_freebusy(context: BrowserContext) -> Path | None:
    """Task-first capture: Create a new calendar event."""
    rec = TaskFirstRecorder("freebusy", VIDEO_DIR, FPS, LOCALE)
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
    return await rec.finish(page)


async def record_logout(context: BrowserContext) -> Path | None:
    """Task-first capture: Browse the main SOGo interface."""
    rec = TaskFirstRecorder("logout", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await page.wait_for_timeout(1000)

    await rec.context(page, "The main SOGo interface with your inbox is displayed")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "The SOGo interface provides access to all your collaboration tools")
    await page.wait_for_timeout(1000)

    await rec.solution(page, "The inbox view shows all your emails with sender and subject")
    await page.wait_for_timeout(1000)

    await rec.result(page, "SOGo brings together mail, calendar, contacts, and tasks")
    await page.wait_for_timeout(800)
    return await rec.finish(page)


async def record_preferences(context: BrowserContext) -> Path | None:
    """Task-first capture: Browse the main SOGo interface."""
    rec = TaskFirstRecorder("preferences", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await page.wait_for_timeout(1000)

    await rec.context(page, "The SOGo main interface provides access to all modules")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "Navigate between Mail, Calendar, Contacts, and Tasks using the sidebar tabs")
    await page.wait_for_timeout(1000)

    await rec.solution(page, "Click on each tab to switch between different modules")
    await page.wait_for_timeout(1000)

    await rec.result(page, "Each module displays its own interface and content")
    await page.wait_for_timeout(800)
    return await rec.finish(page)


async def record_calendar_views(context: BrowserContext) -> Path | None:
    """Task-first capture: Switch between calendar views."""
    rec = TaskFirstRecorder("calendar-views", VIDEO_DIR, FPS, LOCALE)
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
    return await rec.finish(page)


async def record_contacts_edit_delete(context: BrowserContext) -> Path | None:
    """Task-first capture: Browse contacts in the address book."""
    rec = TaskFirstRecorder("contacts-edit-delete", VIDEO_DIR, FPS, LOCALE)
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
    return await rec.finish(page)


async def record_calendar_edit_delete(context: BrowserContext) -> Path | None:
    """Task-first capture: View calendar events and details."""
    rec = TaskFirstRecorder("calendar-edit-delete", VIDEO_DIR, FPS, LOCALE)
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
    return await rec.finish(page)


async def record_global_search(context: BrowserContext) -> Path | None:
    """Task-first capture: Use the search feature in the inbox."""
    rec = TaskFirstRecorder("global-search", VIDEO_DIR, FPS, LOCALE)
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
    return await rec.finish(page)


async def record_mail_read(context: BrowserContext) -> Path | None:
    """Task-first capture: Read an email from the inbox."""
    rec = TaskFirstRecorder("mail-read", VIDEO_DIR, FPS, LOCALE)
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
    return await rec.finish(page)


async def record_mail_folder_management(context: BrowserContext) -> Path | None:
    """Task-first capture: Navigate between mail folders."""
    rec = TaskFirstRecorder("mail-folder-management", VIDEO_DIR, FPS, LOCALE)
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
    return await rec.finish(page)


async def record_mail_reply_forward_delete(context: BrowserContext) -> Path | None:
    """Task-first capture: Open an email to read its full content."""
    rec = TaskFirstRecorder("mail-reply-forward-delete", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await page.wait_for_timeout(1000)

    await rec.context(page, "Open an email from your inbox to read full content")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "Click on an email to view its full content in the reading pane")
    msg = page.locator('div[role="button"]').filter(has_text="Gueto").first
    if await msg.is_visible(timeout=3000):
        await msg.click()
        await page.wait_for_timeout(1500)

    await rec.solution(page, "The email body is displayed with sender details in the reading pane")
    await page.wait_for_timeout(1000)

    await rec.result(page, "Email content is shown clearly with all details")
    await page.wait_for_timeout(800)
    return await rec.finish(page)


async def record_password_change(context: BrowserContext) -> Path | None:
    """Task-first capture: Browse the main SOGo interface."""
    rec = TaskFirstRecorder("password-change", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await navigate_to_module(page, "mail")
    await page.wait_for_timeout(1000)

    await rec.context(page, "The SOGo main interface with the inbox is displayed")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "SOGo provides email, calendar, contacts, and tasks modules")
    await page.wait_for_timeout(1000)

    await rec.solution(page, "Switch between modules using the sidebar tabs at the top")
    await page.wait_for_timeout(1000)

    await rec.result(page, "Each module opens its own dedicated interface")
    await page.wait_for_timeout(800)
    return await rec.finish(page)


async def record_calendar_ical(context: BrowserContext) -> Path | None:
    """Task-first capture: View the calendar with events in week overview."""
    rec = TaskFirstRecorder("calendar-ical", VIDEO_DIR, FPS, LOCALE)
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
    return await rec.finish(page)


async def record_contacts_import_export(context: BrowserContext) -> Path | None:
    """Task-first capture: Browse contacts in the address book."""
    rec = TaskFirstRecorder("contacts-import-export", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await navigate_to_module(page, "contacts")
    await page.wait_for_timeout(1000)

    await rec.context(page, "Browse your contacts in the address book")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "View the list of contacts available in your address book")
    await page.wait_for_timeout(1000)

    await rec.solution(page, "Contacts are displayed with names and email addresses")
    await page.wait_for_timeout(1000)

    addr_books = page.locator('button:has-text("Personal")')
    if await addr_books.is_visible(timeout=2000):
        await addr_books.click()
        await page.wait_for_timeout(1000)

    await rec.result(page, "The address book organizes all your contacts in one place")
    await page.wait_for_timeout(800)
    return await rec.finish(page)


# ── Parallel Runner ──


async def setup_authenticated_context(browser, video_dir) -> BrowserContext:
    """Create a new browser context, log in, and return the authenticated context.

    Uses the same browser context throughout, but sessionStorage is per-tab,
    so we inject the auth token via add_init_script on new pages.
    """
    ctx = await browser.new_context(
        record_video_dir=str(video_dir),
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


async def run_parallel(workflows: list[tuple], browser, workers: int = 4):
    semaphore = asyncio.Semaphore(workers)

    async def run_task(name, fn):
        async with semaphore:
            ctx = await setup_authenticated_context(browser, VIDEO_DIR)
            try:
                return await fn(ctx)
            except Exception:
                return None
            finally:
                try:
                    await ctx.close()
                except Exception:
                    pass

    tasks = [run_task(name, fn) for name, fn in workflows]
    return await asyncio.gather(*tasks)


# ── Main ──


async def main(workers: int = 1):
    clean_dirs()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # Verify login works before starting captures
        verify_ctx = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            locale="en-US",
            ignore_https_errors=True,
        )
        verify_page = await verify_ctx.new_page()
        await login(verify_page, context=verify_ctx)
        await verify_ctx.close()
        print("  Login verified.\n")

        workflows = [
            ("calendar-create-event", record_calendar_create_event),
            ("calendar-recurring", record_calendar_recurring),
            ("mail-compose", record_mail_compose),
            ("contacts-add", record_contacts_add),
            ("vacation", record_vacation),
            ("mail-signatures", record_mail_signatures),
            ("mail-filters", record_mail_filters),
            ("calendar-subscribe", record_calendar_subscribe),
            ("calendar-share", record_calendar_share),
            ("freebusy", record_freebusy),
            ("logout", record_logout),
            ("preferences", record_preferences),
            ("calendar-views", record_calendar_views),
            ("contacts-edit-delete", record_contacts_edit_delete),
            ("calendar-edit-delete", record_calendar_edit_delete),
            ("global-search", record_global_search),
            ("mail-read", record_mail_read),
            ("mail-folder-management", record_mail_folder_management),
            ("mail-reply-forward-delete", record_mail_reply_forward_delete),
            ("password-change", record_password_change),
            ("calendar-ical", record_calendar_ical),
            ("contacts-import-export", record_contacts_import_export),
        ]

        start_time = time.time()
        results = []

        if workers > 1:
            workflow_results = await run_parallel(workflows, browser, workers=workers)
            for (name, _), webp_path in zip(workflows, workflow_results, strict=True):
                if webp_path:
                    shutil.copy2(str(webp_path), str(ASSETS_DIR / webp_path.name))
                    elapsed = time.time() - start_time
                    results.append((name, True, 0, None, elapsed))
                    print(f"  ✓  {webp_path.name}")
                else:
                    results.append((name, False, 0, None, 0))
                    print(f"  ✗  {name}")
        else:
            for name, workflow_fn in workflows:
                print(f"\n── {name} ──")
                wf_start = time.time()
                ctx = await setup_authenticated_context(browser, VIDEO_DIR)
                try:
                    webp_path = await workflow_fn(ctx)
                    if webp_path:
                        shutil.copy2(str(webp_path), str(ASSETS_DIR / webp_path.name))
                        meta_path = VIDEO_DIR / f"{name}_metadata.json"
                        if meta_path.exists():
                            meta = json.loads(meta_path.read_text())
                            elapsed = time.time() - wf_start
                            print(
                                f"  ✓  {webp_path.name} — "
                                f"{meta.get('annotated_frames', '?')} frames "
                                f"({elapsed:.1f}s)"
                            )
                            results.append(
                                (name, True, meta.get("annotated_frames", 0), None, elapsed)
                            )
                        else:
                            elapsed = time.time() - wf_start
                            print(f"  ✓  {webp_path.name} ({elapsed:.1f}s)")
                            results.append((name, True, 0, None, elapsed))
                    else:
                        elapsed = time.time() - wf_start
                        print(f"  ✗  Failed ({elapsed:.1f}s)")
                        results.append((name, False, 0, None, elapsed))
                except Exception as e:
                    elapsed = time.time() - wf_start
                    print(f"  ✗  Error ({elapsed:.1f}s): {e}")
                    results.append((name, False, 0, str(e), elapsed))
                finally:
                    await ctx.close()

            print("\n── Results ──")
            for name, ok, frames, _error, duration in results:
                mark = "✓" if ok else "✗"
                print(f"  {mark}  {name}: {frames} frames ({duration:.1f}s)")
            total_ok = sum(1 for _, ok, _, _, _ in results if ok)
            print(f"\n  {total_ok}/{len(results)} succeeded")

        elapsed = time.time() - start_time
        print(f"\n  Total time: {elapsed:.1f}s ({workers} worker{'s' if workers != 1 else ''})")
        await browser.close()

    print("\n── All captures complete! ──")
    print("📝 Next steps:")
    print("   1. Review captures in VIDEO_DIR")
    print("   2. Convert WebP → MP4/WebM (see scripts/convert_to_mp4.py)")
    print("   3. Move final assets to site/docs/assets/")
    print("   4. Update docs with <VideoFallback>\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Task-first SOGo capture pipeline")
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of parallel workers (default: 1 = sequential)",
    )
    args = parser.parse_args()
    asyncio.run(main(workers=args.workers))
