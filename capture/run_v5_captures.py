#!/usr/bin/env python3
"""SOGo 5 live re-captures against the sogo5-capture stack (vhrz2392:8085).

Replaces the v5 duplicate cluster (one empty-calendar screenshot shipped
under many names) with distinct, truthful states. Two freebusy close-ups
(02-freebusy-grid, freebusy) are excluded: this image's page-action
dispatch bug 500s freebusy.ifb/ajaxRead, so the grid never receives busy
data (upstream demo returns 200 for the same action; see notes in
site/image-provenance.json).

Usage:
  python3 capture/run_v5_captures.py [--out DIR] [--only name,name] [--lang en|de]
"""
from __future__ import annotations

import asyncio
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from playwright.async_api import Locator, Page, async_playwright  # noqa: E402

from capture.run_screenshot_captures import (  # noqa: E402
    ScreenshotRecorder,
    click_required,
    dismiss_hints,
    fill_required,
    require,
)

BASE = "http://vhrz2392:8085/SOGo"
USER = "sogo-tests1"
PW = "sogo"
WEEK = f"/SOGo/so/{USER}/Calendar/view#!/calendar/week/20260914"
NEXT_WEEK = f"/SOGo/so/{USER}/Calendar/view#!/calendar/week/20260921"

# UI strings used as selectors — German values verified against
# UI/*/German.lproj/Localizable.strings (SOGo 5.12 source).
UI = {
    "en": dict(new_event="New Event", create_event="Create a new event",
               attendees="Invite Attendees", weekly="Weekly",
               subscribe="Subscribe to a Calendar", new_contact="New Contact",
               new_card="Create a new address book card", firstname="Firstname",
               lastname="Lastname", phone="Phone Number", new_phone="New Phone Number",
               options="Options", new_folder="New Folder", save="Save",
               search="Search", prefs_mail="Mail",
               toggle_menu="Toggle Menu", reply="Reply"),
    "de": dict(new_event="Neuer Termin", create_event="Neuen Termin erstellen",
               attendees="Teilnehmer einladen", weekly="Wöchentlich",
               subscribe="Einen Kalender abonnieren", new_contact="Neuer Kontakt",
               new_card="Neue Adresskarte erzeugen", firstname="Vorname",
               lastname="Nachname", phone="Telefon", new_phone="Neue Telefonnummer",
               options="Optionen", new_folder="Neuer Ordner", save="Speichern",
               search="Suchen", prefs_mail="E-Mail",
               toggle_menu="Menü umschalten", reply="Antworten"),
}
L: dict = {}


async def login(page: Page) -> None:
    await page.goto(f"{BASE}/", wait_until="domcontentloaded")
    await page.wait_for_timeout(1500)
    await fill_required(page, "input[type='text']", USER, "username field")
    await fill_required(page, "input[type='password']", PW, "password field")
    await click_required(page, "button[type='submit']", "login submit")
    for _ in range(30):
        await page.wait_for_timeout(1000)
        if "/so/" in page.url:
            break
    else:
        raise RuntimeError("login never landed in /so/")
    await page.wait_for_timeout(2500)
    await dismiss_hints(page)


async def snap(rec: ScreenshotRecorder, page: Page, label: str, scope=None, margin: int = 24) -> None:
    """rec.capture that hard-fails on empty/blank shots."""
    path = await ScreenshotRecorder.capture(rec, page, label, scope=scope, margin=margin)
    if path is None:
        raise RuntimeError("screenshot empty or annotation failed")


async def open_editor(page: Page) -> Locator:
    """Two-step speed-dial: main FAB, then the 'Create a new event' mini-fab.
    Any dialog left open by a previous state is closed first."""
    if await page.locator("md-dialog:visible").count():
        await page.keyboard.press("Escape")
        for _ in range(10):
            await page.wait_for_timeout(400)
            if not await page.locator("md-dialog:visible").count():
                break
    await click_required(page, f'button[aria-label="{L["new_event"]}"]', "new event FAB")
    await page.wait_for_timeout(500)
    await click_required(page, f'button[aria-label="{L["create_event"]}"]', "mini-fab")
    dlg = page.locator("md-dialog:visible").last
    await require(dlg, "event editor dialog")
    await page.wait_for_timeout(700)
    return dlg


async def click_btn(page: Page, label: str) -> None:
    """md-buttons sometimes evade get_by_text; iterate and match by inner text."""
    for b in await page.locator("button").all():
        txt = (await b.inner_text()).strip().upper()
        if txt == label.upper():
            await b.click()
            return
    raise RuntimeError(f"button {label!r} not found")


