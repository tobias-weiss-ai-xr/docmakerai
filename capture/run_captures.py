#!/usr/bin/env python3
"""
DocMaker AI — SOGo Workflow Capture Runner

Captures smooth animated WebP sequences for each tutorial workflow using
Playwright video recording + ffmpeg frame extraction + annotation overlay.

Usage:
  export SOGO_URL=https://demo.sogo.nu/SOGo/
  export SOGO_USERNAME=demo
  export SOGO_PASSWORD=demo
  python run_captures.py
"""

from __future__ import annotations

import asyncio
import os
import shutil
from pathlib import Path

from playwright.async_api import BrowserContext, Page, async_playwright

try:
    from capture.video_pipeline import WorkflowRecorder
except ImportError:
    from video_pipeline import WorkflowRecorder

ROOT = Path(__file__).resolve().parent
VIDEO_DIR = ROOT / "videos"
GIF_DIR = ROOT / "gifs"
ASSETS_DIR = ROOT.parent / "site" / "docs" / "assets"
SCREENSHOT_DIR = ROOT / "screenshots"

SOGO_URL = os.environ.get("SOGO_URL", "https://demo.sogo.nu/SOGo/")
USERNAME = os.environ.get("SOGO_USERNAME", "demo")
PASSWORD = os.environ.get("SOGO_PASSWORD", "demo")

FPS = 6
LOCALE = "de"


def clean_dirs() -> None:
    for d in [VIDEO_DIR, GIF_DIR, ASSETS_DIR, SCREENSHOT_DIR]:
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)


async def login(page: Page) -> None:
    print("── Login ──")
    await page.goto(SOGO_URL, wait_until="networkidle", timeout=30000)
    await page.wait_for_timeout(2000)
    await page.fill("[ng-model='app.creds.username']", USERNAME)
    await page.fill("#passwordField", PASSWORD)
    await page.click("md-switch[ng-model='app.creds.rememberLogin']")
    await page.wait_for_timeout(300)
    await page.click("button[type='submit']")
    await page.wait_for_timeout(5000)


async def goto(page: Page, url_suffix: str, wait_ms: int = 3000) -> None:
    await page.goto(
        f"{SOGO_URL}so/{USERNAME}/{url_suffix}",
        wait_until="networkidle",
        timeout=15000,
    )
    await page.wait_for_timeout(wait_ms)


# ── Workflow Runners ──

