---
title: "Calendar — Import & Export (iCal)"
description: "Import and export calendars using iCal (.ics) format in SOGo 5"
sidebar_label: "Import & Export (iCal)"
---

import PageSEO from '@site/src/components/PageSEO';

<PageSEO title="Calendar — Import & Export (iCal)" description="Step-by-step tutorial to import and export calendars using iCal (.ics) format in SOGo 5" keywords={["ical", "import", "export", "ics", "calendar sharing"]} />

# Calendar — Import & Export (iCal)

Share your calendar with others by exporting it as an iCal file, or import calendars from other applications into SOGo.

## Prerequisites

- A SOGo 5 account with valid credentials
- You are logged into SOGo 5

## Step-by-Step Instructions

### Step 1: Open the Calendar Module

In the sidebar navigation on the left, click **Calendar** to open the calendar view.

### Step 2: Access Calendar Settings

Click the **three-dot menu** (⋯) in the calendar toolbar.


### Step 3: Export Your Calendar

1. Open the settings of the desired calendar via the three-dot menu
2. Choose the export option — the calendar is downloaded as an `.ics` (iCal) file

### Step 4: Import a Calendar

1. Click the **Import** button in the calendar settings
2. Select the `.ics` file you want to import
3. Choose the target calendar for the import
4. Click **Import** to begin

:::info
iCal (`.ics`) is a standard calendar file format supported by most calendar applications including Google Calendar, Microsoft Outlook, and Apple Calendar.
:::

## Import Options

| Option | Description | Use When |
|--------|--------------|---------|
| **Add all events** | Imports all events from the file | First-time import |
| **Merge duplicates** | Skips events with same date and title | Update existing calendar |
| **Update existing** | Replaces events with matching times | Refreshing a shared calendar |

:::warning
Importing a calendar with hundreds of events may take several minutes. Do not close the page while the import is processing.
:::

## Sharing via iCal

To subscribe to your calendar from another application (e.g., on your phone), you need the calendar URL:

1. Open the settings of the desired calendar via the three-dot menu
2. You will find the calendar URL there under **Links to this calendar** — not in the export dialog
3. Share the URL with others; they can use it to subscribe to your calendar in their own application

## Troubleshooting

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Import button not visible | Calendar sharing not enabled | Contact your administrator to enable sharing |
 | Import fails | Invalid `.ics` file format | Verify the file opens in a calendar application first |
| Export file is empty | Calendar has no events | Add events to the calendar before exporting |
## Accessibility

### Keyboard Navigation

This application supports keyboard navigation. No mouse required for completing this task.

| Action | Keyboard Shortcut | Notes |
|--------|--------------------------------------|------------------------------|
| Navigate modules | `Tab` / `Shift+Tab` | Cycles through sections |
| Select/activate | `Enter` or `Space` | Activate button or link |
| Cancel/close | `Escape` | Cancel current action |
| Navigate lists | `Arrow keys` | Move through items |

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