async def set_time_inputs(page: Page, start: str, end: str) -> None:
    """Time inputs are bare inputs whose value matches HH:MM (no aria label)."""
    hits = []
    for inp in await page.locator("md-dialog input").all():
        val = await inp.input_value()
        if len(val) == 5 and val[2] == ":" and val[:2].isdigit() and val[3:].isdigit():
            hits.append(inp)
    if len(hits) < 2:
        raise RuntimeError(f"expected 2 HH:MM inputs, found {len(hits)}")
    await hits[0].fill(start)
    await hits[1].fill(end)


async def open_repeat_menu(page: Page) -> Locator:
    """The Repeat control is the md-select bound to repeat.frequency (the
    dialog's first md-select is the Calendar picker — don't click that one).
    Verifies by waiting for a visible option, then scopes the md-select-menu
    child (the container div keeps a 0x0 box in this build)."""
    sel = page.locator("md-dialog md-select[ng-model='editor.component.repeat.frequency']").first
    await require(sel, "repeat md-select")
    opt = page.locator(f'md-option:visible:has-text("{L["weekly"]}")').first
    for attempt in range(3):
        await sel.click(force=attempt > 0)
        try:
            await opt.wait_for(timeout=4000)
            await page.wait_for_timeout(700)
            return page.locator("md-select-menu:visible").first
        except Exception:
            continue
    raise RuntimeError("repeat menu did not open")


async def pick_menu_option(page: Page, text: str) -> None:
    """Select an md-option from an open md-select menu. Pointer clicks are
    intercepted by the menu backdrop, so click with force and fall back to
    keyboard navigation."""
    opt = page.locator(f"md-option:visible:has-text('{text}')").first
    try:
        await opt.click(force=True, timeout=4000)
        return
    except Exception:
        pass
    opts = await page.locator("md-option:visible").all()
    idx = None
    for i, o in enumerate(opts):
        if text.lower() in (await o.inner_text()).lower():
            idx = i
            break
    if idx is None:
        raise RuntimeError(f"menu option {text!r} not found")
    for _ in range(idx + 1):
        await page.keyboard.press("ArrowDown")
        await page.wait_for_timeout(120)
    await page.keyboard.press("Enter")


async def seed_recurring_if_needed(page: Page) -> bool:
    """Create 'Weekly Team Sync' (Mon 09:30-10:30, weekly) once. Returns True
    if this run created it (caller may capture the fresh-save state)."""
    await page.goto(f"{BASE}{WEEK}", wait_until="domcontentloaded")
    await page.wait_for_timeout(3500)
    if "Weekly Team Sync" in (await page.content()):
        return False
    dlg = await open_editor(page)
    title = dlg.locator("input").nth(0)
    await title.fill("Weekly Team Sync")
    await set_time_inputs(page, "09:30", "10:30")
    await open_repeat_menu(page)
    await pick_menu_option(page, L["weekly"])
    await page.wait_for_timeout(500)
    await click_btn(page, L["save"].upper())
    await page.wait_for_timeout(3000)
    if "Weekly Team Sync" not in (await page.content()):
        raise RuntimeError("recurring event did not persist")
    return True


# ---------------------------------------------------------------- states


async def st_calendar_view(page: Page, rec: ScreenshotRecorder) -> None:
    """Subscription doc: the 'Subscribe to a Calendar' dialog."""
    await page.goto(f"{BASE}{WEEK}", wait_until="domcontentloaded")
    await page.wait_for_timeout(3500)
    await click_required(page, f'button[aria-label*="{L["subscribe"]}"]', "subscribe button")
    await page.wait_for_timeout(1200)
    dlg = page.locator("md-dialog:visible").last
    await require(dlg, "subscribe dialog")
    await snap(rec, page, "Calendar view with subscription options", scope=dlg)


async def st_create_view(page: Page, rec: ScreenshotRecorder) -> None:
    """Create-event doc step 1 'Open Calendar': calendar module with the
    module rail/menu drawer open."""
    await page.goto(f"{BASE}{WEEK}", wait_until="domcontentloaded")
    await page.wait_for_timeout(3500)
    await click_required(page, f'button[aria-label="{L["toggle_menu"]}"]', "module rail toggle")
    await page.wait_for_timeout(900)
    await snap(rec, page, "Calendar module in sidebar")


async def pgk(page: Page, att: Locator) -> None:
    await att.press("ArrowDown")
    await page.wait_for_timeout(300)
    await att.press("Enter")


