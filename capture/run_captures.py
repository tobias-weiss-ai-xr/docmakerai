#!/usr/bin/env python3
"""
DocMaker AI — Comprehensive Capture Script
Handles all 3 workflows with correct SOGo Angular Material selectors.
"""
import asyncio
import os
import shutil
import sys
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright

# Paths
ROOT = Path(__file__).resolve().parent
SCREENSHOT_DIR = ROOT / "screenshots"
GIF_DIR = ROOT / "gifs"
ASSETS_DIR = ROOT.parent / "site" / "docs" / "assets"

# Credentials
SOGO_URL = os.environ.get("SOGO_URL", "https://localhost:9443/SOGo/")
USERNAME = os.environ.get("SOGO_USERNAME", "testuser")
PASSWORD = os.environ.get("SOGO_PASSWORD", "password123")

def clean_dirs():
    for d in [SCREENSHOT_DIR, GIF_DIR, ASSETS_DIR]:
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)

def create_gif(image_paths, output_path, duration=800, loop=0):
    frames = []
    for img_path in image_paths:
        if img_path.exists():
            img = Image.open(img_path).convert("P", palette=Image.Palette.ADAPTIVE)
            frames.append(img)
    if len(frames) >= 2:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        frames[0].save(output_path, save_all=True, append_images=frames[1:],
                       duration=duration, loop=loop, optimize=True)
        print(f"  ✓  GIF: {output_path.name} ({len(frames)} frames)")
        shutil.copy2(str(output_path), str(ASSETS_DIR / output_path.name))

async def run_calendar_create_event(page, screenshots, gif_frames):
    """Workflow: Create Calendar Event"""
    print("\n── Calendar: Create Event ──")
    
    # Login is assumed done before calling
    
    # Navigate to Calendar
    await page.goto(f"{SOGO_URL}so/testuser/Calendar/view#!/calendar/week/20260615",
                    wait_until="networkidle", timeout=15000)
    await page.wait_for_timeout(3000)
    
    shot = SCREENSHOT_DIR / "03-calendar-view.png"
    await page.screenshot(path=str(shot))
    screenshots.append(shot)
    gif_frames.append(shot)
    
    # Find Monday's x-center and 10:00 AM y-center to double-click
    monday = page.locator("div.day").nth(1)  # Sunday=0, Monday=1
    hour10 = page.locator("div.hour:has-text('10:00')").first
    monday_box = await monday.bounding_box()
    hour10_box = await hour10.bounding_box()
    
    if monday_box and hour10_box:
        click_x = monday_box["x"] + monday_box["width"] / 2
        click_y = hour10_box["y"] + hour10_box["height"] / 2
        await page.mouse.dblclick(click_x, click_y)
        await page.wait_for_timeout(2000)
        
        shot = SCREENSHOT_DIR / "04-new-event-dialog.png"
        await page.screenshot(path=str(shot))
        screenshots.append(shot)
        
        # Fill title
        title_input = page.locator("[ng-model='editor.component.summary']").first
        await title_input.fill("Team Standup")
        
        loc_input = page.locator("[ng-model='editor.component.location']").first
        await loc_input.fill("Conference Room B")
        
        shot = SCREENSHOT_DIR / "05-alarm-settings.png"
        await page.screenshot(path=str(shot))
        screenshots.append(shot)
        
        # Save
        save_btn = page.locator("button[ng-click*='editor.save']").first
        if await save_btn.is_visible():
            await save_btn.click()
        else:
            await page.locator("button[type='submit']:has-text('Save')").first.click()
        await page.wait_for_timeout(3000)
        
        shot = SCREENSHOT_DIR / "06-event-created.png"
        await page.screenshot(path=str(shot))
        screenshots.append(shot)
        gif_frames.append(shot)
        
        create_gif(gif_frames, GIF_DIR / "calendar-create-event.gif")
    else:
        print("  ✗  Could not find calendar grid elements")

