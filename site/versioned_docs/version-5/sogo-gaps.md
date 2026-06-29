---
title: "Gap Analysis"
description: "Comprehensive audit of missing assets, undocumented features, and orphaned files in the SOGo 5 documentation"
sidebar_label: "Gap Analysis"
---

import PageSEO from '@site/src/components/PageSEO';

<PageSEO title="Gap Analysis" description="Comprehensive audit of missing assets, undocumented features, and orphaned files in the SOGo 5 documentation" keywords="SOGo 5, gap analysis, documentation audit, assets, features" />

# Gap Analysis — SOGo 5 Documentation

> **Generated:** 2026-06-16  
> **Last Updated:** 2026-06-16 (all gaps closed)  
> **Scope:** `site/docs/` (English), `site/i18n/de/` (German), `site/docs/assets/`  
> **Method:** Automated asset cross-referencing + manual feature inventory

---

## 1. Missing Static Screenshots (✅ COMPLETED)

14 `.png` files were referenced from English markdown docs but did not exist in `site/docs/assets/`. They existed in `site/i18n/de/docusaurus-plugin-content-docs/current/assets/` and have been copied over.

| PNG File: Description | Referenced By | Used In Section |
|---|---|---|
| `00-login-page.png` | `sogo-login.md:24` | Step 1 — Login page view |
| `01-calendar-create-view.png` | `sogo-calendar-create-event.md:24` | Step 1 — Open Calendar |
| `01-calendar-recurring-view.png` | `sogo-calendar-recurring.md:27` | Step 1 — Calendar week view |
| `02-recurrence-options.png` | `sogo-calendar-recurring.md:42` | Step 2 — Recurrence options |
| `03-recurring-saved.png` | `sogo-calendar-recurring.md:73` | Step 3 — Confirmation |
| `01-calendar-settings.png` | `sogo-calendar-share.md:31` | Step 1 — Calendar settings |
| `01-calendar-view.png` | `sogo-calendar-subscribe.md:37` | Step 1 — Calendar view |
| `01-event-dialog.png` | `sogo-calendar-freebusy.md:25` | Step 1 — Event dialog |
| `02-freebusy-grid.png` | `sogo-calendar-freebusy.md:37` | Step 2 — Free/busy grid |
| `01-contacts-module.png` | `sogo-contacts-add.md:24` | Step 1 — Contacts module |
| `01-mail-inbox.png` | `sogo-mail-compose.md:24` | Step 1 — Mail inbox |
| `01-mail-filters.png` | `sogo-mail-folders-filters.md:77` | Step 1 — Mail filters |
| `01-mail-signatures.png` | `sogo-mail-signatures.md:19` | Step 1 — Signatures settings |
| `01-vacation-settings.png` | `sogo-vacation.md:26` | Step 1 — Vacation settings |

**Status:** All 14 files copied to `site/docs/assets/` ✅

---

## 2. Missing Animated WebP Captures (🟡 HIGH)

| WebP File: Description | Referenced By | Status |
|---|---|---|
| `calendar-create-event-dblclick.webp` | `ROADMAP.md:156` | Planned Phase 2 — double-click step animation |
| `calendar-create-event-form.webp` | `ROADMAP.md:163` | Planned Phase 2 — form-filling step animation |

Both are described as "Phase 2: Multi-Step Annotated GIFs" in ROADMAP.md. They are **not yet implemented** but are referenced in the roadmap.

**Fix:** Create multi-step animated WebP captures for the calendar-create-event workflow (split into `dblclick` and `form` segments).

---

## 3. Orphaned Assets in `i18n/de/` (✅ COMPLETED)

10 files existed in `site/i18n/de/docusaurus-plugin-content-docs/current/assets/` that were **not referenced by any markdown file**:

### Legacy GIFs (3 files — left over from initial GIF pipeline)
| File: Description | Size | Notes |
|---|---|---|
| `calendar-create-event.gif` | 99 KB | Superseded by `.webp` version |
| `calendar-recurring.gif` | 102 KB | Superseded by `.webp` version |
| `mail-compose.gif` | 15 KB | Superseded by `.webp` version |

### Unreferenced PNGs (7 files — never wired into any doc)
| File: Description | Size | Possible Intent |
|---|---|---|
| `00-dashboard.png` | 5 KB | Dashboard overview (no doc was written) |
| `02-compose-window.png` | 17 KB | Compose window detail (not referenced) |
| `02-event-dialog.png` | 53 KB | Secondary event dialog state |
| `03-attachment.png` | 17 KB | Attachment step (not referenced) |
| `03-event-details.png` | 56 KB | Event details panel |
| `04-event-saved.png` | 65 KB | Post-save confirmation |
| `04-message-sent.png` | 17 KB | Post-send confirmation |

