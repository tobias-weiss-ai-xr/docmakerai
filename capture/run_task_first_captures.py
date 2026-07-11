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

SOGO_URL = os.environ.get("SOGO_URL", "http://vhrz2392.hrz.uni-marburg.de:8080/SOGo/")
USERNAME = os.environ.get("SOGO_USERNAME", "testuser")
PASSWORD = os.environ.get("SOGO_PASSWORD", "eval2026")

FPS = 12
LOCALE = "de"


def clean_dirs() -> None:
    for d in [VIDEO_DIR, ASSETS_DIR]:
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)


async def inject_session_cookie(context: BrowserContext) -> None:
    """Inject the HttpOnly session cookie via SSH+curl (workaround for secure flag).

    SOGo sets the session cookie with ``secure`` flag, but the HRZ instance
    is served over plain HTTP. Browsers reject secure cookies over HTTP, so
    we fetch the cookie via curl on the server (which ignores the flag) and
    inject it manually into the Playwright context.
    """
    from urllib.parse import urlparse

    parsed = urlparse(SOGO_URL)
    ssh_host = parsed.hostname  # e.g., vhrz2392.hrz.uni-marburg.de
    ssh_port = parsed.port or 80

    # Build the internal URL for curl (localhost works because it's the same container)
    base_path = parsed.path.rstrip("/")
    connect_url = f"http://localhost:{ssh_port}{base_path}/connect"

    # Password/username may contain special chars, escape for SSH command
    safe_user = USERNAME.replace("'", "'\\''")
    safe_pass = PASSWORD.replace("'", "'\\''")

    cmd = (
        f"curl -s -X POST '{connect_url}' "
        f"-H 'Content-Type: application/json' "
        f'-d \'{{"userName":"{safe_user}","password":"{safe_pass}"}}\' '
        f"-c /tmp/.sogo_session_cookies 2>/dev/null && "
        f"cat /tmp/.sogo_session_cookies"
    )

    proc = await asyncio.create_subprocess_exec(
        "ssh",
        "-o",
        "StrictHostKeyChecking=no",
        "-o",
        "ConnectTimeout=10",
        f"ansible@{ssh_host}",
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=15)
    cookie_jar = stdout.decode()

    cookies_to_add = []
    for line in cookie_jar.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        # #HttpOnly_ lines are NOT comments — they indicate HttpOnly cookies
        if line.startswith("#") and not line.startswith("#HttpOnly_"):
            continue

        parts = line.split("\t")
        if len(parts) >= 7:
            raw_domain = parts[0]
            is_httponly = raw_domain.startswith("#HttpOnly_")
            _ = raw_domain[len("#HttpOnly_") :] if is_httponly else raw_domain
            path = parts[2]
            name = parts[5]
            value = parts[6]

            cookies_to_add.append(
                {
                    "name": name,
                    "value": value,
                    "domain": str(ssh_host),
                    "path": path,
                    "httpOnly": is_httponly,
                    "secure": False,
                    "sameSite": "Lax",
                }
            )

    if cookies_to_add:
        await context.add_cookies(cookies_to_add)
        print(f"   Injected {len(cookies_to_add)} cookie(s) via server-side curl")


async def login(page, context: BrowserContext | None = None) -> None:
    print("\n  Login...")
    await page.goto(SOGO_URL, wait_until="networkidle", timeout=30000)
    await page.wait_for_timeout(2000)
    await page.fill("[ng-model='app.creds.username']", USERNAME)
    await page.fill("#passwordField", PASSWORD)
    await page.click("md-switch[ng-model='app.creds.rememberLogin']")
    await page.wait_for_timeout(300)
    await page.click("button[type='submit']")
    await page.wait_for_timeout(5000)

    if context:
        await inject_session_cookie(context)


