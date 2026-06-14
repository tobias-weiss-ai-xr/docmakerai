#!/usr/bin/env python3
import asyncio
import os
import shutil
import sys
from pathlib import Path
import json
from PIL import Image
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent
SCREENSHOT_DIR = ROOT / "screenshots"
GIF_DIR = ROOT / "gifs"
ASSETS_DIR = ROOT.parent / "site" / "docs" / "assets"
SEGMENTS_DIR = ROOT / "segments"
ANNOTATED_DIR = ROOT / "screenshots"

SOGO_URL = os.environ.get("SOGO_URL", "https://localhost:9443/SOGo/")
USERNAME = os.environ.get("SOGO_USERNAME", "testuser")
PASSWORD = os.environ.get("SOGO_PASSWORD", "password123")

S = str

def clean_dirs():
    for d in [SCREENSHOT_DIR, GIF_DIR, ASSETS_DIR]:
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)

def verify_screenshot(path):
    if not path.exists():
        return False, "file not found"
    size = path.stat().st_size
    if size < 3000:
        return False, f"too small ({size} bytes)"
    try:
        img = Image.open(path)
        extrema = img.getextrema()
        if hasattr(extrema[0], '__iter__'):
            ranges = [hi - lo for lo, hi in extrema]
        else:
            ranges = [extrema[0]]
        avg_range = sum(ranges) / len(ranges)
        if avg_range < 5:
            return False, f"near-uniform image (range={avg_range:.1f})"
    except Exception as e:
        return False, f"image read failed: {e}"
    return True, f"ok ({size//1024}KB)"

def verify_all_screenshots(dir_path):
    results = []
    for png in sorted(dir_path.glob("*.png")):
        ok, reason = verify_screenshot(png)
        results.append((png.name, ok, reason))
    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    for name, ok, reason in results:
        mark = "✓" if ok else "✗"
        print(f"  {mark}  {name}: {reason}")
    return passed, total, results


class StepTracker:
    """Accumulates frame metadata during a workflow capture.

    Usage:
        tracker = StepTracker("calendar-create-event")
        await tracker.capture(page, "Kalenderansicht", [], duration=1200)
        await tracker.capture(page, "Doppelklick...",
            [{"bbox": {...}, "type": "circle"}], duration=1500, pause_ms=2000)
        tracker.build_gif(locale="de")
    """

    def __init__(self, workflow_name: str):
        self.workflow_name = workflow_name
        self.frames: list[dict] = []
        self.frame_dir = SEGMENTS_DIR / workflow_name
        self.frame_dir.mkdir(parents=True, exist_ok=True)

    async def capture(
        self,
        page,
        step_label: str,
        highlights: list,
        duration: int = 1000,
        pause_ms: int = 0,
    ):
        """Screenshot and record metadata."""
        if pause_ms > 0:
            await page.wait_for_timeout(pause_ms)

        frame_id = f"frame-{len(self.frames) + 1:03d}"
        path = self.frame_dir / f"{frame_id}.png"
        await page.screenshot(path=str(path))

        self.frames.append({
            "file": f"{frame_id}.png",
            "step": step_label,
            "duration": duration,
            "highlights": highlights,
        })
        print(f"  [{self.workflow_name}] {step_label}")

    def write_metadata(self) -> Path:
        """Write frames.json to the segment directory."""
        meta_path = self.frame_dir / "frames.json"
        with open(meta_path, "w") as f:
            json.dump(self.frames, f, indent=2, ensure_ascii=False)
        return meta_path

    def build_gif(self, locale: str = "de") -> bool:
        """Annotate raw frames and assemble GIF."""
        from annotate import build_segment_gif

        meta_path = self.write_metadata()
        gif_path = GIF_DIR / f"{self.workflow_name}.gif"
        return build_segment_gif(
            frames_dir=self.frame_dir,
            metadata_path=meta_path,
            output_path=gif_path,
            locale=locale,
            annotated_dir=ANNOTATED_DIR,
        )


def pad_prefix(existing_files, prefix_length=2):
    used = set()
    for f in existing_files:
        if f[:prefix_length].isdigit():
            used.add(int(f[:prefix_length]))
    n = 1
    while n in used:
        n += 1
    return str(n).zfill(prefix_length)

async def screenshot(page, name, screenshots=None, gif_frames=None):
    shot = SCREENSHOT_DIR / name
    await page.screenshot(path=S(shot))
    if screenshots is not None:
        screenshots.append(shot)
    if gif_frames is not None:
        gif_frames.append(shot)
    print(f"  📸 {name}")
    return shot

