---
title: "Mail — Spec-Based Guide"
description: "Spec-based guide covering SOGo mail module workflows including compose, read, reply, forward, delete, folders, filters, and signatures."
sidebar_label: "Mail Specification Guide"
---

import PageSEO from '@site/src/components/PageSEO';

<PageSEO title="Mail — Spec-Based Guide" description="Spec-based guide covering SOGo mail module workflows including compose, read, reply, forward, delete, folders, filters, and signatures." keywords="SOGo 5, mail, email, compose, reply, forward, folders, filters, signatures, spec" />

# SOGo Mail

Capture SOGo mail module workflows as annotated WebP animations for the user
guide. Covers composing, reading, replying, forwarding, deleting messages,
folder management, filters, and signatures.

## Prerequisites

- authenticated session with the mail module open
- The inbox is displayed with messages
- message is open in the preview pane
- message is open
- message is selected in the inbox
- The mail module sidebar is visible
- The mail filters settings page is open
- The mail signatures settings page is open

## Step-by-Step Instructions

### Mail Compose

The capture pipeline will record composing and sending a new email message.

#### Step 1: Click the compose button

The user clicks the compose button

**Expected result:**

- the compose window will open
- the recipient, subject, and body fields will be filled
- the message will be sent
- the WebP will annotate each step with UI highlights

### Mail Read

The capture pipeline will record viewing and reading an email message.

#### Step 1: Click a message

The user clicks a message

**Expected result:**

- the message will open in the preview pane
- the message headers and body will be visible

#### Step 2: The capture produces a >90% white frame

The capture produces a >90% white frame

**Expected result:**

- the pipeline will fall back to a PNG screenshot (`01-mail-inbox.png`)
- the documentation will reference the PNG instead of the WebP

:::note
This workflow is known to produce blank captures in the current pipeline. The documentation describes the expected behavior textually.
:::

### Reply, Forward, Delete

The capture pipeline will record replying to, forwarding, and deleting messages.

#### Step 1: Click the reply button

The user clicks the reply button

**Expected result:**

- a compose window will open with the original quoted
- a reply will be typed and sent

#### Step 2: Click the forward button

The user clicks the forward button

**Expected result:**

- a compose window will open with the original attached
- a new recipient will be entered and sent

#### Step 3: Click the delete button

The user clicks the delete button

**Expected result:**

- the message will move to the trash
- the inbox will update

### Folder Management

The capture pipeline will record creating, renaming, and deleting mail folders.

#### Step 1: Create a new folder

The user creates a new folder

**Expected result:**

- the folder will appear in the sidebar
- messages will be movable into the new folder

### Mail Filters

The capture pipeline will record creating a mail filter rule.

#### Step 1: Define a new filter rule with criteria and action

The user defines a new filter rule with criteria and action

**Expected result:**

- the filter will be saved
- future matching messages will trigger the rule

### Mail Signatures

The capture pipeline will record creating and configuring email signatures.

#### Step 1: Enter signature text and saves

The user enters signature text and saves

**Expected result:**

- the signature will be stored
- new compose windows will include the signature

## Troubleshooting

mail-read, mail-reply-forward-delete, mail-folder-management, mail-signatures, mail-filters produce blank captures — currently replaced with PNGs or removed from docs

## Related Sections

- [Auth Session](./sogo-spec-auth-session)

## Implementation Reference

Source: `capture/run_captures.py` — `record_mail_compose()`, `record_mail_read()`, `record_mail_reply_forward_delete()`, `record_mail_folder_management()`, `record_mail_filters()`, `record_mail_signatures()`

## Appendix: Scenario Reference

| Scenario | Precondition | Action | Expected Result |
|---|---|---|---|
| Compose and send | an authenticated session with the mail module open | the user clicks the compose button | the compose window will open |
| Open and read message | the inbox is displayed with messages | the user clicks a message | the message will open in the preview pane |
| Blank capture handling | the mail-read workflow is known to produce blank captures | the capture produces a >90% white frame | the pipeline will fall back to a PNG screenshot (`01-mail-inbox.png`) |
| Reply workflow | a message is open in the preview pane | the user clicks the reply button | a compose window will open with the original quoted |
| Forward workflow | a message is open | the user clicks the forward button | a compose window will open with the original attached |
| Delete workflow | a message is selected in the inbox | the user clicks the delete button | the message will move to the trash |
| Create folder | the mail module sidebar is visible | the user creates a new folder | the folder will appear in the sidebar |
| Create filter rule | the mail filters settings page is open | the user defines a new filter rule with criteria and action | the filter will be saved |
| Create signature | the mail signatures settings page is open | the user enters signature text and saves | the signature will be stored |