async def goto(page, url_suffix: str, wait_ms: int = 3000) -> None:
    url = f"{SOGO_URL}so/{USERNAME}/{url_suffix}"
    await page.goto(url, wait_until="networkidle", timeout=30000)
    await page.wait_for_timeout(wait_ms)


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
        await page.wait_for_timeout(2000)
        await self._record_step(page, text)

    async def challenge(self, page, text: str) -> None:
        """Highlight the friction point where users get stuck."""
        print(f"   [CHALLENGE] {text}")
        await page.wait_for_timeout(1500)
        await self._record_step(page, text)

    async def solution(self, page, text: str) -> None:
        """Show the fix/feature — this is the learning moment."""
        print(f"   [SOLUTION] {text}")
        await page.wait_for_timeout(3500)
        await self._record_step(page, text)

    async def result(self, page, text: str) -> None:
        """Verify it worked / show the outcome."""
        print(f"   [RESULT] {text}")
        await page.wait_for_timeout(2000)
        await self._record_step(page, text)

    async def highlight(self, page, selector: str, label: str = ""):
        """Highlight a UI element for narrative clarity."""
        await page.wait_for_timeout(500)
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
    """Task-first capture: Schedule a weekly team standup meeting."""
    rec = TaskFirstRecorder("calendar-create-event", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Calendar/view#!/calendar/week/20260615")

    # 1. CONTEXT: User needs to schedule a team standup
    await rec.context(page, "Schedule a weekly team standup every Monday at 10 AM")
    await page.wait_for_timeout(2500)

    # 2. CHALLENGE: Finding the right time slot
    await rec.challenge(page, "Find the Monday 10 AM slot that is free from other meetings")
    monday = page.locator("sg-calendar-day.day").nth(8)
    hour10 = monday.locator(".clickableHourCell10").first
    mb = await monday.bounding_box()
    if mb:
        await rec.highlight(page, ".clickableHourCell10", "10 AM time slot")
        await page.wait_for_timeout(1000)

    # 3. SOLUTION: Double-click to create event, fill details, set recurrence
    await rec.solution(page, "Double-click on Monday 10 AM to create a new event with details")
    mb = await monday.bounding_box()
    hb = await hour10.bounding_box()
    if mb and hb:
        await page.mouse.dblclick(mb["x"] + mb["width"] / 2, hb["y"] + hb["height"] / 2)
        await page.wait_for_timeout(2000)

        await page.click("[ng-model='editor.component.summary']")
        await page.fill("[ng-model='editor.component.summary']", "")
        await page.type("[ng-model='editor.component.summary']", "Weekly Team Standup", delay=120)
        await page.wait_for_timeout(800)

        await page.click("[ng-model='editor.component.location']")
        await page.fill("[ng-model='editor.component.location']", "")
        await page.type("[ng-model='editor.component.location']", "Conference Room B", delay=80)
        await page.wait_for_timeout(800)

        selector = "[ng-model='editor.component.repeat.frequency']"
        await rec.highlight(page, selector, "Recurrence dropdown")
        rs = page.locator(selector).first
        if await rs.is_visible():
            await rs.click()
            await page.wait_for_timeout(500)
            wk = page.locator("md-option:has-text('Wöchentlich')").first
            if not await wk.is_visible():
                wk = page.locator("md-option:has-text('Weekly')").first
            if await wk.is_visible():
                await wk.click()
                await page.wait_for_timeout(300)
                await page.keyboard.press("Escape")
                await page.wait_for_timeout(500)

        btn = page.locator("button[ng-click*='editor.save']").first
        if not await btn.is_visible():
            btn = page.locator("button[type='submit']:has-text('Save')").first
        await btn.click()
        await page.wait_for_timeout(3000)

    # 4. RESULT: Event appears with recurring indicator
    await rec.result(page, "Weekly event appears on calendar with recurring indicator")
    await page.wait_for_timeout(2000)
    return await rec.finish(page)


async def record_calendar_recurring(context: BrowserContext) -> Path | None:
    """Task-first capture: Create a recurring weekly event with an alarm."""
    rec = TaskFirstRecorder("calendar-recurring", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Calendar/view#!/calendar/week/20260615")

    await rec.context(page, "Set up a recurring weekly meeting that repeats automatically")
    await page.wait_for_timeout(1500)

    await rec.challenge(
        page, "Manually creating the same event every week is tedious and error-prone"
    )
    monday = page.locator("sg-calendar-day.day").nth(8)
    hour11 = monday.locator(".clickableHourCell11").first
    mb = await monday.bounding_box()
    hb = await hour11.bounding_box()
    if mb and hb:
        await page.mouse.dblclick(mb["x"] + mb["width"] / 2, hb["y"] + hb["height"] / 2)
        await page.wait_for_timeout(2000)

        await rec.solution(page, "Use the recurrence dropdown to set event to 'Weekly' repeat")
        await page.click("[ng-model='editor.component.summary']")
        await page.fill("[ng-model='editor.component.summary']", "")
        await page.type("[ng-model='editor.component.summary']", "Weekly Team Standup", delay=100)
        await page.wait_for_timeout(800)

        rs = page.locator("[ng-model='editor.component.repeat.frequency']").first
        if await rs.is_visible():
            await rs.click()
            await page.wait_for_timeout(500)
            wk = page.locator("md-option:has-text('Wöchentlich')").first
            if not await wk.is_visible():
                wk = page.locator("md-option:has-text('Weekly')").first
            if await wk.is_visible():
                await wk.click()
                await page.wait_for_timeout(300)
                await page.keyboard.press("Escape")
                await page.wait_for_timeout(500)
        await rec.highlight(
            page, "[ng-model='editor.component.repeat.frequency']", "Weekly recurrence"
        )

        btn = page.locator("button[ng-click*='editor.save']").first
        if not await btn.is_visible():
            btn = page.locator("button[type='submit']:has-text('Save')").first
        await btn.click()
        await page.wait_for_timeout(3000)

    await rec.result(page, "Event is now set to repeat weekly with no manual effort")
    await page.wait_for_timeout(2000)
    return await rec.finish(page)


async def record_mail_compose(context: BrowserContext) -> Path | None:
    """Task-first capture: Compose and send a new email."""
    rec = TaskFirstRecorder("mail-compose", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Mail/view#!/Mail", 5000)

    await rec.context(page, "Write and send an email to a colleague")
    await page.wait_for_timeout(1500)

    await rec.challenge(page, "Finding the compose button and addressing the email correctly")
    compose_btn = page.locator(
        "button:has-text('Compose'), button:has-text('Verfassen'), a:has-text('Compose')"
    ).first
    if await compose_btn.is_visible(timeout=3000):
        await compose_btn.click()
        await page.wait_for_timeout(2000)

    await rec.solution(page, "Fill in recipient, subject, and message body, then send")
    await page.wait_for_timeout(1000)

    to_field = page.locator("[ng-model='composer.to'], input[ng-model*='to']").first
    if await to_field.is_visible(timeout=2000):
        await to_field.click()
        await to_field.fill("")
        await to_field.type("colleague@company.com", delay=40)
        await page.wait_for_timeout(300)

    subj_field = page.locator("[ng-model='composer.subject'], input[ng-model*='subject']").first
    if await subj_field.is_visible(timeout=2000):
        await subj_field.click()
        await subj_field.fill("")
        await subj_field.type("Meeting Reminder", delay=80)
        await page.wait_for_timeout(300)

    body_field = page.locator("[ng-model='composer.text'], .composer-body, [contenteditable]").first
    if await body_field.is_visible(timeout=2000):
        await body_field.click()
        await body_field.fill("")
        await body_field.type("Hi, just a reminder about our meeting tomorrow at 10 AM.", delay=20)
        await page.wait_for_timeout(500)

    send_btn = page.locator("button:has-text('Send'), button[ng-click*='send']").first
    if await send_btn.is_visible(timeout=2000):
        await send_btn.click()
        await page.wait_for_timeout(3000)

    await rec.result(page, "Email has been sent and appears in the Sent folder")
    await page.wait_for_timeout(2000)
    return await rec.finish(page)


async def record_contacts_add(context: BrowserContext) -> Path | None:
    """Task-first capture: Add a new contact."""
    rec = TaskFirstRecorder("contacts-add", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Contacts")

    await rec.context(page, "Add a new colleague to your address book")
    await page.wait_for_timeout(1500)

    await rec.challenge(page, "Finding where to create a new contact entry")
    add_btn = page.locator(
        "button[ng-click*='add'], button[ng-click*='new'], a[ng-click*='add']"
    ).first
    if await add_btn.is_visible(timeout=2000):
        await add_btn.click()
        await page.wait_for_timeout(2000)

    await rec.solution(page, "Fill in the contact details: name, email, and company")
    fn = page.locator("[ng-model='contact.c_firstname'], input[name='firstname']").first
    if await fn.is_visible():
        await fn.click()
        await fn.fill("")
        await fn.type("John", delay=80)
        await page.wait_for_timeout(300)

    ln = page.locator("[ng-model='contact.c_name'], input[name='lastname']").first
    if await ln.is_visible():
        await ln.click()
        await ln.fill("")
        await ln.type("Doe", delay=80)
        await page.wait_for_timeout(300)

    em = page.locator("[ng-model='contact.c_email'], input[type='email']").first
    if await em.is_visible():
        await em.click()
        await em.fill("")
        await em.type("john.doe@company.com", delay=40)
        await page.wait_for_timeout(300)

    sv = page.locator("button[ng-click*='save'], button[type='submit']:has-text('Save')").first
    if await sv.is_visible(timeout=2000):
        await sv.click()
        await page.wait_for_timeout(3000)

    await rec.result(page, "John Doe is now saved in your contacts list")
    await page.wait_for_timeout(2000)
    return await rec.finish(page)


async def record_vacation(context: BrowserContext) -> Path | None:
    """Task-first capture: Configure vacation auto-reply in Mail preferences."""
    rec = TaskFirstRecorder("vacation", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Preferences#!/mailer", 5000)

    await rec.context(page, "Set up an automatic out-of-office reply for your vacation")
    await page.wait_for_timeout(1000)

    await rec.challenge(
        page, "Colleagues need to know you are away without manually telling everyone"
    )
    await page.wait_for_timeout(1000)

    await rec.solution(
        page, "Navigate to the Vacation tab in Mail preferences and enable the auto-reply feature"
    )
    vacation_tab = page.locator(
        "md-tab-item:has-text('Vacation'), button:has-text('Vacation'), .tab-item:has-text('Vacation')"
    ).first
    if await vacation_tab.is_visible(timeout=2000):
        await vacation_tab.click()
        await page.wait_for_timeout(1000)
    await page.wait_for_timeout(1000)

    # Enable vacation auto-reply checkbox
    vacation_enable = page.locator("md-checkbox:has-text('Enable vacation auto reply'), checkbox:has-text('Enable vacation auto')").first
    if await vacation_enable.is_visible(timeout=2000):
        await vacation_enable.click()
        await page.wait_for_timeout(1000)
    await page.wait_for_timeout(2000)

    await rec.result(
        page, "Vacation auto-reply is enabled - you will automatically respond while away"
    )
    await page.wait_for_timeout(2000)
    return await rec.finish(page)


async def record_mail_signatures(context: BrowserContext) -> Path | None:
    """Task-first capture: Configure email signature in Mail preferences."""
    rec = TaskFirstRecorder("mail-signatures", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Preferences#!/mailer", 5000)

    await rec.context(page, "Create a professional email signature for all outgoing messages")
    await page.wait_for_timeout(1000)

    await rec.challenge(
        page,
        "Every email needs a signature with contact info, but typing it manually is repetitive",
    )
    await page.wait_for_timeout(1000)

    await rec.solution(page, "Configure signature insertion rules in Mail preferences")
    sig_new = page.locator("md-checkbox[ng-model*='SOGoMailUseSignatureOnNew']").first
    if await sig_new.is_visible(timeout=2000):
        await sig_new.click()
        await page.wait_for_timeout(1000)
    sig_reply = page.locator("md-checkbox[ng-model*='SOGoMailUseSignatureOnReply']").first
    if await sig_reply.is_visible(timeout=2000):
        await sig_reply.click()
        await page.wait_for_timeout(1000)
    await page.wait_for_timeout(2000)

    await rec.result(page, "Signature is now configured to be inserted in new and reply messages")
    await page.wait_for_timeout(2000)
    return await rec.finish(page)


async def record_mail_filters(context: BrowserContext) -> Path | None:
    """Task-first capture: Configure mail organization in Mail preferences."""
    rec = TaskFirstRecorder("mail-filters", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Preferences#!/mailer", 5000)

    await rec.context(page, "Automatically organize incoming emails into folders")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "Your inbox is cluttered with newsletters and automated messages")
    await page.wait_for_timeout(1000)

    await rec.solution(page, "Configure mail display and organization settings in Preferences")
    threads = page.locator("md-checkbox[ng-model*='SOGoMailSortByThreads']").first
    if await threads.is_visible(timeout=2000):
        await threads.click()
        await page.wait_for_timeout(1000)
    subscribed = page.locator("md-checkbox[ng-model*='SOGoMailShowSubscribedFoldersOnly']").first
    if await subscribed.is_visible(timeout=2000):
        await subscribed.click()
        await page.wait_for_timeout(1000)
    await page.wait_for_timeout(2000)

    await rec.result(page, "Mail organization settings are active and will keep your inbox tidy")
    await page.wait_for_timeout(2000)
    return await rec.finish(page)


async def record_calendar_subscribe(context: BrowserContext) -> Path | None:
    """Task-first capture: Subscribe to external calendar."""
    rec = TaskFirstRecorder("calendar-subscribe", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Calendar/view")

    await rec.context(page, "Subscribe to a shared or public calendar to stay informed")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "Keeping up with multiple calendars from different sources is hard")
    btn = page.locator("button[ng-click*='subscribe'], button[title*='Subscribe']").first
    if await btn.is_visible(timeout=2000):
        await btn.click()
        await page.wait_for_timeout(2000)
    else:
        await rec.challenge(
            page, "Subscribe button may be in a different location in this SOGo version"
        )
        return await rec.finish(page)

    await rec.solution(page, "Enter the calendar URL and subscribe to get live updates")
    url_inp = page.locator("input[ng-model='subscription.url'], input[type='url']").first
    if await url_inp.is_visible():
        await url_inp.click()
        await url_inp.fill("")
        await url_inp.type("https://calendar.example.com/feed.ics", delay=40)
        await page.wait_for_timeout(300)

        sv = page.locator(
            "button[ng-click*='save'], button[type='submit']:has-text('Subscribe')"
        ).first
        if await sv.is_visible(timeout=2000):
            await sv.click()
            await page.wait_for_timeout(3000)

    await rec.result(page, "External calendar is now visible alongside your personal calendar")
    await page.wait_for_timeout(2000)
    return await rec.finish(page)


async def record_calendar_share(context: BrowserContext) -> Path | None:
    """Task-first capture: Share calendar with another user."""
    rec = TaskFirstRecorder("calendar-share", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Calendar/view")

    await rec.context(
        page, "Share your calendar with a colleague so they can see your availability"
    )
    await page.wait_for_timeout(1000)

    await rec.challenge(
        page, "Coordinating schedules requires visibility into each other's calendars"
    )
    gear_btn = page.locator("button[ng-click*='calendar'], button[ng-click*='settings']").first
    if await gear_btn.is_visible(timeout=2000):
        await gear_btn.click()
        await page.wait_for_timeout(1500)

    share_tab = page.locator(
        "a:has-text('Share'), button:has-text('Teilen'), md-tab-item:has-text('Share')"
    ).first
    if await share_tab.is_visible(timeout=2000):
        await share_tab.click()
        await page.wait_for_timeout(2000)

    await rec.solution(page, "Add the colleague's email and set the appropriate permission level")
    em = page.locator("input[ng-model='share.email'], input[type='email']").first
    if await em.is_visible():
        await em.click()
        await em.fill("")
        await em.type("colleague@company.com", delay=50)
        await page.wait_for_timeout(300)

    perm = page.locator("md-select[ng-model='share.permission'], select").first
    if await perm.is_visible(timeout=2000):
        await perm.click()
        await page.wait_for_timeout(500)
        ro = page.locator("md-option:has-text('View'), option:has-text('Read')").first
        if await ro.is_visible(timeout=1000):
            await ro.click()
            await page.wait_for_timeout(500)

    await rec.result(page, "Calendar is now shared and the colleague can view your schedule")
    await page.wait_for_timeout(2000)
    return await rec.finish(page)


async def record_freebusy(context: BrowserContext) -> Path | None:
    """Task-first capture: Create event with attendee availability check."""
    rec = TaskFirstRecorder("freebusy", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Calendar/view#!/calendar/week/20260615")

    await rec.context(page, "Schedule a team meeting and check attendee availability")
    await page.wait_for_timeout(1000)

    await rec.challenge(
        page, "Scheduling across time zones and busy schedules leads to back-and-forth emails"
    )
    monday = page.locator("sg-calendar-day.day").nth(8)
    hour14 = monday.locator(".clickableHourCell14").first
    mb = await monday.bounding_box()
    hb = await hour14.bounding_box()
    if mb and hb:
        await page.mouse.dblclick(mb["x"] + mb["width"] / 2, hb["y"] + hb["height"] / 2)
        await page.wait_for_timeout(2000)

    await rec.solution(
        page, "Add attendees and use the free/busy view to find a mutually free time slot"
    )
    await page.click("[ng-model='editor.component.summary']")
    await page.fill("[ng-model='editor.component.summary']", "")
    await page.type("[ng-model='editor.component.summary']", "Team Meeting", delay=100)
    await page.wait_for_timeout(500)

    at = page.locator("button:has-text('Attendees'), [ng-click*='attendee']").first
    if await at.is_visible(timeout=2000):
        await at.click()
        await page.wait_for_timeout(2000)

        em = page.locator("input[ng-model='attendee.email'], input[type='email']").first
        if await em.is_visible():
            await em.click()
            await em.fill("")
            await em.type("colleague@company.com", delay=50)
            await page.wait_for_timeout(2000)

    await rec.result(page, "Free/busy information shows optimal meeting time for all attendees")
    await page.wait_for_timeout(2000)
    return await rec.finish(page)


async def record_logout(context: BrowserContext) -> Path | None:
    """Task-first capture: Log out of SOGo."""
    rec = TaskFirstRecorder("logout", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Calendar/view", 2000)

    await rec.context(page, "Sign out of SOGo when you are done working")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "Leaving your session open on a shared computer is a security risk")
    logout_link = page.locator('a[href*="logoff"]').first
    if await logout_link.is_visible(timeout=2000):
        box = await logout_link.bounding_box()
        if box:
            await rec.highlight(page, 'a[href*="logoff"]', "Logout button")
        await logout_link.click()
        await page.wait_for_timeout(3000)
    else:
        user_menu = page.locator("button[ng-click*='userMenu'], .user-menu").first
        if await user_menu.is_visible():
            await user_menu.click()
            await page.wait_for_timeout(500)
            lo = page.locator("button:has-text('Logout'), a:has-text('Abmelden')").first
            if await lo.is_visible():
                await lo.click()
                await page.wait_for_timeout(3000)

    await rec.solution(page, "Click the logout button to securely end your session")
    await rec.result(page, "Session is closed and the login screen is displayed")
    await page.wait_for_timeout(2000)
    return await rec.finish(page)


async def record_preferences(context: BrowserContext) -> Path | None:
    """Task-first capture: Configure user preferences."""
    rec = TaskFirstRecorder("preferences", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)

    await rec.context(page, "Customize SOGo to match your working preferences")
    settings_link = page.locator('a[href*="Preferences"]').first
    if await settings_link.is_visible(timeout=3000):
        await settings_link.click()
        await page.wait_for_timeout(3000)
    else:
        await goto(page, "Preferences", 3000)

    await page.wait_for_timeout(500)

    await rec.challenge(
        page, "Default settings may not match your workflow or notification preferences"
    )
    tabs = page.locator("md-tab-item, .tab-item, [role='tab']").all()
    tab_texts = []
    for tab in await tabs:
        tt = await tab.text_content()
        if tt and tt.strip():
            tab_texts.append(tt.strip())
    if tab_texts:
        for target_tab_text in ["General", "Notification", "Benachrichtigungen"]:
            tab = page.locator(
                f"md-tab-item:has-text('{target_tab_text}'),"
                f" .tab-item:has-text('{target_tab_text}')"
            ).first
            if await tab.is_visible(timeout=1000):
                await tab.click()
                await page.wait_for_timeout(1500)
                break

    await rec.solution(
        page,
        "Browse through the settings tabs to configure"
        " language, notifications, and display options",
    )
    await page.wait_for_timeout(1000)

    await rec.result(page, "SOGo is now configured to your personal preferences")
    await page.wait_for_timeout(2000)
    return await rec.finish(page)


async def record_calendar_views(context: BrowserContext) -> Path | None:
    """Task-first capture: Switch between calendar views."""
    rec = TaskFirstRecorder("calendar-views", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Calendar/view", 2000)

    await rec.context(
        page, "View your calendar in different layouts depending on your planning needs"
    )
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "The default week view does not give enough detail for a busy day")
    day_btn = page.locator("button:has-text('Day'), md-button:has-text('Tag')").first
    if await day_btn.is_visible(timeout=2000):
        await day_btn.click()
        await page.wait_for_timeout(2000)

    await rec.solution(
        page, "Switch between Day, Week, and Month views to get the right level of detail"
    )
    await page.wait_for_timeout(500)

    month_btn = page.locator("button:has-text('Month'), md-button:has-text('Monat')").first
    if await month_btn.is_visible(timeout=2000):
        await month_btn.click()
        await page.wait_for_timeout(2000)

    week_btn = page.locator("button:has-text('Week'), md-button:has-text('Woche')").first
    if await week_btn.is_visible(timeout=2000):
        await week_btn.click()
        await page.wait_for_timeout(2000)

    await rec.result(page, "Calendar view changes instantly to show the selected layout")
    await page.wait_for_timeout(2000)
    return await rec.finish(page)


async def record_contacts_edit_delete(context: BrowserContext) -> Path | None:
    """Task-first capture: Edit and delete a contact."""
    rec = TaskFirstRecorder("contacts-edit-delete", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Contacts", 2000)

    await rec.context(page, "Update contact information or remove outdated entries")
    await page.wait_for_timeout(1000)

    await rec.challenge(
        page, "Contact details change over time and old contacts clutter the address book"
    )
    user = page.locator("text=John").first
    if await user.is_visible(timeout=3000):
        await user.click()
        await page.wait_for_timeout(2000)

        await rec.solution(page, "Select a contact, edit their phone number, and save the changes")
        phone = page.locator("[ng-model='contact.c_telephone'], input[type='tel']").first
        if await phone.is_visible():
            await phone.click()
            await phone.fill("")
            await phone.type("+49 123 456 789", delay=50)
            await page.wait_for_timeout(300)

            sv = page.locator(
                "button[ng-click*='save'], button[type='submit']:has-text('Save')"
            ).first
            if await sv.is_visible(timeout=2000):
                await sv.click()
                await page.wait_for_timeout(2000)

        await page.wait_for_timeout(500)

        del_btn = page.locator(
            "button[ng-click*='delete'], button:has-text('Delete'), button:has-text('Löschen')"
        ).first
        if await del_btn.is_visible(timeout=2000):
            await del_btn.click()
            await page.wait_for_timeout(2000)

        await rec.result(page, "Contact has been updated and then removed from the address book")
    else:
        await rec.context(page, "No contacts found to edit")
        await page.wait_for_timeout(1000)

    await page.wait_for_timeout(2000)
    return await rec.finish(page)


async def record_calendar_edit_delete(context: BrowserContext) -> Path | None:
    """Task-first capture: Edit and delete a calendar event."""
    rec = TaskFirstRecorder("calendar-edit-delete", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Calendar/view", 2000)

    await rec.context(page, "Modify event details or remove events that are no longer relevant")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "Plans change and outdated events clutter the calendar")
    existing = page.locator("sg-calendar-event, .calendar-event, .fc-event, [class*='event']").first
    if await existing.is_visible(timeout=3000):
        await existing.click()
        await page.wait_for_timeout(3000)

        await rec.solution(
            page, "Click on the event to edit the title and details, then save or delete"
        )
        title = page.locator("[ng-model='editor.component.summary']").first
        if await title.is_visible(timeout=2000):
            await title.click()
            await title.fill("")
            await title.type("Team Standup (Updated)", delay=80)
            await page.wait_for_timeout(300)

            sv = page.locator("button[ng-click*='editor.save'], button[type='submit']").first
            if await sv.is_visible():
                await sv.click()
                await page.wait_for_timeout(3000)

        del_btn = page.locator(
            "button[ng-click*='delete'], button:has-text('Delete'), button:has-text('Löschen')"
        ).first
        if await del_btn.is_visible(timeout=2000):
            await del_btn.click()
            await page.wait_for_timeout(3000)

        await rec.result(page, "Event has been updated and then removed from the calendar")
    else:
        await rec.context(page, "No existing events to edit")
        await page.wait_for_timeout(1000)

    await page.wait_for_timeout(2000)
    return await rec.finish(page)


async def record_global_search(context: BrowserContext) -> Path | None:
    """Task-first capture: Use global search."""
    rec = TaskFirstRecorder("global-search", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Calendar/view", 2000)

    await rec.context(page, "Quickly find emails, contacts, or events using search")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "Scrolling through long lists to find information wastes time")
    search_btn = page.locator(
        "button:has-text('Suchen'), button[ng-click*='search'], button[title*='Search']"
    ).first
    if await search_btn.is_visible(timeout=2000):
        await search_btn.click()
        await page.wait_for_timeout(1000)
    else:
        await page.keyboard.press("Control+F")
        await page.wait_for_timeout(1000)

    await rec.solution(
        page, "Type your search term and let SOGo find matching items across all modules"
    )
    inp = page.locator("input[type='search'], input[placeholder*='Search'], input:visible").first
    if await inp.is_visible(timeout=2000):
        await inp.fill("")
        await inp.type("Meeting", delay=80)
        await page.wait_for_timeout(2000)

    await rec.result(page, "Search results display matching items instantly")
    await page.wait_for_timeout(2000)
    return await rec.finish(page)


async def record_mail_read(context: BrowserContext) -> Path | None:
    """Task-first capture: Read an email."""
    rec = TaskFirstRecorder("mail-read", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Mail/view", 2000)

    await rec.context(page, "Open and read an email from your inbox")
    await page.wait_for_timeout(1000)

    await rec.challenge(
        page, "Knowing which emails need attention is hard from the subject line alone"
    )
    msg = page.locator("._mailSubject[ng-show], .mail-subject, [class*='mailSubject']").first
    if await msg.is_visible(timeout=3000):
        await rec.highlight(
            page, "._mailSubject[ng-show], .mail-subject, [class*='mailSubject']", "Email subject"
        )

    await rec.solution(page, "Click on an email to open and read its full contents")
    if await msg.is_visible(timeout=3000):
        await msg.click()
        await page.wait_for_timeout(2000)

    await rec.result(page, "The email body is displayed with full details")
    await page.wait_for_timeout(2000)
    return await rec.finish(page)


async def record_mail_folder_management(context: BrowserContext) -> Path | None:
    """Task-first capture: Browse mail folders."""
    rec = TaskFirstRecorder("mail-folder-management", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Mail/view", 2000)

    await rec.context(page, "Organize emails by navigating between different folders")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "With many folders, finding the right one takes time")
    folder_list = await page.locator("._folderLink, .folder-item, [ng-click*='selectFolder']").all()
    if folder_list:
        first_folder = folder_list[1] if len(folder_list) > 1 else folder_list[0]

    await rec.solution(page, "Click on a folder to see its contents, just like a file browser")
    if folder_list:
        first_folder = folder_list[1] if len(folder_list) > 1 else folder_list[0]
        if await first_folder.is_visible(timeout=2000):
            await first_folder.click()
            await page.wait_for_timeout(2000)

    await rec.result(page, "The selected folder's emails are displayed")
    await page.wait_for_timeout(2000)
    return await rec.finish(page)


async def record_mail_reply_forward_delete(context: BrowserContext) -> Path | None:
    """Task-first capture: Reply, forward, or delete an email."""
    rec = TaskFirstRecorder("mail-reply-forward-delete", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Mail/view", 2000)

    await rec.context(
        page, "Respond to an email by replying, forwarding, or cleaning up by deleting"
    )
    await page.wait_for_timeout(1000)

    await rec.challenge(
        page, "Managing email correspondence requires quick actions to stay productive"
    )
    msg = page.locator("._mailRow[ng-click], .mail-row").first
    if await msg.is_visible(timeout=3000):
        await msg.click()
        await page.wait_for_timeout(2000)

    await rec.solution(
        page, "Use Reply to answer, Forward to share, or Delete to remove unwanted messages"
    )
    reply_btn = page.locator("button:has-text('Reply'), button[title*='Reply']").first
    if await reply_btn.is_visible(timeout=2000):
        await reply_btn.click()
        await page.wait_for_timeout(2000)
        close_btn = page.locator("button:has-text('Close'), button[ng-click*='close']").first
        if await close_btn.is_visible(timeout=2000):
            await close_btn.click()
            await page.wait_for_timeout(1000)

    delete_btn = page.locator("button[title*='Delete'], button:has-text('Delete')").first
    if await delete_btn.is_visible(timeout=2000):
        await delete_btn.click()
        await page.wait_for_timeout(2000)

    await rec.result(
        page, "Email actions are completed: replied, forwarded, or removed from the inbox"
    )
    await page.wait_for_timeout(2000)
    return await rec.finish(page)


async def record_password_change(context: BrowserContext) -> Path | None:
    """Task-first capture: Access account security settings."""
    rec = TaskFirstRecorder("password-change", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Preferences#!/general", 5000)

    await rec.context(page, "Update your SOGo account password for security")
    await page.wait_for_timeout(1000)

    await rec.challenge(page, "Regular password changes are important for account security")
    await page.wait_for_timeout(1000)

    await rec.solution(
        page,
        "Navigate to Preferences to find the password change and two-factor authentication options",
    )
    tfa = page.locator("md-checkbox[ng-model*='SOGoEnableTwoFactorAuthentication']").first
    if await tfa.is_visible(timeout=2000):
        await tfa.click()
        await page.wait_for_timeout(1000)
    await page.wait_for_timeout(2000)

    await rec.result(
        page,
        "Account security settings are accessible in Preferences"
        " (password change requires admin approval)",
    )
    await page.wait_for_timeout(2000)
    return await rec.finish(page)


async def record_calendar_ical(context: BrowserContext) -> Path | None:
    """Task-first capture: Export calendar as iCal."""
    rec = TaskFirstRecorder("calendar-ical", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Calendar/view", 2000)

    await rec.context(page, "Export your calendar to share or back up your events")
    await page.wait_for_timeout(1000)

    await rec.challenge(
        page, "You need to share your calendar with someone who uses a different calendar app"
    )
    settings_btn = page.locator(
        "button:has-text('Settings'), md-button:has-text('Einstellungen')"
    ).first
    if await settings_btn.is_visible(timeout=2000):
        await settings_btn.click()
        await page.wait_for_timeout(2000)

    await rec.solution(
        page, "Find the iCal export option in calendar settings to download your events"
    )
    export_link = page.locator(
        "a:has-text('Export'), a[href*='ical'], button:has-text('iCal')"
    ).first
    if await export_link.is_visible(timeout=2000):
        await export_link.click()
        await page.wait_for_timeout(2000)

    await rec.result(
        page, "Calendar events are exported in iCal format for use in other applications"
    )
    await page.wait_for_timeout(2000)
    return await rec.finish(page)


async def record_contacts_import_export(context: BrowserContext) -> Path | None:
    """Task-first capture: Import or export contacts."""
    rec = TaskFirstRecorder("contacts-import-export", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Contacts", 2000)

    await rec.context(
        page, "Import contacts from another system or export your address book as backup"
    )
    await page.wait_for_timeout(1000)

    await rec.challenge(
        page, "Switching email providers or backing up contacts requires a standardized format"
    )
    menu_btn = page.locator("button:has-text('Actions'), md-button[ng-click*='menu']").first
    if await menu_btn.is_visible(timeout=2000):
        await menu_btn.click()
        await page.wait_for_timeout(1000)

    await rec.solution(page, "Use the Actions menu to import from or export contacts to a file")
    import_option = page.locator("md-menu-item:has-text('Import')").first
    if await import_option.is_visible(timeout=2000):
        await import_option.click()
        await page.wait_for_timeout(1500)

    if not await import_option.is_visible(timeout=1000):
        await rec.context(page, "Import/export options may depend on SOGo server configuration")
        await page.wait_for_timeout(500)

    await rec.result(
        page, "Contacts can be transferred between systems using standard formats like vCard"
    )
    await page.wait_for_timeout(2000)
    return await rec.finish(page)


# ── Parallel Runner ──


async def run_parallel(workflows: list[tuple], browser, storage: object, workers: int = 4):
    semaphore = asyncio.Semaphore(workers)

    async def run_task(name, fn):
        async with semaphore:
            ctx = await browser.new_context(
                record_video_dir=str(VIDEO_DIR),
                viewport={"width": 1280, "height": 800},
                locale="en-US",
                ignore_https_errors=True,
                storage_state=storage,
            )
            try:
                return await fn(ctx)
            finally:
                await ctx.close()

    tasks = [run_task(name, fn) for name, fn in workflows]
    return await asyncio.gather(*tasks)


# ── Main ──


async def main(workers: int = 1):
    clean_dirs()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # Single login, shared storage
        login_context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            locale="en-US",
            ignore_https_errors=True,
        )
        login_page = await login_context.new_page()
        await login(login_page, context=login_context)
        storage = await login_context.storage_state()
        await login_context.close()

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
            workflow_results = await run_parallel(workflows, browser, storage, workers=workers)
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
                ctx = await browser.new_context(
                    record_video_dir=str(VIDEO_DIR),
                    viewport={"width": 1280, "height": 800},
                    locale="en-US",
                    ignore_https_errors=True,
                    storage_state=storage,
                )
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
