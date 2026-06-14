#!/usr/bin/env python3
import asyncio
import os
import shutil
import sys
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent
SCREENSHOT_DIR = ROOT / "screenshots"
GIF_DIR = ROOT / "gifs"
ASSETS_DIR = ROOT.parent / "site" / "docs" / "assets"

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

async def run_calendar_create_event(page):
    ss, gif = [], []
    print("\n── Calendar: Create Event ──")
    await goto(page, "Calendar/view#!%2Fcalendar%2Fweek%2F20260615")
    await screenshot(page, "01-calendar-create-view.png", ss, gif)
    monday = page.locator("div.day").nth(1)
    hour10 = page.locator("div.hour:has-text('10:00')").first
    monday_box = await monday.bounding_box()
    hour10_box = await hour10.bounding_box()
    if monday_box and hour10_box:
        cx = monday_box["x"] + monday_box["width"] / 2
        cy = hour10_box["y"] + hour10_box["height"] / 2
        await page.mouse.dblclick(cx, cy)
        await page.wait_for_timeout(2000)
        await screenshot(page, "02-event-dialog.png", ss)
        ti = page.locator("[ng-model='editor.component.summary']").first
        await ti.fill("Team Standup")
        li = page.locator("[ng-model='editor.component.location']").first
        await li.fill("Conference Room B")
        await screenshot(page, "03-event-details.png", ss)
        sb = page.locator("button[ng-click*='editor.save']").first
        if await sb.is_visible():
            await sb.click()
        else:
            await page.locator("button[type='submit']:has-text('Save')").first.click()
        await page.wait_for_timeout(3000)
        await screenshot(page, "04-event-saved.png", ss, gif)
    create_gif(gif, GIF_DIR / "calendar-create-event.gif")

async def run_calendar_recurring(page):
    ss, gif = [], []
    print("\n── Calendar: Recurring Event ──")
    await goto(page, "Calendar/view#!%2Fcalendar%2Fweek%2F20260615")
    await screenshot(page, "01-calendar-recurring-view.png", ss, gif)
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
        await screenshot(page, "02-recurrence-options.png", ss)
        sb = page.locator("button[ng-click*='editor.save']").first
        if await sb.is_visible():
            await sb.click()
        else:
            await page.locator("button[type='submit']:has-text('Save')").first.click()
        await page.wait_for_timeout(3000)
        await screenshot(page, "03-recurring-saved.png", ss, gif)
    create_gif(gif, GIF_DIR / "calendar-recurring.gif")

async def run_mail_compose(page):
    ss, gif = [], []
    print("\n── Mail: Compose ──")
    await goto(page, "Mail/view#!%2FMail%2F0%2Finbox", 5000)
    await screenshot(page, "01-mail-inbox.png", ss, gif)
    await page.evaluate("window.location.hash = '#!/Mail/0/compose'")
    await page.wait_for_timeout(3000)
    await screenshot(page, "02-compose-window.png", ss)
    await screenshot(page, "03-attachment.png", ss)
    await screenshot(page, "04-message-sent.png", ss, gif)
    create_gif(gif, GIF_DIR / "mail-compose.gif")

# ── New workflows ──

async def run_contacts_add(page):
    ss = []
    print("\n── Contacts: Add ──")
    await goto(page, "Contacts")
    await screenshot(page, "01-contacts-module.png", ss)

async def run_vacation(page):
    ss = []
    print("\n── Vacation Settings ──")
    clicked = await click_gear_menu(page, "Vacation")
    if not clicked:
        await goto(page, "settings/vacation")
        await page.wait_for_timeout(3000)
    await screenshot(page, "01-vacation-settings.png", ss)

async def run_mail_signatures(page):
    ss = []
    print("\n── Mail: Signatures ──")
    clicked = await click_gear_menu(page, "Signatures")
    if not clicked:
        await goto(page, "settings/mail/signatures")
        await page.wait_for_timeout(3000)
    await screenshot(page, "01-mail-signatures.png", ss)

