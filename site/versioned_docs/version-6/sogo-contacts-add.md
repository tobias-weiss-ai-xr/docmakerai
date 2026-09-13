---
title: "Add a Contact"
description: "Learn how to add and organize contacts in the SOGo 6 address book"
sidebar_label: "Add a Contact"
---

import PageSEO from '@site/src/components/PageSEO';

<PageSEO title="Add a Contact" description="Step-by-step tutorial to add and organize contacts in the SOGo 6 address book" keywords={["contacts", "address book", "add contact", "organize", "groups"]} />

# Add a Contact

This tutorial explains how to add contacts to your SOGo 6 address book
and organize them into lists.

## Prerequisites

- A SOGo 6 account with valid credentials
- You are logged into SOGo 6

## Step-by-Step Instructions

### Step 1: Open the Contacts Module

In the sidebar navigation on the left, click **Contacts**
to open your address book.


The contacts view shows your address book with any existing contacts.
On the left, you'll see your address books and lists.

### Step 2: Create a New Contact

Click the **+** (plus) button to add a new contact.

A blank contact form will appear.

![Step 2: Add New Contact](./assets/contacts-add.png)

### Step 3: Enter Contact Information

Fill in the contact's details. The most commonly used fields are:

| Field | Description | Recommended |
| :--- | :--- | :--- |
| **First Name** | Given name | ✅ Always |
| **Last Name** | Family name | ✅ Always |
| **Email** | Primary email address | ✅ Always |
| **Phone** | Telephone number | Optional |
| **Mobile** | Mobile phone number | Optional |
| **Organisation** | Organization or company | Optional |
| **Role** | Function or role at the company | Optional |
| **Title** | e.g., Dr., Prof. | Optional |

:::tip
The **Display Name** field is auto-filled from First + Last name,
but you can customize it (e.g., "John D. (IT Support)").
:::

### Step 4: Add Additional Details (Optional)

Scroll down to access more fields:

| Section | Fields |
| :--- | :--- |
| **Address** | Street, City, ZIP, Country |
| **Other Email** | Secondary email addresses |
| **Website** | Personal or work URL |
| **IM** | Instant messaging handles (Jabber, etc.) |
| **Notes** | Free-text notes about the contact |

### Step 5: Choose an Address Book

If you have multiple address books, select which one to save to using
the dropdown at the top of the contact form.

Typically there is a personal address book — at the University of Marburg it
carries your account abbreviation, like your Personal calendar — and possibly
additional shared address books.
- **Collected Addresses** — Automatically saved from sent emails

### Step 6: Save the Contact

Click **Save** to add the contact to your address book.

The contact will now appear in your contact list. You can:

- Click on it to view or edit details
- Start typing the name when composing an email to auto-complete

## Organizing Contacts into Lists

### Create a List

1. In the top navigation, click **+** next to **Lists**
2. Enter a name for the list (e.g., "Team", "Clients", "Family")
3. Click **OK**

### Add Contacts to a List

1. Drag a contact from the list onto the list name, or
2. Click the three-dot menu (⋯) next to the list, select **Add Members**, and choose contacts

## Importing Contacts (CSL/vCard)

To import contacts from another service:

1. Click the **three-dot menu** (⋯) in the contacts toolbar
2. Select **Import**
3. Choose a file:
   - **vCard (.vcf)** — Standard format, works with most address books
   - **CSV (.csv)** — Spreadsheet export format
4. Click **Import**

:::warning
Imported contacts are added to the currently selected address book.
Make sure the correct address book is selected before importing.
:::

## Editing or Deleting a Contact

- **Edit:** Click on a contact in the list, then click **Edit**
- **Delete:** Select the contact and click **Delete** (trash icon)

## Conclusion

You have successfully added a contact to your SOGo 6 address book.
Contacts are available throughout SOGo 6 — when composing email, inviting
attendees to calendar events, or searching for colleagues.

## Accessibility

### Keyboard Navigation

SOGo 6 supports full keyboard navigation for contacts management.

| Action | Keyboard Shortcut | Notes |
|--------|----------------------------------|---------------------------|
| Navigate to Contacts | `Alt+M`, `Tab` to Contacts |
| New contact | `+` or `C` | Creates new contact |
| Navigate contacts | `J` / `K` | Next/previous contact |
| Search contacts | `/` | Focus search field |
| Edit contact | `E` | Edit selected contact |
| Delete contact | `D` | Delete selected contact |
| Cancel | `Escape` | Close dialog |

### Screen Reader Workflow

**Step 1: Navigate to Contacts Module**
1. `Alt+M` or `Tab` to sidebar
2. Arrow keys to "Contacts"
3. `Enter` to activate Contacts module
4. Screen reader: "Contacts module, heading, level 2"

**Step 2: Create New Contact**
1. Focus on "+" button (top of contacts list)
2. Screen reader: "New contact, button"
3. `Enter` to activate

**Step 3: Complete Contact Form**

Form fields appear in this order (screen reader focus sequence):

1. **First Name** - recommended
   - Type first name
   - `Tab` to next field

2. **Last Name** - recommended
   - Type last name
   - `Tab` to next field

3. **Email** - recommended
   - Type primary email address
   - Screen reader: "Email, edit, text@domain.com, editable combobox"

**Optional fields (tab through or skip with `Shift+Tab`):**

4. **Phone** - main phone number
5. **Mobile** - mobile phone number
6. **Organisation** - organization or company
7. **Role** - function or role at the company

**Additional sections (scroll or `Tab` further):**

8. **Address** section
   - Street, City, ZIP, Country fields
9. **Other Email** - secondary email addresses
10. **Website** - personal or work URL
11. **IM** - IM handles
12. **Notes** - free-text notes

**Step 4: Choose Address Book (if applicable)**
- `Tab` to Address Book dropdown
- `Arrow` keys to select from "Personal", "Shared", etc.
- `Enter` to confirm

**Step 5: Save Contact**
- `Tab` to Save button
- `Enter` to activate
- You should hear: "Contact saved"
- Contact appears in contact list

**Common Screen Reader Announcements:**

| Announcement | Meaning | Action |
|-------------------------------|----------------------|-----------------|
| "Email, editable combobox" | Email field with suggestions | Type email to see suggestions |
| "Select address book, combo box" | Choose where to save contact | `Arrow` to select, `Enter` to confirm |
| "Contact saved" | Success | Contact now in address book |
| "Please enter a valid email" | Invalid email format | Fix email address |

**Keyboard Shortcuts in Contact Form:**
- `Ctrl+S` or `Cmd+S` → Save (alias for Enter on Save button)
- `Escape` → Cancel/discard
- `Tab` → Next field
- `Shift+Tab` → Previous field

### Visual Content Descriptions

**contacts-add.png:** This static screenshot shows adding a contact in SOGo 6's address book interface.


**Screen Reader Alternative:** If you cannot view this image, please use the **Screen Reader Workflow** section above.


### High Contrast Mode

SOGo 6 supports theme customization (light/dark mode) via user preferences. Workarounds for low-vision users:

**Browser/OS-Level High Contrast:**
1. **Windows:** `Win+Ctrl+C` toggles high contrast → Settings → Ease of Access → High Contrast
2. **macOS:** `System Preferences → Accessibility → Display → Increase contrast`
3. **Browser Extensions:** Dark Reader, High Contrast (Chrome)

**Contact Form Accessibility:** All form fields have associated labels. Use `Tab` to navigate between fields. Screen readers will announce field labels and current values.