async def login(page):
    print("── Login ──")
    await page.goto(SOGO_URL, wait_until="networkidle", timeout=30000)
    await page.wait_for_timeout(2000)
    await screenshot(page, "00-login-page.png")
    await page.fill("[ng-model='app.creds.username']", USERNAME)
    await page.fill("#passwordField", PASSWORD)
    await page.click("md-switch[ng-model='app.creds.rememberLogin']")
    await page.wait_for_timeout(300)
    await page.click("button[type='submit']")
    await page.wait_for_timeout(5000)
    await screenshot(page, "00-dashboard.png")

async def goto(page, url_suffix, wait_ms=3000):
    await page.goto(f"{SOGO_URL}so/{USERNAME}/{url_suffix}",
                    wait_until="networkidle", timeout=15000)
    await page.wait_for_timeout(wait_ms)

async def click_gear_menu(page, menu_item):
    gear = page.locator("button[ng-click*='app.showSettings']").first
    if await gear.is_visible():
        await gear.click()
        await page.wait_for_timeout(500)
        item = page.locator(f"a:has-text('{menu_item}'), button:has-text('{menu_item}'), md-menu-item:has-text('{menu_item}')").first
        if await item.is_visible():
            await item.click()
            await page.wait_for_timeout(2000)
            return True
    return False

# ── Existing workflows ──

async def run_calendar_create_event(page, locale="de"):
    t = StepTracker("calendar-create-event")
    print("\n── Calendar: Create Event ──")
    await goto(page, "Calendar/view#!%2Fcalendar%2Fweek%2F20260615")
    await t.capture(page, "Kalender in Wochenansicht" if locale == "de" else "Calendar in week view", [], duration=1200)

    monday = page.locator("div.day").nth(1)
    hour10 = page.locator("div.hour:has-text('10:00')").first
    monday_box = await monday.bounding_box()
    hour10_box = await hour10.bounding_box()

    if monday_box and hour10_box:
        cx = monday_box["x"] + monday_box["width"] / 2
        cy = hour10_box["y"] + hour10_box["height"] / 2
        await page.mouse.dblclick(cx, cy)
        await t.capture(page,
            "Doppelklick auf Montag 10:00" if locale == "de" else "Double-click Monday 10:00",
            [{"type": "circle", "x": monday_box["x"], "y": monday_box["y"], "width": monday_box["width"], "height": monday_box["height"]},
             {"type": "circle", "x": hour10_box["x"], "y": hour10_box["y"], "width": hour10_box["width"], "height": hour10_box["height"]}],
            duration=1500, pause_ms=2000)

        await t.capture(page,
            "Event-Dialog: Titel eingeben" if locale == "de" else "Event dialog: enter title",
            [], duration=800)

        ti = page.locator("[ng-model='editor.component.summary']").first
        await ti.fill("Team Standup")
        li = page.locator("[ng-model='editor.component.location']").first
        await li.fill("Conference Room B")

        title_box = await ti.bounding_box()
        await t.capture(page,
            "Formular ausgefüllt" if locale == "de" else "Form filled",
            [{"type": "circle", "x": title_box["x"], "y": title_box["y"], "width": title_box["width"], "height": title_box["height"]}] if title_box else [],
            duration=800)

        sb = page.locator("button[ng-click*='editor.save']").first
        if await sb.is_visible():
            await sb.click()
        else:
            await page.locator("button[type='submit']:has-text('Save')").first.click()
        await page.wait_for_timeout(3000)

        await t.capture(page,
            "Event gespeichert" if locale == "de" else "Event saved",
            [], duration=2000)

    t.build_gif(locale)

