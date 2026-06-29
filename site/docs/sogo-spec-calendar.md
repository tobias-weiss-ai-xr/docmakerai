---
title: "Calendar — Spec-Based Guide"
description: "Spec-based guide covering SOGo calendar module workflows including event creation, recurring events, sharing, subscriptions, and free/busy lookup."
sidebar_label: "Calendar Specification Guide"
---

import PageSEO from '@site/src/components/PageSEO';

<PageSEO title="Calendar — Spec-Based Guide" description="Spec-based guide covering SOGo calendar module workflows including event creation, recurring events, sharing, subscriptions, and free/busy lookup." keywords="SOGo 5, calendar, events, recurring, sharing, iCal, free/busy, spec" />

# SOGo Calendar

Capture SOGo calendar module workflows as annotated WebP animations for the
user guide. Covers event creation, recurring events, editing, deletion, view
switching, sharing, subscriptions, free/busy scheduling, and iCal import/export.

## Prerequisites

- authenticated session and the calendar in week view
- event dialog is open
- The calendar module is open
- existing calendar event exists
- calendar exists in the user's account
- event dialog with attendees is open
- calendar exists with events

## Step-by-Step Instructions

### Calendar Event Creation

The capture pipeline will record the workflow for creating a new calendar
event via double-click on a time slot, filling the event dialog, and saving.

#### Step 1: Double-click the time slot at Monday 10:00

The user double-clicks the time slot at Monday 10:00

**Expected result:**

- the event dialog will open
- the title and location fields will be filled
- the event will be saved
- the workflow will produce an annotated WebP with step indicators and UI highlights

#### Step 2: The double-click action occurs

The double-click action occurs

**Expected result:**

- red circle highlights will mark the day cell and hour cell
- a step header will display "Doppelklick auf Montag 10:00"

:::tip
During recording the system automatically overlays step headers and UI highlights (red circles, arrows) on each frame.
:::

### Recurring Events

The capture pipeline will record creating a weekly recurring event series.

#### Step 1: The repeat dropdown is set to "Weekly"

The repeat dropdown is set to "Weekly"

**Expected result:**

- the event will be saved as a recurring series
- the resulting calendar will show the repeating pattern
- the WebP will annotate the repeat selection and saved series

### Calendar Views

The capture pipeline will record switching between calendar view modes
(day, week, month).

#### Step 1: Click the view selector buttons

The user clicks the view selector buttons

**Expected result:**

- the calendar will transition between day, week, and month views
- each transition will be captured as an annotated frame

### Event Edit and Delete

The capture pipeline will record editing an existing event and deleting it.

#### Step 1: Click the event to open the dialog

The user clicks the event to open the dialog

**Expected result:**

- the title will be modified and saved
- the event will then be deleted via the delete action
- the WebP will show both the edit and delete steps

### Calendar Sharing

The capture pipeline will record sharing a calendar with another user.

#### Step 1: Open the sharing dialog

The user opens the sharing dialog

**Expected result:**

- a recipient will be added with permissions
- the sharing will be confirmed
- the WebP will annotate the sharing workflow

### Calendar Subscription

The capture pipeline will record subscribing to an external iCal calendar feed.

#### Step 1: Open the subscription dialog

The user opens the subscription dialog

**Expected result:**

- an iCal URL will be entered
- the subscription will be confirmed
- the subscribed calendar will appear in the sidebar

### Free/Busy Scheduling

The capture pipeline will record scheduling a meeting using the free/busy grid.

#### Step 1: The free/busy grid is displayed

The free/busy grid is displayed

**Expected result:**

- attendee availability will be visible
- a suitable time slot will be selected
- the WebP will annotate the grid interaction

### iCal Import/Export

The capture pipeline will record importing and exporting calendar data via iCal format.

#### Step 1: Select the export option

The user selects the export option

**Expected result:**

- an iCal file will be downloaded
- the WebP will show the export workflow

## Troubleshooting

8 workflows produce blank captures (see capture-pipeline spec for reliability requirements)

## Related Sections

- [Auth Session](./sogo-spec-auth-session)

## Implementation Reference

Source: `capture/run_captures.py` — `record_calendar_create_event()`, `record_calendar_recurring()`, `record_calendar_views()`, `record_calendar_edit_delete()`, `record_calendar_share()`, `record_calendar_subscribe()`, `record_freebusy()`, `record_calendar_ical()`

## Appendix: Scenario Reference

| Scenario: Description | Precondition | Action | Expected Result |
|---|---|---|---|
| Create event via double-click | an authenticated session and the calendar in week view | the user double-clicks the time slot at Monday 10:00 | the event dialog will open |
| Annotation markers | the calendar create event workflow is being recorded | the double-click action occurs | red circle highlights will mark the day cell and hour cell |
| Weekly recurrence | an event dialog is open | the repeat dropdown is set to "Weekly" | the event will be saved as a recurring series |
| View switching | the calendar module is open | the user clicks the view selector buttons | the calendar will transition between day, week, and month views |
| Edit then delete | an existing calendar event exists | the user clicks the event to open the dialog | the title will be modified and saved |
| Share with user | a calendar exists in the user's account | the user opens the sharing dialog | a recipient will be added with permissions |
| Subscribe to iCal feed | the calendar module is open | the user opens the subscription dialog | an iCal URL will be entered |
| Schedule with attendees | an event dialog with attendees is open | the free/busy grid is displayed | attendee availability will be visible |
| Export calendar | a calendar exists with events | the user selects the export option | an iCal file will be downloaded |
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