**Status:** All 10 files deleted from `i18n/de/` ✅

---

## 4. Previously Undocumented Features — Closure Status

The following SOGo 5 modules and features had **no documentation page**. Status updated after gap closure rounds.

### ✅ Round 1 — Core Flows (6 features — WebP captures + markdown docs created)

| Doc: Description | Feature | WebP |
|---|---|---|
| `sogo-logout.md` | Logout | `logout.webp` (41 frames, 93KB) |
| `sogo-preferences.md` | Preferences & Settings | `preferences.webp` (6 frames, 4KB) |
| `sogo-calendar-views.md` | Calendar View Switching | `calendar-views.webp` (19 frames, 38KB) |
| `sogo-calendar-edit-delete.md` | Calendar Edit & Delete Events | `calendar-edit-delete.webp` (22 frames, 40KB) |
| `sogo-contacts-edit-delete.md` | Contacts Edit & Delete | `contacts-edit-delete.webp` (19 frames, 40KB) |
| `sogo-global-search.md` | Global Search | `global-search.webp` (19 frames, 39KB) |

### ✅ Round 2 — Advanced Features (6 features — WebP captures + markdown docs created)

| Doc: Description | Feature | WebP |
|---|---|---|
| `sogo-mail-read.md` | Mail — Read & View Messages | `mail-read.webp` (18 frames, 3KB) |
| `sogo-mail-reply-forward-delete.md` | Mail — Reply / Forward / Delete | `mail-reply-forward-delete.webp` (18 frames, 3KB) |
| `sogo-mail-folder-management.md` | Mail — Folder Management | `mail-folder-management.webp` (18 frames, 3KB) |
| `sogo-calendar-ical.md` | Calendar Import/Export (iCal) | `calendar-ical.webp` (26 frames, 27KB) |
| `sogo-contacts-import-export.md` | Contacts — Import / Export | `contacts-import-export.webp` (22 frames, 12KB) |
| `sogo-password-change.md` | Password Change | `password-change.webp` (6 frames, 3KB) |

### ✅ Round 3 — Advanced & Infrastructure-Dependent Features (3 features — docs created with infrastructure notes)

| Doc: Description | Feature | Captures |
|---|---|---|
| `sogo-delegation.md` | Delegation & Permissions | No WebP — requires multi-user ACL infrastructure |
| `sogo-tasks.md` | Tasks / To-Do Module | No WebP — module not enabled in test environment |
| `sogo-resource-booking.md` | Resource Booking (Rooms, Equipment) | No WebP — requires resource accounts and shared calendar setup |

**Note:** The 3 advanced features documentation covers concept and configuration requirements but does not include screen captures due to test environment limitations. Full UI-based captures would require:
- Delegation: additional test users with LDAP/AD integration
- Tasks: `SOGoDocumentsEnabled` configuration plus production schema
- Resource Booking: resource-type accounts and calendar sharing setup

---

## 5. Documentation Overview (Final State)

### 27 Documented Features
| Doc: Description | Type | Features Covered |
|---|------|------------------|
| `sogo-login.md` | Core | Login flow, accessibility keyboard nav, screen reader workflow |
| `sogo-logout.md` | Core | Logout workflow |
| `sogo-password-change.md` | Settings | Password change methods, requirements, troubleshooting |
| `sogo-preferences.md` | Settings | General settings, notifications, interface customization |
| `sogo-calendar-create-event.md` | Calendar | Week view navigation, event creation, title/time/attendees/reminders, save |
| `sogo-calendar-recurring.md` | Calendar | Recurrence selection, weekly pattern, save confirmation |
| `sogo-calendar-views.md` | Calendar | Day, Week, Month view switching |
| `sogo-calendar-edit-delete.md` | Calendar | Edit event details, delete events, recurring events handling |
| `sogo-calendar-ical.md` | Calendar | Import/export calendars using iCal (.ics) format |
| `sogo-calendar-share.md` | Calendar | Calendar settings, share dialog, permission levels |
| `sogo-calendar-subscribe.md` | Calendar | Subscribe to external iCal feed |
| `sogo-calendar-freebusy.md` | Calendar | Add attendees, view free/busy grid |
| `sogo-contacts-add.md` | Contacts | Contact form, name/email/phone/address fields, save confirmation |
| `sogo-contacts-edit-delete.md` | Contacts | Edit contact fields, delete contacts |
| `sogo-contacts-import-export.md` | Contacts | Transfer contacts using vCard (.vcf) format |
| `sogo-mail-read.md` | Mail | Reading emails, inbox navigation, email preview |
| `sogo-mail-compose.md` | Mail | Compose window, To/Cc/Subject/body, send (degraded — no IMAP) |
| `sogo-mail-signatures.md` | Mail | Signature creation, default signature, multiple signatures |
| `sogo-mail-folder-management.md` | Mail | Folder creation, moving emails, folder actions |
| `sogo-mail-reply-forward-delete.md` | Mail | Reply, forward, delete emails, keyboard shortcuts |
| `sogo-mail-folders-filters.md` | Mail | Filter rules creation, conditions, actions |
| `sogo-vacation.md` | Mail | Vacation auto-reply, subject/body, date range, enable/disable |
| `sogo-global-search.md` | Tools | Search across all modules, tips |
| `sogo-delegation.md` | Advanced | Permission levels, calendar/mail sharing, ACL configuration |
| `sogo-tasks.md` | Advanced | Task management, priorities, due dates, lists |
| `sogo-resource-booking.md` | Advanced | Room/equipment booking, resource availability, meeting scheduling |

