---
title: "Contacts — Import & Export"
description: "Transfer contacts using vCard format in SOGo 5"
sidebar_label: "Import & Export"
---

import PageSEO from '@site/src/components/PageSEO';

<PageSEO title="Contacts — Import & Export" description="Transfer contacts using vCard format in SOGo 5. Step-by-step tutorial covers importing and exporting contacts between applications." keywords="SOGo 5, contacts, import, export, vCard, address book" />

# Contacts — Import & Export

Migrate contacts between applications using vCard import/export.

## Prerequisites

- A SOGo 5 account with valid credentials
- You are logged into SOGo 5

## Step-by-Step Instructions

### Step 1: Open the Contacts Module

In the sidebar, click **Contacts** to open the address book.

### Step 2: Access Actions Menu

Click the **Actions** menu button (often a downward arrow or three dots) near the top of the contact list.

![Contacts import/export menu in SOGo 5](./assets/contacts-import-export.png)

### Step 3: Export Contacts

1. Select **Export** from the Actions menu
2. Choose the address book to export
3. The contacts download as a `.vcf` (vCard) file

### Step 4: Import Contacts

1. Click **Import** from the Actions menu
2. Select the `.vcf` file you want to import
3. Choose the target address book
4. Select how to handle duplicates:
   - **Skip** — Do not import duplicates
   - **Update** — Replace existing contacts with imported data
   - **Add as new** — Import as separate contact
5. Click **Import** to begin

:::info
vCard (`.vcf`) is the standard format for sharing contacts across applications like Microsoft Outlook, Apple Contacts, Gmail, and more.
:::

## Import Options

| Duplicate Handling: Description | Description |
|--------------------|-------------|
| **Skip duplicates** | Ignores contacts with the same email address |
| **Update existing** | Overwrites existing contact data with imported information |
| **Add all** | Imports all contacts, creating duplicates if necessary |

## Export Options

| Format: Description | Description | Typical Size (100 contacts) |
|--------|--------------|-----------------------------|
| **vCard 3.0** | Standard vCard format | ~25 KB |
| **vCard 4.0** | Newer format with extended fields | ~30 KB |
| **CSV** | Comma-separated values for spreadsheet apps | ~15 KB |

:::tip
To back up your entire address book, periodically export all contacts to a vCard file and store it in a safe location.
:::

## Troubleshooting

| Issue: Description | Possible Cause | Solution |
|-------|---------------|----------|
| Import/Export actions not visible | Feature not enabled | Contact your administrator |
| Import fails | Corrupted vCard file | Open the file in a text editor and verify format |
| Contacts appear twice | Duplicate handling not selected | Choose "Skip duplicates" during import |
| Specific fields missing | Format incompatibility | Convert the vCard to vCard 3.0 format and retry |
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

