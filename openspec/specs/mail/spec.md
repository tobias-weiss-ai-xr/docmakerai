# mail Specification

> Source files: capture/run_captures.py (record_mail_* functions)
> Last updated: 2025-06-20

## Purpose

Capture SOGo mail module workflows as annotated WebP animations for the user
guide. Covers composing, reading, replying, forwarding, deleting messages,
folder management, filters, and signatures.

## Requirements

### Requirement: Mail Compose

The capture pipeline SHALL record composing and sending a new email message.

#### Scenario: Compose and send

- **GIVEN** an authenticated session with the mail module open
- **WHEN** the user clicks the compose button
- **THEN** the compose window SHALL open
- **AND** the recipient, subject, and body fields SHALL be filled
- **AND** the message SHALL be sent
- **AND** the WebP SHALL annotate each step with UI highlights

### Requirement: Mail Read

The capture pipeline SHALL record viewing and reading an email message.

#### Scenario: Open and read message

- **GIVEN** the inbox is displayed with messages
- **WHEN** the user clicks a message
- **THEN** the message SHALL open in the preview pane
- **AND** the message headers and body SHALL be visible

#### Scenario: Blank capture handling

- **GIVEN** the mail-read workflow is known to produce blank captures
- **WHEN** the capture produces a >90% white frame
- **THEN** the pipeline SHALL fall back to a PNG screenshot (`01-mail-inbox.png`)
- **AND** the documentation SHALL reference the PNG instead of the WebP

### Requirement: Reply, Forward, Delete

The capture pipeline SHALL record replying to, forwarding, and deleting messages.

#### Scenario: Reply workflow

- **GIVEN** a message is open in the preview pane
- **WHEN** the user clicks the reply button
- **THEN** a compose window SHALL open with the original quoted
- **AND** a reply SHALL be typed and sent

#### Scenario: Forward workflow

- **GIVEN** a message is open
- **WHEN** the user clicks the forward button
- **THEN** a compose window SHALL open with the original attached
- **AND** a new recipient SHALL be entered and sent

#### Scenario: Delete workflow

- **GIVEN** a message is selected in the inbox
- **WHEN** the user clicks the delete button
- **THEN** the message SHALL move to the trash
- **AND** the inbox SHALL update

### Requirement: Folder Management

The capture pipeline SHALL record creating, renaming, and deleting mail folders.

#### Scenario: Create folder

- **GIVEN** the mail module sidebar is visible
- **WHEN** the user creates a new folder
- **THEN** the folder SHALL appear in the sidebar
- **AND** messages SHALL be movable into the new folder

### Requirement: Mail Filters

The capture pipeline SHALL record creating a mail filter rule.

#### Scenario: Create filter rule

- **GIVEN** the mail filters settings page is open
- **WHEN** the user defines a new filter rule with criteria and action
- **THEN** the filter SHALL be saved
- **AND** future matching messages SHALL trigger the rule

### Requirement: Mail Signatures

The capture pipeline SHALL record creating and configuring email signatures.

#### Scenario: Create signature

- **GIVEN** the mail signatures settings page is open
- **WHEN** the user enters signature text and saves
- **THEN** the signature SHALL be stored
- **AND** new compose windows SHALL include the signature

## Technical Notes

- **Implementation**: `capture/run_captures.py` — `record_mail_compose()`, `record_mail_read()`, `record_mail_reply_forward_delete()`, `record_mail_folder_management()`, `record_mail_filters()`, `record_mail_signatures()`
- **Dependencies**: auth-session, capture-pipeline (WorkflowRecorder)
- **Known issues**: mail-read, mail-reply-forward-delete, mail-folder-management, mail-signatures, mail-filters produce blank captures — currently replaced with PNGs or removed from docs
