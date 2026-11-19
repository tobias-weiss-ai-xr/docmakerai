---
title: "Bookings (calrs)"
sidebar_label: "Bookings (calrs)"
sidebar_position: 27
description: "Appointment booking for everyone — pick a slot on a colleague's page, no account needed"
---

# Bookings (calrs)

[calrs](https://calendar.openedusuite.org) is the openEduSuite's
booking service — "Powered by calrs 🦀", from
[cal.rs](https://cal.rs). Reach it through the portal tile
**Bookings (calrs)**. Every member has a public booking page:
colleagues and guests pick a free slot there, no account required,
and the booking lands in the shared booking calendar that SOGo
mirrors.

![Public booking page: pick a free slot](./assets/calrs-booking.png)

## Booking an Appointment

You do not sign in to book. Open the host's booking page — its
address follows the pattern

```
https://calendar.openedusuite.org/u/<name>/vc
```

where `<name>` is the host's account name (dots become dashes:
`andreas.simon@…` → `/u/andreas-simon/`). Two booking types are
ready for every member:

- **Video Consultation** (`vc`) — 30 minutes
- **Test-Termin** (`test`) — 15 minutes, for trying it out

Pick a day, pick a free slot, enter name and email, and the booking
is fixed — the page confirms with "You're booked". Confirmed
bookings flow into the shared booking calendar; in
[SOGo](/sogo6/sogo-calendar-views) you can watch them arrive via
the subscribed booking calendar.

## Your Own Booking Page

Sign in with **Sign in with SSO** and your openEduSuite account.
Your dashboard opens with **Overview**, **Event Types**,
**Bookings**, and **Teams**:

![calrs dashboard after SSO login](./assets/calrs-dashboard.png)

- **Event Types** — your bookable meeting types: title, length, and
  description. The two from the suite bootstrap are yours to keep or
  to edit.
- **Bookings** — what others booked with you, upcoming first.
- **Teams** — bookable types shared across several people
  (round-robin), for service desks and consultation hours.

Your own page is at `/u/<your name>/vc` — share the link in your
email signature or the [wiki](/suite/xwiki), and people book you
without a single email thread.

## Bookings and SOGo

calrs manages the booking flow; the calendar underneath speaks
CalDAV. The shared booking calendar is the same collection SOGo
mirrors — so a booked slot blocks the time in [SOGo's calendar
view](/sogo6/sogo-calendar-views) too, and free/busy stays honest in
both directions.

## Accessibility

| Action | Key |
|--------|-----|
| Move through days, slots, and the booking form | `Tab` |
| Open or pick the focused element | `Enter` |

- The booking page is a plain page in reading order: day picker,
  slot list, then the form for name and email — `Tab` walks you
  through it, `Enter` picks.
- The dashboard uses ordinary links and tables; `Escape` closes
  dialogs. `Ctrl+Home` (German keyboards: `Strg+Pos1`) returns you
  to the top of the page.