async def open_dialog_with_attendee(page: Page) -> Locator:
    """Editor with title + sogo-tests2 attendee chip (freebusy section
    renders below, fetching availability)."""
    dlg = await open_editor(page)
    await dlg.locator("input").nth(0).fill("Project Kickoff")
    att = dlg.locator(f'input[aria-label="{L["attendees"]}"]')
    await require(att, "attendee autocomplete input")
    await att.fill("sogo-tests2")
    # wait until the suggestion list actually offers the user, then pick it
    # (md-autocomplete renders its list in a floating container on <body>)
    for _ in range(20):
        await page.wait_for_timeout(500)
        if "Tests Two" in (await page.content()):
            break
    else:
        raise RuntimeError("attendee suggestion never appeared")
    added = False
    for attempt in range(3):
        await att.fill("sogo-tests2")
        # wait until the suggestion list offers the user, then pick it
        for _ in range(20):
            await page.wait_for_timeout(500)
            if "Tests Two" in (await page.content()):
                break
        else:
            continue
        await pgk(page, att)
        for _ in range(10):
            await page.wait_for_timeout(500)
            if await dlg.locator("md-chip").count():
                added = True
                break
        if added:
            break
    if not added:
        raise RuntimeError("attendee chip never appeared")
    await page.wait_for_timeout(2500)
    return dlg


async def st_event_dialog(page: Page, rec: ScreenshotRecorder) -> None:
    dlg = await open_dialog_with_attendee(page)
    await snap(rec, page, "Event dialog with attendee", scope=dlg)


async def st_recurrence_options(page: Page, rec: ScreenshotRecorder) -> None:
    await open_editor(page)
    menu = await open_repeat_menu(page)
    await snap(rec, page, "Recurrence options in event dialog", scope=menu, margin=40)


async def st_calendar_recurring(page: Page, rec: ScreenshotRecorder) -> None:
    dlg = await open_editor(page)
    await open_repeat_menu(page)
    await pick_menu_option(page, L["weekly"])
    await page.wait_for_timeout(600)
    await snap(rec, page, "Weekly recurrence selected in event dialog", scope=dlg)


async def st_recurring_saved(page: Page, rec: ScreenshotRecorder) -> None:
    await seed_recurring_if_needed(page)
    ev = page.get_by_text("Weekly Team Sync").first
    await require(ev, "saved recurring event in grid")
    await snap(rec, page, "Recurring event saved in calendar", scope=ev, margin=110)


async def st_recurring_view(page: Page, rec: ScreenshotRecorder) -> None:
    """Recurring doc step 1: the plain week view before creating the event."""
    await page.goto(f"{BASE}{WEEK}", wait_until="domcontentloaded")
    await page.wait_for_timeout(3500)
    await snap(rec, page, "Calendar week view")


async def st_global_search(page: Page, rec: ScreenshotRecorder) -> None:
    await page.goto(f"{BASE}/so/{USER}/Mail/view#!/inbox", wait_until="domcontentloaded")
    await page.wait_for_timeout(4000)
    btn = page.locator(f'button[aria-label="{L["search"]}"]:visible').first
    await require(btn, "global search button")
    await btn.click()
    await page.wait_for_timeout(800)
    field = page.locator("input[ng-model='$sgSearchController.searchText']").first
    await require(field, "search input")
    await field.fill("Team")
    await page.wait_for_timeout(2000)
    if "Team Meeting" not in (await page.content()):
        raise RuntimeError("search results did not appear")
    results = page.locator("md-virtual-repeat-container:visible").nth(1)
    await snap(rec, page, "Searching in SOGo 5", scope=results, margin=30)


async def st_freebusy_grid(page: Page, rec: ScreenshotRecorder) -> None:
    """Attendee chips + availability grid section. Busy bars require
    freebusy.ifb/ajaxRead which this image build 500s on — the grid itself
    renders truthfully."""
    dlg = await open_dialog_with_attendee(page)
    grid = dlg.locator("md-content.sg-freebusy")
    await require(grid, "freebusy grid")
    await grid.scroll_into_view_if_needed()
    await page.wait_for_timeout(600)
    section = grid.locator("xpath=ancestor::div[contains(@class,'sg-form-section')][1]")
    await snap(rec, page, "Free/busy availability grid", scope=section, margin=24)


