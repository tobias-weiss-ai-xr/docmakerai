---
title: "Resource Booking (Rooms, Equipment)"
description: "Book shared resources like meeting rooms and equipment"
sidebar_label: "Resource Booking"
---

import PageSEO from '@site/src/components/PageSEO';

<PageSEO title="Resource Booking (Rooms, Equipment)" description="How to book shared resources like meeting rooms and equipment in SOGo 6" keywords={["resource booking", "meeting rooms", "equipment", "scheduling", "facilities"]} />

# Resource Booking

Reserve shared resources — meeting rooms, projectors, equipment — through the calendar.

:::info
A resource is typically a special calendar account provided by your
administrator. The demo environment at demov6.sogo.nu has no resource
accounts, so this guide describes the booking path without screenshots
of a resource picker.
:::

## Prerequisites

- A SOGo 6 account with valid credentials
- Logged into SOGo 6
- Resource accounts configured by your administrator

## The Booking Path

Booking a resource means creating an event and adding the resource as a
participant:

1. Open the **Calendar** module
2. Create an event — click the **+** button in the toolbar, or
   double-click a time slot in the calendar grid
   (see [Create an Event](./sogo-calendar-create-event))
3. In the event dialog, expand **Participants**
4. Type the resource's name — rooms and equipment appear in the same
   auto-complete as people
5. Add the people who should attend
6. Click **Create Event**

## Checking a Resource's Availability

Before booking, check when the resource is free:

- Add it to the event and use the availability view — see
  [Free/Busy](./sogo-calendar-freebusy)
- The resource's busy times show up like any participant's

If a booking is declined, pick a different slot — the resource is
already reserved at that time.

## Accessibility

### Keyboard Navigation

| Action | How | Notes |
|--------|-----|-------|
| Create the booking event | `Tab` to **Create Event**, then `Enter` | See Create an Event |
| Open Participants | `Tab` to the Participants field | Section within the event dialog |
| Save the booking | `Tab` to **Create Event**, then `Enter` | Confirm button of the dialog |

### Screen Readers

- `Strg+Pos1` / `Ctrl+Home` takes you to the top of the page — a reliable
  starting point for exploring with `h` (headings) in your screen reader.
- In the availability view, busy blocks are visual — the free/busy data
  behind them is read out as text by the screen reader.

- **High contrast and dark mode:** contrast and dark themes come from the
  operating system or browser — Windows `Win+Ctrl+C`, macOS *Increase contrast*,
  or a browser extension such as Dark Reader. If the app offers its own dark
  theme, switch it in its settings; the navigation described above still applies.
