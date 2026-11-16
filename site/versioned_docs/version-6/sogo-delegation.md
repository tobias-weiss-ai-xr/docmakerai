---
title: "Delegation & Permissions"
description: "How sharing and rights work in SOGo 6"
sidebar_label: "Delegation & Permissions"
---

import PageSEO from '@site/src/components/PageSEO';

<PageSEO title="Delegation & Permissions" description="How SOGo 6 calendar sharing works: the rights a person can get and how to combine them" keywords={["delegation", "permissions", "access control", "sharing", "acl"]} />

# Delegation & Permissions

Delegate access to your calendars by granting other users rights on them.

## Prerequisites

- A SOGo 6 account with valid credentials
- You are logged into SOGo 6
- At least two users with SOGo accounts (for delegation)

## The Rights Model

When you share a calendar, you grant each person one of these rights:

| Right | What it allows |
|:------|:---------------|
| See events without details | Busy/free times only — no titles, no details |
| See events with details | Titles, times and descriptions |
| Answer | Respond to invitations |
| Edit | Create, change and delete events |

How a given event appears to that person then depends on both their right
and the event's classification — see
[Free/Busy: What Others See](./sogo-calendar-freebusy#what-others-see).

The same two-axis model applies to address books and mail folders where
your deployment enables sharing.

## Sharing in Practice

Where the sharing controls live depends on your deployment: they appear
with the per-item or per-collection menus of a module.

:::info
The demo environment at demov6.sogo.nu does not expose the share
controls, so this guide deliberately shows no walkthrough of them.
:::

## Related Settings

Calendar behavior you can set yourself (avatar menu → **Calendar**):

- Default calendar and default classification (e.g. *Confidential*)
- Whether off-work hours show as busy — see
  [Free/Busy](./sogo-calendar-freebusy)
- First day of the week

## See Also

- [Free/Busy](./sogo-calendar-freebusy) — how shared availability looks
- [Calendar Sharing](./sogo-calendar-share) — mutual sharing walkthrough

## Accessibility

### Keyboard Navigation

The sharing controls, where your deployment shows them, are regular
buttons and dropdowns: reach them with `Tab` / `Shift+Tab` and activate
with `Enter`.

### Screen Readers

- `Strg+Pos1` / `Ctrl+Home` takes you to the top of the page — a reliable
  starting point for exploring with `h` (headings) in your screen reader.
- The rights tables above use real table markup, so screen readers can
  navigate them row by row.
