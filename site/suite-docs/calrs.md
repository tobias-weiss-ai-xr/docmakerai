---
title: "Bookings (calrs)"
sidebar_label: "Bookings (calrs)"
sidebar_position: 27
description: "Appointment booking for everyone — pick a slot on a colleague's page, no account needed"
---
import PageSEO from '@site/src/components/PageSEO';

<PageSEO
  title="Bookings (calrs)"
  description="Appointment booking for everyone — pick a slot on a colleague's page, no account needed"
  keywords={["Bookings", "calrs", "openEduSuite"]}
  suffix="openEduSuite"
  defaultKeywords={["higher education", "open source"]}
/>


# Bookings (calrs)

[calrs](https://calendar.openedusuite.org) is the openEduSuite's
booking service — "Powered by calrs", says the footer of every
page — from [cal.rs](https://cal.rs). Reach it through the [portal](/suite/portal)
tile **Bookings (calrs)**. Every member has a public booking page:
colleagues and guests pick a free slot there, no account required.

![Public booking page: pick a free slot](./assets/calrs-booking.png)

## Booking an Appointment

You do not sign in to book. Open the host's booking page — its
address follows the pattern

```
https://calendar.openedusuite.org/u/<name>/vc
```

where `<name>` is the host's account name (dots become dashes:
`andreas.simon@…` → `/u/andreas-simon/`). Two event types are
ready for every member:

- **Video Consultation** (`vc`) — 30 minutes
- **Test-Termin** (`test`) — 15 minutes, for trying it out

The page shows the host's name, the event type with its length, a
timezone picker, and a month calendar: pick a day, pick a free
slot, enter name and email, and confirm. Free slots appear only
once the host has connected a calendar (see **Sources** below).

## Your Own Booking Page

On the login page choose **Sign in with SSO** and authenticate
with your openEduSuite account. The dashboard opens: the sidebar
groups **Overview**, **Event Types**, **Bookings**, and **Teams**
under Scheduling, followed by **Invite Links**, **Sources**,
**Profile & Settings**, and **Troubleshoot**.

![calrs dashboard after SSO login](./assets/calrs-dashboard.png)

- **Overview** — your public page address, a getting-started
  checklist (connect a calendar, create your first event type,
  share your booking link), and counters for event types,
  upcoming bookings, pending approvals, and calendar sources.
- **Event Types** — your bookable meeting types, each listed with
  its length and its public link, plus **+ New** for another one.
  The edit form covers title, slug, description, location,
  duration, slot interval, and per-day availability hours.
- **Bookings** — what others booked with you, upcoming first.
- **Teams** — booking types shared across several people; teams
  are created by administrators, who add you as a member.
- **Invite Links** — single-use booking links for internal event
  types, for specific contacts — no one else can book.
- **Sources** — the CalDAV connection: pick a provider (SOGo,
  Nextcloud, Zimbra, and more) and calrs checks that calendar
  before a slot is offered.
- **Troubleshoot** — a day view that shows, hour by hour, why a
  slot is available or blocked: calendar event, booking, outside
  hours, buffer or minimum notice.

Under **Profile & Settings** you set your display name, username
(the part after `/u/` in your booking URL), title and bio for the
public page, booking email, timezone, and your default working
hours. Your own page is at `/u/<your name>/vc` — share the link in
your email signature or the [wiki](/suite/xwiki), and people book
you without a single email thread.

## Bookings and SOGo

calrs manages the booking flow; the calendar underneath speaks
CalDAV. The **Sources** provider list includes SOGo itself:
connect your SOGo calendar and calrs checks it before offering a
slot — a booked slot blocks the time in [SOGo's calendar
view](/sogo6/sogo-calendar-views) too, and free/busy stays honest
in both directions.

If the service stays closed to you, the
[helpdesk](/suite/helpdesk-create-ticket) reaches its operators.

## Accessibility

| Action | Key |
|--------|-----|
| Move through days, slots, and the booking form | `Tab` |
| Open or pick the focused element | `Enter` |

- The booking page is a plain page in reading order: month
  calendar, slot list, then the form for name and email — `Tab`
  walks you through it, `Enter` picks.
- The dashboard uses ordinary links and tables; `Escape` closes
  dialogs. `Ctrl+Home` (German keyboards: `Strg+Pos1`) returns you
  to the top of the page.

- **High contrast and dark mode:** contrast and dark themes come from the
  operating system or browser — Windows `Win+Ctrl+C`, macOS *Increase contrast*,
  or a browser extension such as Dark Reader. If the app offers its own dark
  theme, switch it in its settings; the navigation described above still applies.