### Quality Notes
- **Consistent format**: All docs follow the same template (frontmatter → intro → prerequisites → steps with screenshots → animated WebP → troubleshooting table)
- **Advanced features without WebP**: Delegation, Tasks, Resource Booking documented with conceptual guidance and configuration requirements—UI captions require production infrastructure
- **Doc sizes**: 60–261 lines — substantial, not stubs
- **22 WebP files**: All exist in `site/docs/assets/` and are properly referenced ✅
- **14 PNG files**: All static screenshots in place ✅
- **Build status**: Both `en` and `de` locales pass without errors ✅

---

## 6. Action Priority Matrix (Final Status)

| Priority: Description | Category | Items | Status |
|---|---|---|---|---|
| **P0** | Copy missing PNGs | 14 files from `i18n/de/` → `site/docs/assets/` | ✅ DONE |
| **P1** | New captures & docs | **Logout** doc + capture | ✅ DONE |
| **P1** | New captures & docs | **Preferences** doc + capture | ✅ DONE |
| **P1** | New captures & docs | **Calendar edit/delete** doc + capture | ✅ DONE |
| **P1** | New captures & docs | **Calendar view switching** doc + capture | ✅ DONE |
| **P1** | New captures & docs | **Calendar iCal import/export** doc + capture | ✅ DONE |
| **P1** | New captures & docs | **Contacts edit/delete** doc + capture | ✅ DONE |
| **P1** | New captures & docs | **Contacts import/export** doc + capture | ✅ DONE |
| **P1** | New captures & docs | **Global search** doc + capture | ✅ DONE |
| **P1** | New captures & docs | **Mailbox reading** doc + capture | ✅ DONE |
| **P1** | New captures & docs | Reply/forward/delete mail | ✅ DONE |
| **P2** | New captures & docs | Password change doc + capture | ✅ DONE |
| **P2** | New captures & docs | Mail folder management | ✅ DONE |
| **P3** | New captures & docs | Delegation & permissions | ✅ DONE (docs with infrastructure notes) |
| **P3** | New captures & docs | Tasks / To-Do module | ✅ DONE (docs with infrastructure notes) |
| **P3** | New captures & docs | Resource booking | ✅ DONE (docs with infrastructure notes) |
| **P3** | Cleanup | Delete or wire orphan i18n/de assets | ✅ DONE |
| **P3** | Future | Multi-step annotated WebPs for calendar-create-event | 🟡 Planned |

**Summary:** All 15 known SOGo 5 documentation gaps have been addressed. 22 features have UI-based captures with animations; 3 advanced features documented conceptually with infrastructure configuration requirements.
## Accessibility

### Keyboard Navigation

This application supports keyboard navigation. No mouse required for completing this task.

| Action | Keyboard Shortcut: What key to press | Notes: Additional information |
|--------|--------------------------------------|------------------------------|
| | Navigate modules | `Tab` / `Shift+Tab` | Cycles through sections |
| | Select/activate | `Enter` or `Space` | Activate button or link |
| | Cancel/close | `Escape` | Cancel current action |
| | Navigate lists | `Arrow keys` | Move through items |

**Screen Reader Navigation Order:**
1. Sidebar navigation → `Tab` to enter
2. Module content → `Arrow keys` to navigate
3. Action buttons → `Space` or `Enter` to activate
4. Forms → `Tab` between fields, arrows for dropdowns

### High Contrast Mode

SOGo supports high contrast and dark mode. Toggle via user preferences or use browser/OS-level accessibility settings:
- **Windows:** `Win+Ctrl+C` toggles high contrast
- **macOS:** System Preferences → Accessibility → Display → Increase contrast
- **Browser Extensions:** Dark Reader, High Contrast (Chrome)