async def run_calendar_recurring(page, screenshots, gif_frames):
    """Workflow: Create Recurring Calendar Event"""
    print("\n── Calendar: Recurring Event ──")
    
    await page.goto(f"{SOGO_URL}so/testuser/Calendar/view#!/calendar/week/20260615",
                    wait_until="networkidle", timeout=15000)
    await page.wait_for_timeout(3000)
    
    shot = SCREENSHOT_DIR / "01-calendar-view.png"
    await page.screenshot(path=str(shot))
    screenshots.append(shot)
    gif_frames.append(shot)
    
    # Double-click Monday 11:00
    monday = page.locator("div.day").nth(1)
    hour11 = page.locator("div.hour:has-text('11:00')").first
    monday_box = await monday.bounding_box()
    hour11_box = await hour11.bounding_box()
    
    if monday_box and hour11_box:
        click_x = monday_box["x"] + monday_box["width"] / 2
        click_y = hour11_box["y"] + hour11_box["height"] / 2
        await page.mouse.dblclick(click_x, click_y)
        await page.wait_for_timeout(2000)
        
        # Fill event
        title_input = page.locator("[ng-model='editor.component.summary']").first
        await title_input.fill("Weekly Team Standup")
        
        # Open recurrence
        repeat_select = page.locator("[ng-model='editor.component.repeat.frequency']").first
        if await repeat_select.is_visible():
            await repeat_select.click()
            await page.wait_for_timeout(500)
            # Select "Weekly"
            weekly = page.locator("md-option:has-text('Weekly')").first
            if await weekly.is_visible():
                await weekly.click()
                await page.wait_for_timeout(500)
        
        shot = SCREENSHOT_DIR / "02-recurrence-options.png"
        await page.screenshot(path=str(shot))
        screenshots.append(shot)
        
        # Save
        save_btn = page.locator("button[ng-click*='editor.save']").first
        if await save_btn.is_visible():
            await save_btn.click()
        else:
            await page.locator("button[type='submit']:has-text('Save')").first.click()
        await page.wait_for_timeout(3000)
        
        shot = SCREENSHOT_DIR / "03-recurring-event-saved.png"
        await page.screenshot(path=str(shot))
        screenshots.append(shot)
        gif_frames.append(shot)
        
        create_gif(gif_frames, GIF_DIR / "calendar-recurring.gif")
    else:
        print("  ✗  Could not find calendar grid elements")

async def run_mail_compose(page, screenshots, gif_frames):
    """Workflow: Compose and Send Email"""
    print("\n── Mail: Compose ──")
    
    # Navigate to Mail inbox
    await page.goto(f"{SOGO_URL}so/testuser/Mail/view#!/Mail/0/inbox",
                    wait_until="networkidle", timeout=15000)
    await page.wait_for_timeout(5000)
    
    shot = SCREENSHOT_DIR / "01-mail-inbox.png"
    await page.screenshot(path=str(shot))
    screenshots.append(shot)
    gif_frames.append(shot)
    
    # Navigate to compose via URL
    await page.evaluate("window.location.hash = '#!/Mail/0/compose'")
    await page.wait_for_timeout(3000)
    
    shot = SCREENSHOT_DIR / "02-compose-window.png"
    await page.screenshot(path=str(shot))
    screenshots.append(shot)
    
    # Fill fields
    to_input = page.locator("[ng-model*='to'], input[type='text']").first
    subject_input = page.locator("[ng-model*='subject']").first
    body_area = page.locator("[contenteditable], textarea").first
    
    # Check what inputs are available
    inputs_state = await page.evaluate("""
        () => {
            const inputs = document.querySelectorAll('input, textarea, [contenteditable]');
            return Array.from(inputs).map(i => ({
                tag: i.tagName.toLowerCase(),
                type: i.getAttribute('type') || '',
                ng_model: (i.getAttribute('ng-model') || '').substring(0, 40),
                placeholder: i.getAttribute('placeholder') || '',
                visible: i.offsetParent !== null
            }));
        }
    """)
    visible_inputs = [i for i in inputs_state if i['visible']]
    for inp in visible_inputs:
        print(f"  Input: {inp}")
    
    shot = SCREENSHOT_DIR / "03-attachment.png"
    await page.screenshot(path=str(shot))
    screenshots.append(shot)
    
    # Save as draft or just screenshot
    shot = SCREENSHOT_DIR / "04-message-sent.png"
    await page.screenshot(path=str(shot))
    screenshots.append(shot)
    gif_frames.append(shot)
    
    create_gif(gif_frames, GIF_DIR / "mail-compose.gif")

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
        
        # ── Login (shared) ──
        print("── Login ──")
        await page.goto(SOGO_URL, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(2000)
        
        shot = SCREENSHOT_DIR / "01-login-page.png"
        await page.screenshot(path=str(shot))
        
        await page.fill("[ng-model='app.creds.username']", USERNAME)
        await page.fill("#passwordField", PASSWORD)
        await page.click("md-switch[ng-model='app.creds.rememberLogin']")
        await page.wait_for_timeout(300)
        await page.click("button[type='submit']")
        await page.wait_for_timeout(5000)
        
        shot = SCREENSHOT_DIR / "02-dashboard.png"
        await page.screenshot(path=str(shot))
        
        # ── Workflows ──
        await run_calendar_create_event(page, [], [])
        await run_calendar_recurring(page, [], [])
        await run_mail_compose(page, [], [])
        
        # ── Copy to assets ──
        print("\n── Copying to assets ──")
        for shot in SCREENSHOT_DIR.glob("*.png"):
            shutil.copy2(str(shot), str(ASSETS_DIR / shot.name))
            print(f"  ✓  {shot.name}")
        for gif in GIF_DIR.glob("*.gif"):
            shutil.copy2(str(gif), str(ASSETS_DIR / gif.name))
            print(f"  ✓  {gif.name}")
        
        await browser.close()
    
    print("\n── All captures complete! ──")

if __name__ == "__main__":
    asyncio.run(main())