async def record_calendar_create_event(context: BrowserContext) -> Path | None:
    """Create a calendar event via double-click, typing title and location."""
    rec = WorkflowRecorder("calendar-create-event", VIDEO_DIR, GIF_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Calendar/view#!/calendar/week/20260615")
    await rec.step(page, "Kalender in Wochenansicht", highlights=[])
    await page.wait_for_timeout(1500)

    monday = page.locator("sg-calendar-day.day").nth(8)
    hour10 = monday.locator(".clickableHourCell10").first
    mb = await monday.bounding_box()
    hb = await hour10.bounding_box()
    if mb and hb:
        await page.mouse.dblclick(mb["x"] + mb["width"] / 2, hb["y"] + hb["height"] / 2)
        await rec.step(
            page, "Doppelklick auf Montag 10:00",
            highlights=[
                {"type": "circle", "x": mb["x"], "y": mb["y"],
                 "width": mb["width"], "height": mb["height"]},
                {"type": "circle", "x": hb["x"], "y": hb["y"],
                 "width": hb["width"], "height": hb["height"]},
            ],
        )
        await page.wait_for_timeout(2000)

        # Type title with natural delay
        await page.click("[ng-model='editor.component.summary']")
        await page.fill("[ng-model='editor.component.summary']", "")
        await page.type("[ng-model='editor.component.summary']",
                        "Team Standup", delay=60)
        await rec.step(page, "Titel eingegeben: Team Standup", highlights=[])
        await page.wait_for_timeout(800)

        # Location
        await page.click("[ng-model='editor.component.location']")
        await page.fill("[ng-model='editor.component.location']", "")
        await page.type("[ng-model='editor.component.location']",
                        "Conference Room B", delay=50)
        await rec.step(page, "Ort eingegeben", highlights=[])
        await page.wait_for_timeout(800)

        # Save
        btn = page.locator("button[ng-click*='editor.save']").first
        if not await btn.is_visible():
            btn = page.locator("button[type='submit']:has-text('Save')").first
        await btn.click()
        await page.wait_for_timeout(3000)
        await rec.step(page, "Event gespeichert", highlights=[])

    return await rec.finish(page)


async def record_calendar_recurring(context: BrowserContext) -> Path | None:
    """Create a recurring weekly event with alarm."""
    rec = WorkflowRecorder("calendar-recurring", VIDEO_DIR, GIF_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Calendar/view#!/calendar/week/20260615")
    await rec.step(page, "Kalender in Wochenansicht", highlights=[])
    await page.wait_for_timeout(1500)

    monday = page.locator("sg-calendar-day.day").nth(8)
    hour11 = monday.locator(".clickableHourCell11").first
    mb = await monday.bounding_box()
    hb = await hour11.bounding_box()
    if mb and hb:
        await page.mouse.dblclick(mb["x"] + mb["width"] / 2, hb["y"] + hb["height"] / 2)
        await page.wait_for_timeout(2000)
        await rec.step(page, "Neues Event Dialog", highlights=[])

        # Type title
        await page.click("[ng-model='editor.component.summary']")
        await page.fill("[ng-model='editor.component.summary']", "")
        await page.type("[ng-model='editor.component.summary']",
                        "Weekly Team Standup", delay=60)
        await rec.step(page, "Titel: Weekly Team Standup", highlights=[])
        await page.wait_for_timeout(800)

        # Recurrence
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
                # Dismiss dropdown
                await page.keyboard.press("Escape")
                await page.wait_for_timeout(500)
        rr = await rs.bounding_box()
        await rec.step(
            page, "Wiederholung auf Wöchentlich gesetzt",
            highlights=[{"type": "circle", "x": rr["x"], "y": rr["y"],
                         "width": rr["width"], "height": rr["height"]}]
            if rr else [],
        )
        await page.wait_for_timeout(800)

        # Save
        btn = page.locator("button[ng-click*='editor.save']").first
        if not await btn.is_visible():
            btn = page.locator("button[type='submit']:has-text('Save')").first
        await btn.click()
        await page.wait_for_timeout(3000)
        await rec.step(page, "Serien-Event gespeichert", highlights=[])

    return await rec.finish(page)


async def record_mail_compose(context: BrowserContext) -> Path | None:
    """Navigate to Mail UI (compose not available without IMAP server)."""
    rec = WorkflowRecorder("mail-compose", VIDEO_DIR, GIF_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Mail/view#!/Mail", 5000)
    await rec.step(page, "E-Mail-Ansicht (kein IMAP-Server verfügbar)", highlights=[])
    await page.wait_for_timeout(2000)

    # Show the mail account info that IS available
    acct = page.locator("text=campususer1@localhost.local").first
    if await acct.is_visible(timeout=2000):
        box = await acct.bounding_box()
        if box:
            await rec.step(page, "E-Mail-Konto (nur Konfiguration)",
                           highlights=[{"type": "circle", "x": box["x"], "y": box["y"],
                                        "width": box["width"], "height": box["height"]}])
            await page.wait_for_timeout(1000)

    return await rec.finish(page)


async def record_contacts_add(context: BrowserContext) -> Path | None:
    """Add a new contact."""
    rec = WorkflowRecorder("contacts-add", VIDEO_DIR, GIF_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Contacts")
    await rec.step(page, "Kontakt-Modul geöffnet", highlights=[])
    await page.wait_for_timeout(1000)

    try:
        add_btn = page.locator(
            "button[ng-click*='add'], button[ng-click*='new'], a[ng-click*='add']"
        ).first
        if await add_btn.is_visible(timeout=2000):
            await add_btn.click()
            await page.wait_for_timeout(2000)
    except Exception:
        pass
    await rec.step(page, "Neuen Kontakt anlegen", highlights=[])
    await page.wait_for_timeout(500)

    # First name
    fn = page.locator("[ng-model='contact.c_firstname'], input[name='firstname']").first
    if await fn.is_visible():
        await fn.click()
        await fn.fill("")
        await fn.type("John", delay=80)
        await page.wait_for_timeout(300)
        await rec.step(page, "Vorname: John", highlights=[])

    # Last name
    ln = page.locator("[ng-model='contact.c_name'], input[name='lastname']").first
    if await ln.is_visible():
        await ln.click()
        await ln.fill("")
        await ln.type("Doe", delay=80)
        await page.wait_for_timeout(300)
        await rec.step(page, "Nachname: Doe", highlights=[])

    # Email
    em = page.locator("[ng-model='contact.c_email'], input[type='email']").first
    if await em.is_visible():
        await em.click()
        await em.fill("")
        await em.type("john.doe@company.com", delay=40)
        await page.wait_for_timeout(300)
        await rec.step(page, "E-Mail eingegeben", highlights=[])

    # Save
    try:
        sv = page.locator("button[ng-click*='save'], button[type='submit']:has-text('Save')").first
        if await sv.is_visible(timeout=2000):
            await sv.click()
            await page.wait_for_timeout(3000)
    except Exception:
        pass
    await rec.step(page, "Kontakt gespeichert", highlights=[])

    return await rec.finish(page)


async def record_vacation(context: BrowserContext) -> Path | None:
    """Configure vacation auto-reply."""
    rec = WorkflowRecorder("vacation", VIDEO_DIR, GIF_DIR, FPS, LOCALE)
    page = await rec.start(context)

    # Open vacation settings via gear menu
    gear = page.locator("button[ng-click*='app.showSettings']").first
    if await gear.is_visible():
        await gear.click()
        await page.wait_for_timeout(500)
        vacation_link = page.locator("a:has-text('Vacation'), button:has-text('Vacation')").first
        if await vacation_link.is_visible():
            await vacation_link.click()
            await page.wait_for_timeout(3000)
    else:
        await goto(page, "settings/vacation", 3000)
    await rec.step(page, "Abwesenheitseinstellungen geöffnet", highlights=[])
    await page.wait_for_timeout(500)

    # Toggle auto-reply ON
    try:
        toggle = page.locator(
            "md-switch[ng-model='vacation.enabled'], input[type='checkbox']"
        ).first
        if await toggle.is_visible(timeout=2000):
            await toggle.click()
            await page.wait_for_timeout(1000)
    except Exception:
        pass
    await rec.step(page, "Auto-Antwort aktiviert", highlights=[])

    # Start date
    sd = page.locator("[ng-model='vacation.startDate'], input[name='startdate']").first
    if await sd.is_visible():
        await sd.click()
        await sd.fill("")
        await sd.type("2026-07-15", delay=60)
        await page.wait_for_timeout(300)
        await rec.step(page, "Startdatum: 15.07.2026", highlights=[])

    # End date
    ed = page.locator("[ng-model='vacation.endDate'], input[name='enddate']").first
    if await ed.is_visible():
        await ed.click()
        await ed.fill("")
        await ed.type("2026-07-28", delay=60)
        await page.wait_for_timeout(300)
        await rec.step(page, "Enddatum: 28.07.2026", highlights=[])

    # Message
    try:
        msg = page.locator("[ng-model='vacation.text'], textarea").first
        if await msg.is_visible(timeout=2000):
            await msg.click()
            await msg.fill("")
            await msg.type("Ich bin vom 15.07. bis 28.07. nicht im Büro.", delay=30)
            await page.wait_for_timeout(300)
    except Exception:
        pass
    await rec.step(page, "Nachricht eingegeben", highlights=[])

    # Save
    try:
        sv = page.locator("button[ng-click*='save'], button[type='submit']:has-text('Save')").first
        if await sv.is_visible(timeout=2000):
            await sv.click()
            await page.wait_for_timeout(3000)
    except Exception:
        pass
    await rec.step(page, "Auto-Antwort konfiguriert", highlights=[])

    return await rec.finish(page)


async def record_mail_signatures(context: BrowserContext) -> Path | None:
    """Create email signature."""
    rec = WorkflowRecorder("mail-signatures", VIDEO_DIR, GIF_DIR, FPS, LOCALE)
    page = await rec.start(context)

    gear = page.locator("button[ng-click*='app.showSettings']").first
    if await gear.is_visible():
        await gear.click()
        await page.wait_for_timeout(500)
        sig_link = page.locator("a:has-text('Signature'), button:has-text('Signatures')").first
        if await sig_link.is_visible():
            await sig_link.click()
            await page.wait_for_timeout(3000)
    else:
        await goto(page, "settings/mail/signatures", 3000)
    await rec.step(page, "Signatur-Editor geöffnet", highlights=[])
    await page.wait_for_timeout(500)

    # Signature name
    sn = page.locator("[ng-model='signature.name'], input[name='signaturename']").first
    if await sn.is_visible():
        await sn.click()
        await sn.fill("")
        await sn.type("Standard", delay=80)
        await page.wait_for_timeout(300)
        await rec.step(page, "Signatur-Name: Standard", highlights=[])

    # Signature body
    try:
        sb = page.locator("[ng-model='signature.text'], textarea").first
        if await sb.is_visible(timeout=2000):
            await sb.click()
            await sb.fill("")
            await sb.type("John Doe\nSoftware Engineer\njohn.doe@company.com", delay=30)
            await page.wait_for_timeout(300)
    except Exception:
        pass
    await rec.step(page, "Signatur-Text eingegeben", highlights=[])

    # Save
    try:
        sv = page.locator("button[ng-click*='save'], button[type='submit']:has-text('Save')").first
        if await sv.is_visible(timeout=2000):
            await sv.click()
            await page.wait_for_timeout(3000)
    except Exception:
        pass
    await rec.step(page, "Signatur gespeichert", highlights=[])

    return await rec.finish(page)


async def record_mail_filters(context: BrowserContext) -> Path | None:
    """Create mail filter rule."""
    rec = WorkflowRecorder("mail-filters", VIDEO_DIR, GIF_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "settings/mail/filters", 3000)
    await rec.step(page, "Filter-Übersicht", highlights=[])
    await page.wait_for_timeout(500)

    try:
        add_btn = page.locator(
            "button[ng-click*='add'], button:has-text('Add')"
        ).first
        if await add_btn.is_visible(timeout=2000):
            await add_btn.click()
            await page.wait_for_timeout(2000)
    except Exception:
        pass
    await rec.step(page, "Neuer Filter Dialog", highlights=[])
    await page.wait_for_timeout(500)

    # Filter name
    fn = page.locator("[ng-model='filter.name'], input[name='filtername']").first
    if await fn.is_visible():
        await fn.click()
        await fn.fill("")
        await fn.type("Newsletter", delay=80)
        await page.wait_for_timeout(300)
        await rec.step(page, "Filter-Name: Newsletter", highlights=[])

    # Condition
    mt = page.locator("[ng-model='filter.match'], input[name='filtermatch']").first
    if await mt.is_visible():
        await mt.click()
        await mt.fill("")
        await mt.type("@newsletter.com", delay=50)
        await page.wait_for_timeout(300)
        await rec.step(page, "Bedingung: @newsletter.com", highlights=[])

    # Save
    try:
        sv = page.locator("button[ng-click*='save'], button[type='submit']:has-text('Save')").first
        if await sv.is_visible(timeout=2000):
            await sv.click()
            await page.wait_for_timeout(3000)
    except Exception:
        pass
    await rec.step(page, "Filter gespeichert", highlights=[])

    return await rec.finish(page)


async def record_calendar_subscribe(context: BrowserContext) -> Path | None:
    """Subscribe to external calendar."""
    rec = WorkflowRecorder("calendar-subscribe", VIDEO_DIR, GIF_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Calendar/view")
    await rec.step(page, "Kalenderansicht", highlights=[])
    await page.wait_for_timeout(1000)

    try:
        btn = page.locator(
            "button[ng-click*='subscribe'], button[title*='Subscribe']"
        ).first
        if await btn.is_visible(timeout=2000):
            await btn.click()
            await page.wait_for_timeout(2000)
            await rec.step(page, "Abonnement-Dialog öffnet sich", highlights=[])
    except Exception:
        await rec.step(page, "Kein Subscribe-Button", highlights=[])
        return await rec.finish(page)

    # URL
    url_inp = page.locator(
        "input[ng-model='subscription.url'], input[type='url']"
    ).first
    if await url_inp.is_visible():
        await url_inp.click()
        await url_inp.fill("")
        await url_inp.type("https://calendar.example.com/feed.ics", delay=40)
        await page.wait_for_timeout(300)
        await rec.step(page, "Kalender-URL eingegeben", highlights=[])

        # Subscribe
        try:
            sv = page.locator(
                "button[ng-click*='save'], button[type='submit']:has-text('Subscribe')"
            ).first
            if await sv.is_visible(timeout=2000):
                await sv.click()
                await page.wait_for_timeout(3000)
        except Exception:
            pass
    await rec.step(page, "Kalender abonniert", highlights=[])

    return await rec.finish(page)


async def record_calendar_share(context: BrowserContext) -> Path | None:
    """Share calendar with another user."""
    rec = WorkflowRecorder("calendar-share", VIDEO_DIR, GIF_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Calendar/view")
    await rec.step(page, "Kalenderansicht", highlights=[])
    await page.wait_for_timeout(1000)

    try:
        gear_btn = page.locator(
            "button[ng-click*='calendar'], button[ng-click*='settings']"
        ).first
        if await gear_btn.is_visible(timeout=2000):
            await gear_btn.click()
            await page.wait_for_timeout(1500)
            await rec.step(page, "Kalender-Einstellungen geöffnet", highlights=[])
    except Exception:
        pass

    try:
        share_tab = page.locator(
            "a:has-text('Share'), button:has-text('Teilen'), md-tab-item:has-text('Share')"
        ).first
        if await share_tab.is_visible(timeout=2000):
            await share_tab.click()
            await page.wait_for_timeout(2000)
    except Exception:
        pass
    await rec.step(page, "Freigabe-Dialog", highlights=[])
    await page.wait_for_timeout(500)

    # Email
    em = page.locator(
        "input[ng-model='share.email'], input[type='email']"
    ).first
    if await em.is_visible():
        await em.click()
        await em.fill("")
        await em.type("colleague@company.com", delay=50)
        await page.wait_for_timeout(300)
        await rec.step(page, "Benutzer eingegeben", highlights=[])

    # Permission
    try:
        perm = page.locator("md-select[ng-model='share.permission'], select").first
        if await perm.is_visible(timeout=2000):
            await perm.click()
            await page.wait_for_timeout(500)
            ro = page.locator("md-option:has-text('View'), option:has-text('Read')").first
            if await ro.is_visible(timeout=1000):
                await ro.click()
                await page.wait_for_timeout(500)
    except Exception:
        pass
    await rec.step(page, "Berechtigungen verwalten", highlights=[])

    return await rec.finish(page)


async def record_freebusy(context: BrowserContext) -> Path | None:
    """Create event with attendee availability check."""
    rec = WorkflowRecorder("freebusy", VIDEO_DIR, GIF_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Calendar/view#!/calendar/week/20260615")
    await rec.step(page, "Kalender in Wochenansicht", highlights=[])
    await page.wait_for_timeout(1000)

    monday = page.locator("sg-calendar-day.day").nth(8)
    hour14 = monday.locator(".clickableHourCell14").first
    mb = await monday.bounding_box()
    hb = await hour14.bounding_box()
    if mb and hb:
        await page.mouse.dblclick(mb["x"] + mb["width"] / 2, hb["y"] + hb["height"] / 2)
        await page.wait_for_timeout(2000)
        await rec.step(
            page, "Doppelklick auf 14:00",
            highlights=[
                {"type": "circle", "x": mb["x"], "y": mb["y"],
                 "width": mb["width"], "height": mb["height"]},
                {"type": "circle", "x": hb["x"], "y": hb["y"],
                 "width": hb["width"], "height": hb["height"]},
            ],
        )

        # Title
        await page.click("[ng-model='editor.component.summary']")
        await page.fill("[ng-model='editor.component.summary']", "")
        await page.type("[ng-model='editor.component.summary']",
                        "Team Meeting", delay=60)
        await rec.step(page, "Titel: Team Meeting", highlights=[])
        await page.wait_for_timeout(500)

        # Attendees
        try:
            at = page.locator(
                "button:has-text('Attendees'), [ng-click*='attendee']"
            ).first
            if await at.is_visible(timeout=2000):
                await at.click()
                await page.wait_for_timeout(2000)
                await rec.step(page, "Teilnehmer-Dialog", highlights=[])

                em = page.locator(
                    "input[ng-model='attendee.email'], input[type='email']"
                ).first
                if await em.is_visible():
                    await em.click()
                    await em.fill("")
                    await em.type("colleague@company.com", delay=50)
                    await page.wait_for_timeout(2000)
        except Exception:
            pass

    await rec.step(page, "Verfügbarkeitsprüfung", highlights=[])

    return await rec.finish(page)


async def record_logout(context: BrowserContext) -> Path | None:
    rec = WorkflowRecorder("logout", VIDEO_DIR, GIF_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Calendar/view", 2000)
    await rec.step(page, "Angemeldet im Calendar", highlights=[])
    await page.wait_for_timeout(500)

    logout_link = page.locator('a[href*="logoff"]').first
    if await logout_link.is_visible(timeout=2000):
        box = await logout_link.bounding_box()
        if box:
            await rec.step(page, "Logout-Button",
                           highlights=[{"type": "circle", "x": box["x"], "y": box["y"],
                                        "width": box["width"], "height": box["height"]}])
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
    await rec.step(page, "Abgemeldet — Login-Seite sichtbar", highlights=[])

    return await rec.finish(page)


async def record_preferences(context: BrowserContext) -> Path | None:
    rec = WorkflowRecorder("preferences", VIDEO_DIR, GIF_DIR, FPS, LOCALE)
    page = await rec.start(context)

    settings_link = page.locator('a[href*="Preferences"]').first
    if await settings_link.is_visible(timeout=3000):
        box = await settings_link.bounding_box()
        if box:
            await rec.step(page, "Einstellungen öffnen",
                           highlights=[{"type": "circle", "x": box["x"], "y": box["y"],
                                        "width": box["width"], "height": box["height"]}])
        await settings_link.click()
        await page.wait_for_timeout(3000)
    else:
        await goto(page, "Preferences", 3000)
    await rec.step(page, "Allgemeine Einstellungen", highlights=[])
    await page.wait_for_timeout(500)

    tabs = page.locator("md-tab-item, .tab-item, [role='tab']").all()
    tab_texts = []
    for tab in await tabs:
        tt = await tab.text_content()
        if tt and tt.strip():
            tab_texts.append(tt.strip())
    if tab_texts:
        for target_tab_text in ["General", "Allgemein", "Notification", "Benachrichtigungen"]:
            tab = page.locator(f"md-tab-item:has-text('{target_tab_text}'), .tab-item:has-text('{target_tab_text}')").first
            if await tab.is_visible(timeout=1000):
                await tab.click()
                await page.wait_for_timeout(1500)
                await rec.step(page, f"Tab: {target_tab_text}", highlights=[])
                break

    return await rec.finish(page)


async def record_calendar_views(context: BrowserContext) -> Path | None:
    rec = WorkflowRecorder("calendar-views", VIDEO_DIR, GIF_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Calendar/view", 2000)
    await rec.step(page, "Standard-Wochenansicht", highlights=[])
    await page.wait_for_timeout(500)

    day_btn = page.locator("button:has-text('Day'), md-button:has-text('Tag')").first
    if await day_btn.is_visible(timeout=2000):
        db = await day_btn.bounding_box()
        await day_btn.click()
        await page.wait_for_timeout(2000)
        await rec.step(page, "Tagesansicht",
                       highlights=[{"type": "circle", "x": db["x"], "y": db["y"],
                                    "width": db["width"], "height": db["height"]}]
                        if db else [])
    else:
        view_btns = page.locator("button[ng-click*='view'], button[ng-click*='setView']").all()
        for btn in await view_btns:
            txt = await btn.text_content()
            if txt and "day" in txt.lower():
                await btn.click()
                await page.wait_for_timeout(2000)
                await rec.step(page, "Tagesansicht", highlights=[])
                break
        else:
            await rec.step(page, "Tagesansicht (kein Button-Interaktion)", highlights=[])

    month_btn = page.locator("button:has-text('Month'), md-button:has-text('Monat')").first
    if await month_btn.is_visible(timeout=2000):
        mb = await month_btn.bounding_box()
        await month_btn.click()
        await page.wait_for_timeout(2000)
        await rec.step(page, "Monatsansicht",
                       highlights=[{"type": "circle", "x": mb["x"], "y": mb["y"],
                                    "width": mb["width"], "height": mb["height"]}]
                       if mb else [])
    else:
        await rec.step(page, "Monatsansicht", highlights=[])

    week_btn = page.locator("button:has-text('Week'), md-button:has-text('Woche')").first
    if await week_btn.is_visible(timeout=2000):
        await week_btn.click()
        await page.wait_for_timeout(2000)
        await rec.step(page, "Zurück zur Wochenansicht", highlights=[])

    return await rec.finish(page)


async def record_contacts_edit_delete(context: BrowserContext) -> Path | None:
    rec = WorkflowRecorder("contacts-edit-delete", VIDEO_DIR, GIF_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Contacts", 2000)
    await rec.step(page, "Kontaktliste geöffnet", highlights=[])
    await page.wait_for_timeout(500)

    user = page.locator("text=John").first
    if await user.is_visible(timeout=3000):
        box = await user.bounding_box()
        if box:
            await rec.step(page, "Kontakt: John Doe",
                           highlights=[{"type": "circle", "x": box["x"], "y": box["y"],
                                        "width": box["width"], "height": box["height"]}])
        await user.click()
        await page.wait_for_timeout(2000)
        await rec.step(page, "Kontakt-Details geöffnet", highlights=[])
        await page.wait_for_timeout(500)

        phone = page.locator("[ng-model='contact.c_telephone'], input[type='tel']").first
        if await phone.is_visible():
            await phone.click()
            await phone.fill("")
            await phone.type("+49 123 456 789", delay=50)
            await page.wait_for_timeout(300)
            await rec.step(page, "Telefonnummer bearbeitet", highlights=[])

            sv = page.locator("button[ng-click*='save'], button[type='submit']:has-text('Save')").first
            if await sv.is_visible(timeout=2000):
                await sv.click()
                await page.wait_for_timeout(2000)
                await rec.step(page, "Änderungen gespeichert", highlights=[])
        else:
            await rec.step(page, "Bearbeiten nicht verfügbar", highlights=[])

        try:
            del_btn = page.locator("button[ng-click*='delete'], button:has-text('Delete'), button:has-text('Löschen')").first
            if await del_btn.is_visible(timeout=2000):
                await del_btn.click()
                await page.wait_for_timeout(2000)
                await rec.step(page, "Kontakt gelöscht", highlights=[])
        except Exception:
            await rec.step(page, "Löschen nicht verfügbar", highlights=[])
    else:
        await rec.step(page, "Keine Kontakte gefunden", highlights=[])

    return await rec.finish(page)


async def record_calendar_edit_delete(context: BrowserContext) -> Path | None:
    rec = WorkflowRecorder("calendar-edit-delete", VIDEO_DIR, GIF_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Calendar/view", 2000)
    await rec.step(page, "Kalenderansicht", highlights=[])
    await page.wait_for_timeout(1000)

    existing = page.locator("sg-calendar-event, .calendar-event, .event, [class*='event'], .fc-event").first
    if await existing.is_visible(timeout=3000):
        box = await existing.bounding_box()
        if box:
            await rec.step(page, "Vorhandenes Event",
                           highlights=[{"type": "circle", "x": box["x"], "y": box["y"],
                                        "width": box["width"], "height": box["height"]}])
        await existing.click()
        await page.wait_for_timeout(3000)
        await rec.step(page, "Event-Details geöffnet", highlights=[])
        await page.wait_for_timeout(500)

        title = page.locator("[ng-model='editor.component.summary']").first
        if await title.is_visible(timeout=2000):
            await title.click()
            await title.fill("")
            await title.type("Team Standup (Aktualisiert)", delay=60)
            await page.wait_for_timeout(300)
            await rec.step(page, "Titel bearbeitet", highlights=[])

            sv = page.locator("button[ng-click*='editor.save'], button[type='submit']").first
            if await sv.is_visible():
                await sv.click()
                await page.wait_for_timeout(3000)
                await rec.step(page, "Event aktualisiert", highlights=[])
        else:
            await rec.step(page, "Bearbeiten nicht verfügbar", highlights=[])

        # Delete
        try:
            del_btn = page.locator("button[ng-click*='delete'], button:has-text('Delete'), button:has-text('Löschen')").first
            if await del_btn.is_visible(timeout=2000):
                await del_btn.click()
                await page.wait_for_timeout(3000)
                await rec.step(page, "Event gelöscht", highlights=[])
        except Exception:
            await rec.step(page, "Löschen nicht verfügbar", highlights=[])
    else:
        await rec.step(page, "Keine Events gefunden", highlights=[])

    return await rec.finish(page)


async def record_global_search(context: BrowserContext) -> Path | None:
    """Demonstrate global search."""
    rec = WorkflowRecorder("global-search", VIDEO_DIR, GIF_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Calendar/view", 2000)
    await rec.step(page, "Kalenderansicht", highlights=[])
    await page.wait_for_timeout(500)

    # Find and use the search button/field
    search_btn = page.locator("button:has-text('Suchen'), button[ng-click*='search'], button[title*='Search']").first
    if await search_btn.is_visible(timeout=2000):
        sb = await search_btn.bounding_box()
        await search_btn.click()
        await page.wait_for_timeout(1000)
        await rec.step(page, "Suche geöffnet",
                       highlights=[{"type": "circle", "x": sb["x"], "y": sb["y"],
                                    "width": sb["width"], "height": sb["height"]}]
                       if sb else [])
        # Type in search field
        inp = page.locator("input[type='search'], input[placeholder*='Search'], input:visible").first
        if await inp.is_visible(timeout=2000):
            await inp.fill("")
            await inp.type("Meeting", delay=80)
            await page.wait_for_timeout(2000)
            await rec.step(page, "Suche: Meeting", highlights=[])
    else:
        # Try keyboard shortcut
        await page.keyboard.press("Control+F")
        await page.wait_for_timeout(1000)
        inp = page.locator("input:visible").first
        if await inp.is_visible():
            await inp.fill("")
            await inp.type("Meeting", delay=80)
            await page.wait_for_timeout(1000)
            await rec.step(page, "Suche über Tastatur", highlights=[])
        else:
            await rec.step(page, "Suche nicht verfügbar", highlights=[])

    return await rec.finish(page)


async def record_mail_read(context: BrowserContext) -> Path | None:
    rec = WorkflowRecorder("mail-read", VIDEO_DIR, GIF_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Mailview/0/view", 2000)
    await rec.step(page, "Mailinbox geoffnet", highlights=[])
    await page.wait_for_timeout(500)
    msg = page.locator("._mailSubject[ng-show], .mail-subject, [class*='mailSubject']").first
    if await msg.is_visible(timeout=3000):
        box = await msg.bounding_box()
        if box:
            await rec.step(page, "E-Mail auswahlen", highlights=[{"type": "circle", "x": box["x"], "y": box["y"], "width": box["width"], "height": box["height"]}])
        await msg.click()
        await page.wait_for_timeout(2000)
        await rec.step(page, "E-Mail Details angezeigt", highlights=[])
    return await rec.finish(page)


async def record_mail_folder_management(context: BrowserContext) -> Path | None:
    rec = WorkflowRecorder("mail-folder-management", VIDEO_DIR, GIF_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Mailview/0/view", 2000)
    await rec.step(page, "Mailinbox mit Ordnern", highlights=[])
    await page.wait_for_timeout(500)
    folder_list = await page.locator("._folderLink, .folder-item, [ng-click*='selectFolder']").all()
    if folder_list:
        first_folder = folder_list[1] if len(folder_list) > 1 else folder_list[0]
        if await first_folder.is_visible(timeout=2000):
            box = await first_folder.bounding_box()
            if box:
                await rec.step(page, "Anderen Ordner auswahlen", highlights=[{"type": "circle", "x": box["x"], "y": box["y"], "width": box["width"], "height": box["height"]}])
            await first_folder.click()
            await page.wait_for_timeout(2000)
            await rec.step(page, "Ordner-inhalt angezeigt", highlights=[])
    return await rec.finish(page)


async def record_mail_reply_forward_delete(context: BrowserContext) -> Path | None:
    rec = WorkflowRecorder("mail-reply-forward-delete", VIDEO_DIR, GIF_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Mailview/0/view", 2000)
    await rec.step(page, "Mailinbox geoffnet", highlights=[])
    await page.wait_for_timeout(500)
    msg = page.locator("._mailRow[ng-click], .mail-row").first
    if await msg.is_visible(timeout=3000):
        await msg.click()
        await page.wait_for_timeout(2000)
        await rec.step(page, "E-Mail ausgewahlt", highlights=[])
        reply_btn = page.locator("button:has-text('Reply'), button[title*='Reply']").first
        if await reply_btn.is_visible(timeout=2000):
            box = await reply_btn.bounding_box()
            if box:
                await rec.step(page, "Antwort-Button", highlights=[{"type": "circle", "x": box["x"], "y": box["y"], "width": box["width"], "height": box["height"]}])
            await reply_btn.click()
            await page.wait_for_timeout(2000)
            await rec.step(page, "Antwort-Fenster geoffnet", highlights=[])
        close_btn = page.locator("button:has-text('Close'), button[ng-click*='close']").first
        if await close_btn.is_visible(timeout=2000):
            await close_btn.click()
            await page.wait_for_timeout(1000)
        delete_btn = page.locator("button[title*='Delete'], button:has-text('Delete')").first
        if await delete_btn.is_visible(timeout=2000):
            db = await delete_btn.bounding_box()
            await rec.step(page, "Loschen-Button", highlights=[{"type": "circle", "x": db["x"], "y": db["y"], "width": db["width"], "height": db["height"]}] if db else [])
            await delete_btn.click()
            await page.wait_for_timeout(2000)
            await rec.step(page, "E-Mail geloscht", highlights=[])
    return await rec.finish(page)


async def record_password_change(context: BrowserContext) -> Path | None:
    rec = WorkflowRecorder("password-change", VIDEO_DIR, GIF_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await rec.step(page, "Einstellungen-Menu", highlights=[])
    await page.wait_for_timeout(500)
    settings_link = page.locator("a[href*='Preferences']").first
    if await settings_link.is_visible(timeout=3000):
        await settings_link.click()
        await page.wait_for_timeout(3000)
        await rec.step(page, "Einstellungen geoffnet", highlights=[])
        await page.wait_for_timeout(1000)
        await rec.step(page, "Passwortanderung in den Einstellungen (falls aktiviert)", highlights=[])
        await page.wait_for_timeout(500)
    return await rec.finish(page)


async def record_calendar_ical(context: BrowserContext) -> Path | None:
    rec = WorkflowRecorder("calendar-ical", VIDEO_DIR, GIF_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Calendar/view", 2000)
    await rec.step(page, "Kalenderansicht", highlights=[])
    await page.wait_for_timeout(1000)
    settings_btn = page.locator("button:has-text('Settings'), md-button:has-text('Einstellungen')").first
    if await settings_btn.is_visible(timeout=2000):
        box = await settings_btn.bounding_box()
        if box:
            await rec.step(page, "Einstellungen-Button", highlights=[{"type": "circle", "x": box["x"], "y": box["y"], "width": box["width"], "height": box["height"]}])
        await settings_btn.click()
        await page.wait_for_timeout(2000)
        await rec.step(page, "Einstellungen-Panel geoffnet", highlights=[])
        await page.wait_for_timeout(500)
        export_link = page.locator("a:has-text('Export'), a[href*='ical'], button:has-text('iCal')").first
        if await export_link.is_visible(timeout=2000):
            el = await export_link.bounding_box()
            await rec.step(page, "iCal/Export-Link fehlt (SOGo-Konfiguration)", highlights=[{"type": "circle", "x": el["x"], "y": el["y"], "width": el["width"], "height": el["height"]}] if el else [])
    return await rec.finish(page)


async def record_contacts_import_export(context: BrowserContext) -> Path | None:
    rec = WorkflowRecorder("contacts-import-export", VIDEO_DIR, GIF_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Contacts", 2000)
    await rec.step(page, "Kontaktliste", highlights=[])
    await page.wait_for_timeout(1000)
    menu_btn = page.locator("button:has-text('Actions'), md-button[ng-click*='menu']").first
    if await menu_btn.is_visible(timeout=2000):
        box = await menu_btn.bounding_box()
        if box:
            await rec.step(page, "Actions-Menubutton", highlights=[{"type": "circle", "x": box["x"], "y": box["y"], "width": box["width"], "height": box["height"]}])
        await menu_btn.click()
        await page.wait_for_timeout(1000)
        await rec.step(page, "Menugeoffnet", highlights=[])
        await page.wait_for_timeout(500)
        import_option = page.locator("md-menu-item:has-text('Import')").first
        if await import_option.is_visible(timeout=2000):
            io = await import_option.bounding_box()
            await rec.step(page, "Import-Option fehlt (SOGo-Konfiguration)", highlights=[{"type": "circle", "x": io["x"], "y": io["y"], "width": io["width"], "height": io["height"]}] if io else [])
        export_option = page.locator("md-menu-item:has-text('Export')").first
        if await export_option.is_visible(timeout=2000):
            eo = await export_option.bounding_box()
            await rec.step(page, "Export-Option fehlt (SOGo-Konfiguration)", highlights=[{"type": "circle", "x": eo["x"], "y": eo["y"], "width": eo["width"], "height": eo["height"]}] if eo else [])
    return await rec.finish(page)


# ── Runner ──

async def main() -> None:
    clean_dirs()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

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

        # Login once in a shared context (no video)
        login_context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            locale="en-US",
            ignore_https_errors=True,
        )
        login_page = await login_context.new_page()
        await login(login_page)
        # Extract cookies/storage state
        storage = await login_context.storage_state()
        await login_context.close()

        results = []
        for name, workflow_fn in workflows:
            print(f"\n── {name} ──")
            # Each workflow gets its own context for video recording
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
                    # Copy to assets
                    shutil.copy2(str(webp_path), str(ASSETS_DIR / webp_path.name))
                    meta_path = VIDEO_DIR / f"{name}_metadata.json"
                    if meta_path.exists():
                        import json
                        meta = json.loads(meta_path.read_text())
                        print(f"  ✓  {webp_path.name} — {meta['annotated_frames']} frames, {meta['webp_size_kb']}KB")
                        results.append((name, True, meta["annotated_frames"]))
                    else:
                        print(f"  ✓  {webp_path.name}")
                        results.append((name, True, 0))
                else:
                    print("  ✗  Failed")
                    results.append((name, False, 0))
            except Exception as e:
                print(f"  ✗  Error: {e}")
                results.append((name, False, 0))
            finally:
                await ctx.close()

        print("\n── Results ──")
        for name, ok, frames in results:
            mark = "✓" if ok else "✗"
            print(f"  {mark}  {name}: {frames} annotated frames")

        total_ok = sum(1 for _, ok, _ in results if ok)
        print(f"\n  {total_ok}/{len(results)} succeeded")

        # Copy legacy GIFs too if any
        for gif in sorted(GIF_DIR.glob("*.gif")):
            shutil.copy2(str(gif), str(ASSETS_DIR / gif.name))

        await browser.close()

    print("\n── All captures complete! ──")


if __name__ == "__main__":
    asyncio.run(main())
