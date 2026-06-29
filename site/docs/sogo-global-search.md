---
title: "Global Search"
description: "Search across all modules in SOGo 5"
sidebar_label: "Global Search"
---

import PageSEO from '@site/src/components/PageSEO';

<PageSEO title="Global Search" description="Search across all modules in SOGo 5. Tutorial covers finding emails, contacts, calendar events, and more using the global search feature." keywords="SOGo 5, search, global, email, contacts, calendar" />

# Global Search

Quickly find emails, contacts, calendar events, and more using SOGo 5's global search feature.

## Prerequisites

- A SOGo 5 account with valid credentials
- You are logged into SOGo 5

## Step-by-Step Instructions

### Step 1: Open Search

Click the **Search** button in the top toolbar or use the keyboard shortcut.

![Opening and using global search in SOGo 5](./assets/global-search.webp)

### Step 2: Enter Your Query

Type your search term into the search field. Results appear as you type.

### Step 3: Browse Results

Search results are grouped by module:

| Module: Description | What It Searches |
|--------|------------------|
| **Mail** | Email subject lines and sender names (if IMAP available) |
| **Calendar** | Event titles, locations, and descriptions |
| **Contacts** | Contact names, email addresses, and phone numbers |
| **Tasks** | Task titles (if available) |

Click on any result to navigate directly to that item.

## Search Tips

| Technique: Description | Example | Result |
|-----------|---------|--------|
| **Partial match** | `Meet` | Finds "Meeting", "Meetup", "Street Meet" |
| **By contact name** | `John` | Finds contacts named John and events with John |
| **By date** | `June` | Finds events and emails from June |
| **By location** | `Conference` | Finds events in Conference Room |
| **By keyword** | `Invoice` | Finds all matching items with "Invoice" |

:::tip
Use **global search** to find items across all modules at once instead of searching within each module individually.
:::

## Troubleshooting

| Issue: Description | Possible Cause | Solution |
|-------|---------------|----------|
| No results found | Typo in search term | Double-check spelling or try a partial word |
| Search button not visible | Narrow browser window | Widen the window or use the menu button (☰) |
| Mail results not showing | IMAP server unavailable | Mail search requires an active IMAP connection |
| Results loading slowly | Large mailbox | Narrow your search with more specific terms |
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

