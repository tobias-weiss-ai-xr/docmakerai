# contacts Specification

> Source files: capture/run_captures.py (record_contacts_* functions)
> Last updated: 2025-06-20

## Purpose

Capture SOGo contacts module workflows as annotated WebP animations for the
user guide. Covers adding contacts, editing/deleting contacts, and
importing/exporting contact data.

## Requirements

### Requirement: Contact Creation

The capture pipeline SHALL record adding a new contact to the address book.

#### Scenario: Add new contact

- **GIVEN** an authenticated session with the contacts module open
- **WHEN** the user clicks the add contact button
- **THEN** the contact form SHALL open
- **AND** name, email, and phone fields SHALL be filled
- **AND** the contact SHALL be saved
- **AND** the WebP SHALL annotate the form interaction with step indicators

#### Scenario: Form field highlights

- **GIVEN** the contact form is being recorded
- **WHEN** the user focuses each field
- **THEN** the WebP SHALL show UI highlights on active input fields

### Requirement: Contact Edit and Delete

The capture pipeline SHALL record editing an existing contact and deleting it.

#### Scenario: Edit contact

- **GIVEN** a contact exists in the address book
- **WHEN** the user opens the contact for editing
- **THEN** a field SHALL be modified and saved
- **AND** the WebP SHALL show the edit workflow

#### Scenario: Delete contact

- **GIVEN** a contact exists in the address book
- **WHEN** the user selects and deletes the contact
- **THEN** the contact SHALL be removed
- **AND** the address book SHALL update

### Requirement: Contact Import/Export

The capture pipeline SHALL record importing and exporting contacts via vCard
or CSV format.

#### Scenario: Export contacts

- **GIVEN** the contacts module is open with existing contacts
- **WHEN** the user selects the export option
- **THEN** a vCard or CSV file SHALL be downloaded
- **AND** the WebP SHALL annotate the export workflow

#### Scenario: Import contacts

- **GIVEN** the contacts module is open
- **WHEN** the user selects the import option and uploads a file
- **THEN** the contacts SHALL be parsed and added
- **AND** the address book SHALL reflect the new entries

## Technical Notes

- **Implementation**: `capture/run_captures.py` — `record_contacts_add()`, `record_contacts_edit_delete()`, `record_contacts_import_export()`
- **Dependencies**: auth-session, capture-pipeline (WorkflowRecorder)
