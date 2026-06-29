---
title: "Contacts — Spec-Based Guide"
description: "Spec-based guide covering SOGo contacts module workflows including add, edit/delete, and import/export operations."
sidebar_label: "Contacts Specification Guide"
---

import PageSEO from '@site/src/components/PageSEO';

<PageSEO title="Contacts — Spec-Based Guide" description="Spec-based guide covering SOGo contacts module workflows including add, edit/delete, and import/export operations." keywords="SOGo 5, contacts, address book, vCard, import, export, spec" />

# SOGo Contacts

Capture SOGo contacts module workflows as annotated WebP animations for the
user guide. Covers adding contacts, editing/deleting contacts, and
importing/exporting contact data.

## Prerequisites

- authenticated session with the contacts module open
- The contact form is being recorded
- contact exists in the address book
- The contacts module is open with existing contacts
- The contacts module is open

## Step-by-Step Instructions

### Contact Creation

The capture pipeline will record adding a new contact to the address book.

#### Step 1: Click the add contact button

The user clicks the add contact button

**Expected result:**

- the contact form will open
- name, email, and phone fields will be filled
- the contact will be saved
- the WebP will annotate the form interaction with step indicators

#### Step 2: Focus each field

The user focuses each field

**Expected result:**

- the WebP will show UI highlights on active input fields

:::tip
During recording the system automatically overlays step headers and UI highlights (red circles, arrows) on each frame.
:::

### Contact Edit and Delete

The capture pipeline will record editing an existing contact and deleting it.

#### Step 1: Open the contact for editing

The user opens the contact for editing

**Expected result:**

- a field will be modified and saved
- the WebP will show the edit workflow

#### Step 2: Select and deletes the contact

The user selects and deletes the contact

**Expected result:**

- the contact will be removed
- the address book will update

### Contact Import/Export

The capture pipeline will record importing and exporting contacts via vCard
or CSV format.

#### Step 1: Select the export option

The user selects the export option

**Expected result:**

- a vCard or CSV file will be downloaded
- the WebP will annotate the export workflow

#### Step 2: Select the import option and uploads a file

The user selects the import option and uploads a file

**Expected result:**

- the contacts will be parsed and added
- the address book will reflect the new entries

## Related Sections

- [Auth Session](./sogo-spec-auth-session)

## Implementation Reference

Source: `capture/run_captures.py` — `record_contacts_add()`, `record_contacts_edit_delete()`, `record_contacts_import_export()`

## Appendix: Scenario Reference

| Scenario: Description | Precondition | Action | Expected Result |
|---|---|---|---|
| Add new contact | an authenticated session with the contacts module open | the user clicks the add contact button | the contact form will open |
| Form field highlights | the contact form is being recorded | the user focuses each field | the WebP will show UI highlights on active input fields |
| Edit contact | a contact exists in the address book | the user opens the contact for editing | a field will be modified and saved |
| Delete contact | a contact exists in the address book | the user selects and deletes the contact | the contact will be removed |
| Export contacts | the contacts module is open with existing contacts | the user selects the export option | a vCard or CSV file will be downloaded |
| Import contacts | the contacts module is open | the user selects the import option and uploads a file | the contacts will be parsed and added |
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