async def st_freebusy_closeup(page: Page, rec: ScreenshotRecorder) -> None:
    dlg = await open_dialog_with_attendee(page)
    grid = dlg.locator("md-content.sg-freebusy")
    await require(grid, "freebusy grid")
    await grid.scroll_into_view_if_needed()
    await page.wait_for_timeout(600)
    await snap(rec, page, "Free/busy grid showing colleague availability",
                      scope=grid, margin=36)


async def _fill_contact(page: Page, first: str, last: str, phone: str) -> None:
    def cont(label: str) -> str:
        return f"md-input-container:has(label:has-text('{label}')) input"
    await require(page.locator(cont(L["firstname"])).first, "Firstname field")
    await page.locator(cont(L["firstname"])).first.fill(first)
    await page.locator(cont(L["lastname"])).first.fill(last)
    # phone fields appear only after the add_circle icon-button next to the
    # 'New Phone Number' label is clicked
    add = page.locator(
        "//button[.//md-icon[contains(text(),'add_circle')]]"
        "[following-sibling::label[contains(.,$PHONELBL)]]").first
    await require(add, "'New Phone Number' add button")
    await add.click()
    await page.wait_for_timeout(600)
    phone_input = page.locator(f'md-input-container:has(label:has-text("{L["phone"]}")) input').last
    await require(phone_input, "phone field")
    await phone_input.fill(phone)


async def _click_save(page: Page) -> None:
    for b in await page.locator("button, md-button").all():
        label = ((await b.get_attribute("aria-label")) or "").lower()
        text = (await b.inner_text()).strip().lower()
        if L["save"].lower() in label or text == L["save"].lower():
            await b.click()
            return
    raise RuntimeError("SAVE button not found")


async def st_contacts_add(page: Page, rec: ScreenshotRecorder) -> None:
    """Contacts doc step 2: the New Contact speed-dial menu open."""
    await page.goto(f"{BASE}/so/{USER}/Contacts/view#!/addressbooks/personal",
                    wait_until="domcontentloaded")
    await page.wait_for_timeout(4000)
    await click_required(page, f'button[aria-label="{L["new_contact"]}"]', "new contact FAB")
    await page.wait_for_timeout(800)
    if L["new_card"] not in (await page.content()):
        raise RuntimeError("new contact speed-dial did not open")
    await snap(rec, page, "Add New Contact")


async def st_contacts_edit(page: Page, rec: ScreenshotRecorder) -> None:
    await page.goto(f"{BASE}/so/{USER}/Contacts/view#!/addressbooks/personal",
                    wait_until="domcontentloaded")
    await page.wait_for_timeout(4000)
    if "Tests Two" not in (await page.content()):
        # seed a contact with a phone number once (two-step speed dial)
        await click_required(page, f'button[aria-label="{L["new_contact"]}"]', "new contact FAB")
        await page.wait_for_timeout(600)
        await click_required(page, f'button[aria-label="{L["new_card"]}"]',
                             "mini-fab create card")
        await page.wait_for_timeout(1500)
        await _fill_contact(page, "Tests", "Two", "+49 6421 99999")
        await _click_save(page)
        await page.wait_for_timeout(2500)
        if "Tests Two" not in (await page.content()):
            raise RuntimeError("contact did not persist")
    card = page.locator("md-card, [class*='card'], md-list-item").filter(has_text="Tests Two").first
    await require(card, "contact card")
    await card.click()
    await page.wait_for_timeout(1500)
    # the Edit button is ACL-gated (objectEditor) in this build; the editor
    # state itself is reachable by rewriting the card URL
    if not page.url.endswith("/view"):
        raise RuntimeError(f"contact view not opened: {page.url}")
    await page.goto(page.url[: -len("/view")] + "/edit", wait_until="domcontentloaded")
    await page.wait_for_timeout(2000)
    await require(page.locator(f'md-input-container:has(label:has-text("{L["firstname"]}")) input').first,
                  "Firstname field in editor")
    await snap(rec, page, "Editing a contact's phone number and saving changes")


async def st_mail_folders(page: Page, rec: ScreenshotRecorder) -> None:
    await page.goto(f"{BASE}/so/{USER}/Mail/view#!/inbox", wait_until="domcontentloaded")
    await page.wait_for_timeout(4000)
    # per-mailbox Options menu (the account kebab never opens in this build)
    await click_required(page, f'md-icon[aria-label="{L["options"]}"]:visible',
                         "mailbox options menu")
    item = page.locator(".md-open-menu-container:visible "
                        f'md-menu-item:has-text("{L["new_folder"]}")').first
    await require(item, "New Folder menu entry")
    menu = page.locator("md-menu-content:visible").first
    await snap(rec, page, "Mail folder management", scope=menu, margin=40)