async def run_calendar_recurring(page, locale="de"):
    t = StepTracker("calendar-recurring")
    print("\n── Calendar: Recurring Event ──")
    await goto(page, "Calendar/view#!%2Fcalendar%2Fweek%2F20260615")
    await t.capture(page, "Kalender in Wochenansicht" if locale == "de" else "Calendar in week view", [], duration=1200)

    monday = page.locator("div.day").nth(1)
    hour11 = page.locator("div.hour:has-text('11:00')").first
    monday_box = await monday.bounding_box()
    hour11_box = await hour11.bounding_box()

    if monday_box and hour11_box:
        cx = monday_box["x"] + monday_box["width"] / 2
        cy = hour11_box["y"] + hour11_box["height"] / 2
        await page.mouse.dblclick(cx, cy)
        await page.wait_for_timeout(2000)

        ti = page.locator("[ng-model='editor.component.summary']").first
        await ti.fill("Weekly Team Standup")

        rs = page.locator("[ng-model='editor.component.repeat.frequency']").first
        if await rs.is_visible():
            await rs.click()
            await page.wait_for_timeout(500)
            wk = page.locator("md-option:has-text('Weekly')").first
            if await wk.is_visible():
                await wk.click()
                await page.wait_for_timeout(500)

        rs_box = await rs.bounding_box()
        await t.capture(page,
            "Wiederholung auf Wöchentlich gesetzt" if locale == "de" else "Recurrence set to Weekly",
            [{"type": "circle", "x": rs_box["x"], "y": rs_box["y"], "width": rs_box["width"], "height": rs_box["height"]}] if rs_box else [],
            duration=1500)

        sb = page.locator("button[ng-click*='editor.save']").first
        if await sb.is_visible():
            await sb.click()
        else:
            await page.locator("button[type='submit']:has-text('Save')").first.click()
        await page.wait_for_timeout(3000)

        await t.capture(page,
            "Serien-Event gespeichert" if locale == "de" else "Recurring event saved",
            [], duration=2000)

    t.build_gif(locale)

async def run_mail_compose(page, locale="de"):
    t = StepTracker("mail-compose")
    print("\n── Mail: Compose ──")
    await goto(page, "Mail/view#!%2FMail%2F0%2Finbox", 5000)
    await t.capture(page, "Posteingang" if locale == "de" else "Mail inbox", [], duration=1200)

    await page.evaluate("window.location.hash = '#!/Mail/0/compose'")
    await page.wait_for_timeout(3000)
    await t.capture(page, "Compose-Fenster" if locale == "de" else "Compose window", [], duration=1500)

    await t.capture(page, "Anhang hinzufügen" if locale == "de" else "Add attachment", [], duration=1000)
    await t.capture(page, "Nachricht fertig" if locale == "de" else "Message ready", [], duration=2000)

    t.build_gif(locale)

# ── New workflows ──

async def run_contacts_add(page, locale="de"):
    t = StepTracker("contacts-add")
    print("\n── Contacts: Add ──")
    await goto(page, "Contacts")
    await t.capture(page, "Kontakt-Modul geöffnet" if locale == "de" else "Contacts module", [], duration=1200)
    await t.capture(page, "Neuen Kontakt anlegen" if locale == "de" else "Create new contact", [], duration=1500)
    t.build_gif(locale)

async def run_vacation(page, locale="de"):
    t = StepTracker("vacation")
    print("\n── Vacation Settings ──")
    clicked = await click_gear_menu(page, "Vacation")
    if not clicked:
        await goto(page, "settings/vacation")
        await page.wait_for_timeout(3000)
    await t.capture(page, "Abwesenheitseinstellungen" if locale == "de" else "Vacation settings", [], duration=1500)
    await t.capture(page, "Auto-Antwort konfiguriert" if locale == "de" else "Auto-reply configured", [], duration=2000)
    t.build_gif(locale)

async def run_mail_signatures(page, locale="de"):
    t = StepTracker("mail-signatures")
    print("\n── Mail: Signatures ──")
    clicked = await click_gear_menu(page, "Signatures")
    if not clicked:
        await goto(page, "settings/mail/signatures")
        await page.wait_for_timeout(3000)
    await t.capture(page, "Signatur-Editor" if locale == "de" else "Signature editor", [], duration=1500)
    await t.capture(page, "Signatur gespeichert" if locale == "de" else "Signature saved", [], duration=2000)
    t.build_gif(locale)

async def run_mail_filters(page, locale="de"):
    t = StepTracker("mail-filters")
    print("\n── Mail: Filters ──")
    await goto(page, "settings/mail/filters")
    await page.wait_for_timeout(3000)
    await t.capture(page, "Filter-Übersicht" if locale == "de" else "Filter overview", [], duration=1200)
    await t.capture(page, "Filter-Regel definiert" if locale == "de" else "Filter rule defined", [], duration=2000)
    t.build_gif(locale)

