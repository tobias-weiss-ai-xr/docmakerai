---
title: "Free/Busy Lookup"
description: "Check colleagues' availability before scheduling meetings"
sidebar_label: "Free/Busy Lookup"
---

# Free/Busy Lookup

Check when your colleagues are available before scheduling a
meeting — directly from the event creation dialog.

## Prerequisites

- A SOGo account with valid credentials
- You are logged into SOGo
- The colleague has a SOGo account and has shared their free/busy info

## Step-by-Step Instructions

### Step 1: Start Creating an Event

1. Open the **Calendar** module
2. Click **+** to create a new event, or click an existing event to edit

### Step 2: Open Free/Busy View

1. In the event dialog, click the **Attendees** section
2. Click **Free/Busy** or **Availability** button
3. A time grid opens showing your calendar

### Step 3: Add a Colleague

1. In the free/busy grid, click **Add Person** or **Check Availability**
2. Start typing a colleague's name
3. Select them from the auto-complete list
4. Repeat for each person you want to check

### Step 4: Read the Grid

The grid shows time slots for each person:

| Color | Meaning |
|-------|---------|
| ✅ **Green** | Available |
| ❌ **Red** | Busy (has an event) |
| 🟡 **Yellow** | Tentative / maybe attending |
| ⬜ **White** | No data (not shared, or outside working hours) |

### Step 5: Find a Common Slot

Look for a time when all attendees are green.
SOGo may suggest the next available slot automatically.

### Step 6: Confirm the Time

Click on the desired time slot in the grid.
The event's start/end time updates to match.

## What Others See

By default, SOGo is configured so that other users can see:

| Permission | What's Visible |
|------------|----------------|
| **Free/Busy** | Only whether you're available or busy (no details) |
| **View (read-only)** | Event titles and times |
| **Confidential events** | Marked as "Busy" only, even to viewers |

Your administrator can change default permission levels via the
`SOGoCalendarDefaultRoles` setting.

## Troubleshooting

### Colleague not showing up

- Check they have a SOGo account
- They may not have free/busy sharing enabled
- They might be in a different address book — try typing their full email

### All times show "No data"

- The colleague hasn't shared their calendar with you
- Contact them or your administrator to grant free/busy access
- Default roles may be restricted (`PublicDAndTViewer` must be set)

## Conclusion

Free/busy lookup helps you find meeting times without the
back-and-forth of "Are you free at...?" emails. It works for
anyone in your organization who shares calendar availability.