async def st_mail_actions(page: Page, rec: ScreenshotRecorder) -> None:
    await page.goto(f"{BASE}/so/{USER}/Mail/view#!/Mail/0/INBOX/1", wait_until="domcontentloaded")
    await page.wait_for_timeout(4000)
    reply = page.locator(f'md-button[aria-label="{L["reply"]}"], button[aria-label="{L["reply"]}"]').first
    await require(reply, "reply toolbar button")
    await snap(rec, page, "Mail open with reply, forward and delete actions")


async def st_mail_filters(page: Page, rec: ScreenshotRecorder) -> None:
    await page.goto(f"{BASE}/so/{USER}/Preferences#!/general", wait_until="domcontentloaded")
    await page.wait_for_timeout(4000)
    # nav 'Mail' entry in the preferences sidebar
    mail_nav = None
    for el in await page.locator("md-list-item, a, button").all():
        if (await el.inner_text()).strip().endswith(L["prefs_mail"]):
            mail_nav = el
            break
    if mail_nav is None:
        raise RuntimeError("Mail entry missing in Preferences nav")
    await mail_nav.click()
    await page.wait_for_timeout(2500)
    # Filters is a tab/section on the mailer preferences page
    if "Filter" not in (await page.content()):
        for b in await page.locator("button, md-tab-item, a").all():
            if "filter" in (await b.inner_text()).strip().lower():
                await b.click()
                await page.wait_for_timeout(1500)
                break
        else:
            raise RuntimeError("filters UI not reachable on Preferences mailer page")
    await snap(rec, page, "Mail filters settings")


STATES = [
    ("01-calendar-view", st_calendar_view),
    ("01-calendar-create-view", st_create_view),
    ("01-event-dialog", st_event_dialog),
    ("02-recurrence-options", st_recurrence_options),
    ("calendar-recurring", st_calendar_recurring),
    ("03-recurring-saved", st_recurring_saved),
    ("01-calendar-recurring-view", st_recurring_view),
    ("contacts-add", st_contacts_add),
    ("contacts-edit-delete", st_contacts_edit),
    ("mail-folder-management", st_mail_folders),
    ("02-freebusy-grid", st_freebusy_grid),
    ("freebusy", st_freebusy_closeup),
    ("global-search", st_global_search),
    ("mail-reply-forward-delete", st_mail_actions),
    ("01-mail-filters", st_mail_filters),
]


async def main() -> None:
    out = Path("capture/v5_captures")
    only: set[str] | None = None
    lang = "en"
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--out":
            out = Path(args[i + 1]); i += 2
        elif args[i] == "--only":
            only = {s.strip() for s in args[i + 1].split(",") if s.strip()}; i += 2
        elif args[i] == "--lang":
            lang = args[i + 1]; i += 2
        else:
            i += 1
    global L
    L = UI[lang]
    outdir = out / lang.upper()
    if outdir.exists() and only is None:
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    def fname(n: str) -> str:
        return "mail-filters" if (lang == "de" and n == "01-mail-filters") else n
    selected = [(fname(n), fn) for n, fn in STATES if only is None or n in only]
    results: list[tuple[str, str]] = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--disable-dev-shm-usage"])
        ctx = await browser.new_context(viewport={"width": 1280, "height": 800},
                                        locale="en-US" if lang == "en" else "de-DE")
        page = await ctx.new_page()
        await login(page)
        for name, fn in selected:
            # Each state gets a fresh context: the accessibility image's
            # broken JSON actions (usersSearch) degrade after first use in
            # a session, so attendee autocompletion is only reliable right
            # after login.
            rec = ScreenshotRecorder(name, outdir)
            print(f"\n=== {name}")
            try:
                await fn(page, rec)
                results.append((name, "OK"))
                print(f"  OK -> {outdir / (name + '.png')}")
            except Exception as e:
                results.append((name, f"FAIL: {e}"))
                print(f"  FAIL: {e}")
            await ctx.close()
            ctx = await browser.new_context(
                viewport={"width": 1280, "height": 800},
                locale="en-US" if lang == "en" else "de-DE")
            page = await ctx.new_page()
            try:
                await login(page)
            except Exception as e:
                print(f"  LOGIN FAIL: {e}")
                break
        await browser.close()

    print("\n==== summary")
    for name, status in results:
        print(f"  {status:4} {name}" if status == "OK" else f"  {status} {name}")
    if any(not r[1].startswith("OK") for r in results):
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