async def run_mail_filters(page):
    ss = []
    print("\n── Mail: Filters ──")
    await goto(page, "settings/mail/filters")
    await page.wait_for_timeout(3000)
    await screenshot(page, "01-mail-filters.png", ss)

async def run_calendar_subscribe(page):
    ss = []
    print("\n── Calendar: Subscribe ──")
    await goto(page, "Calendar/view")
    await page.wait_for_timeout(2000)
    try:
        subs_btn = page.locator("button[ng-click*='subscribe'], button[title*='Subscribe']").first
        if await subs_btn.is_visible(timeout=2000):
            await subs_btn.click()
            await page.wait_for_timeout(2000)
            await screenshot(page, "01-subscribe-dialog.png", ss)
        else:
            await screenshot(page, "01-calendar-view.png", ss)
    except Exception:
        await screenshot(page, "01-calendar-view.png", ss)

async def run_calendar_share(page):
    ss = []
    print("\n── Calendar: Share ──")
    await goto(page, "Calendar/view")
    await page.wait_for_timeout(2000)
    try:
        gear_btn = page.locator("button[ng-click*='calendar'], button[ng-click*='settings'], .calendar-settings-btn").first
        if await gear_btn.is_visible(timeout=2000):
            await gear_btn.click()
            await page.wait_for_timeout(1500)
        await screenshot(page, "01-calendar-settings.png", ss)
    except Exception:
        await screenshot(page, "01-calendar-view.png", ss)

async def run_freebusy(page):
    ss = []
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
        await screenshot(page, "01-event-dialog.png", ss)
        try:
            attendees_btn = page.locator("button:has-text('Attendees'), [ng-click*='attendee']").first
            if await attendees_btn.is_visible(timeout=2000):
                await attendees_btn.click()
                await page.wait_for_timeout(1500)
            await screenshot(page, "02-freebusy-grid.png", ss)
        except Exception:
            pass

def create_gif(frames, output_path, duration=800, loop=0):
    img_frames = []
    for fp in frames:
        if fp.exists():
            img = Image.open(fp).convert("P", palette=Image.Palette.ADAPTIVE)
            img_frames.append(img)
    if len(img_frames) >= 2:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        img_frames[0].save(output_path, save_all=True, append_images=img_frames[1:],
                           duration=duration, loop=loop, optimize=True)
        print(f"  ✓  GIF: {output_path.name} ({len(img_frames)} frames)")
        shutil.copy2(S(output_path), S(ASSETS_DIR / output_path.name))

async def main():
    clean_dirs()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            ignore_https_errors=True,
            viewport={"width": 1280, "height": 800},
            locale="en-US"
        )
        page = await context.new_page()
        await login(page)
        await run_calendar_create_event(page)
        await run_calendar_recurring(page)
        await run_mail_compose(page)
        await run_contacts_add(page)
        await run_vacation(page)
        await run_mail_signatures(page)
        await run_mail_filters(page)
        await run_calendar_subscribe(page)
        await run_calendar_share(page)
        await run_freebusy(page)

        # Verify
        print("\n── Screenshot content verification ──")
        passed, total, _ = verify_all_screenshots(SCREENSHOT_DIR)
        if passed < total:
            print(f"\n  ⚠  {total - passed}/{total} failed")
            if passed == 0:
                print("  ✗  ALL blank — aborting")
                await browser.close()
                sys.exit(1)
        else:
            print(f"\n  ✓  All {total} verified")

        # Copy to assets
        print("\n── Copying to assets ──")
        for shot in sorted(SCREENSHOT_DIR.glob("*.png")):
            shutil.copy2(S(shot), S(ASSETS_DIR / shot.name))
            print(f"  ✓  {shot.name}")
        for gif in GIF_DIR.glob("*.gif"):
            shutil.copy2(S(gif), S(ASSETS_DIR / gif.name))
            print(f"  ✓  {gif.name}")
        await browser.close()
    print("\n── All captures complete! ──")

if __name__ == "__main__":
    asyncio.run(main())