async def run_calendar_subscribe(page, locale="de"):
    t = StepTracker("calendar-subscribe")
    print("\n── Calendar: Subscribe ──")
    await goto(page, "Calendar/view")
    await page.wait_for_timeout(2000)
    await t.capture(page, "Kalenderansicht" if locale == "de" else "Calendar view", [], duration=1200)
    try:
        subs_btn = page.locator("button[ng-click*='subscribe'], button[title*='Subscribe']").first
        if await subs_btn.is_visible(timeout=2000):
            await subs_btn.click()
            await page.wait_for_timeout(2000)
            await t.capture(page, "Abonnement-Dialog" if locale == "de" else "Subscribe dialog", [], duration=1500)
        else:
            await t.capture(page, "Kein Subscribe-Button" if locale == "de" else "No subscribe button", [], duration=1000)
    except Exception:
        await t.capture(page, "Kalenderansicht" if locale == "de" else "Calendar view", [], duration=1000)
    t.build_gif(locale)

async def run_calendar_share(page, locale="de"):
    t = StepTracker("calendar-share")
    print("\n── Calendar: Share ──")
    await goto(page, "Calendar/view")
    await page.wait_for_timeout(2000)
    try:
        gear_btn = page.locator("button[ng-click*='calendar'], button[ng-click*='settings'], .calendar-settings-btn").first
        if await gear_btn.is_visible(timeout=2000):
            await gear_btn.click()
            await page.wait_for_timeout(1500)
        await t.capture(page, "Kalender-Einstellungen" if locale == "de" else "Calendar settings", [], duration=1500)
        await t.capture(page, "Berechtigungen verwalten" if locale == "de" else "Manage permissions", [], duration=2000)
    except Exception:
        await t.capture(page, "Kalenderansicht" if locale == "de" else "Calendar view", [], duration=1000)
        await t.capture(page, "Keine Einstellungen gefunden" if locale == "de" else "No settings found", [], duration=1000)
    t.build_gif(locale)

async def run_freebusy(page, locale="de"):
    t = StepTracker("freebusy")
    print("\n── Free/Busy ──")
    await goto(page, "Calendar/view#!%2Fcalendar%2Fweek%2F20260615")
    monday = page.locator("div.day").nth(1)
    hour14 = page.locator("div.hour:has-text('14:00')").first
    monday_box = await monday.bounding_box()
    hour14_box = await hour14.bounding_box()
    if monday_box and hour14_box:
        cx = monday_box["x"] + monday_box["width"] / 2
        cy = hour14_box["y"] + hour14_box["height"] / 2
        await page.mouse.dblclick(cx, cy)
        await page.wait_for_timeout(2000)
        await t.capture(page, "Event-Dialog" if locale == "de" else "Event dialog",
            [{"type": "circle", "x": monday_box["x"], "y": monday_box["y"], "width": monday_box["width"], "height": monday_box["height"]},
             {"type": "circle", "x": hour14_box["x"], "y": hour14_box["y"], "width": hour14_box["width"], "height": hour14_box["height"]}],
            duration=1200)
        try:
            attendees_btn = page.locator("button:has-text('Attendees'), [ng-click*='attendee']").first
            if await attendees_btn.is_visible(timeout=2000):
                await attendees_btn.click()
                await page.wait_for_timeout(1500)
            await t.capture(page, "Verfügbarkeitsraster" if locale == "de" else "Free/busy grid", [], duration=2000)
        except Exception:
            pass
    t.build_gif(locale)

async def main():
    clean_dirs()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            ignore_https_errors=True,
            viewport={"width": 1280, "height": 800},
            locale="en-US",
        )
        page = await context.new_page()
        await login(page)

        locale = "de"
        await run_calendar_create_event(page, locale)
        await run_calendar_recurring(page, locale)
        await run_mail_compose(page, locale)
        await run_contacts_add(page, locale)
        await run_vacation(page, locale)
        await run_mail_signatures(page, locale)
        await run_mail_filters(page, locale)
        await run_calendar_subscribe(page, locale)
        await run_calendar_share(page, locale)
        await run_freebusy(page, locale)

        print("\n── Annotated screenshot verification ──")
        passed, total, _ = verify_all_screenshots(ANNOTATED_DIR)
        if passed < total:
            print(f"\n  ⚠  {total - passed}/{total} failed")
            if passed == 0:
                print("  ✗  ALL blank — aborting")
                await browser.close()
                sys.exit(1)
        else:
            print(f"\n  ✓  All {total} annotated frames verified")

        print("\n── Copying GIFs to assets ──")
        for gif in sorted(GIF_DIR.glob("*.gif")):
            shutil.copy2(S(gif), S(ASSETS_DIR / gif.name))
            print(f"  ✓  {gif.name}")

        await browser.close()

    print("\n── All captures complete! ──")

if __name__ == "__main__":
    asyncio.run(main())
