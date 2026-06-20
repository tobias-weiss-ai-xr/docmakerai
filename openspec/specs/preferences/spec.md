# preferences Specification

> Source files: capture/run_captures.py (record_preferences, record_password_change, record_vacation, record_global_search)
> Last updated: 2025-06-20

## Purpose

Capture SOGo preferences and utility workflows as annotated WebP animations
for the user guide. Covers general settings, password change, vacation
auto-reply configuration, and global search.

## Requirements

### Requirement: Preferences and Settings

The capture pipeline SHALL record navigating and modifying SOGo general
preferences and settings.

#### Scenario: View preferences

- **GIVEN** an authenticated session
- **WHEN** the user opens the preferences/settings panel
- **THEN** the general settings categories SHALL be visible
- **AND** the WebP SHALL annotate the navigation through settings

#### Scenario: Blank capture fallback

- **GIVEN** the preferences workflow is known to produce blank captures
- **WHEN** the capture produces a >90% white frame
- **THEN** the pipeline SHALL fall back to a textual description
- **AND** the documentation SHALL note the capture was blank

### Requirement: Password Change

The capture pipeline SHALL record the password change workflow.

#### Scenario: Change password

- **GIVEN** the user is in the password change settings
- **WHEN** the user enters the current and new passwords
- **THEN** the password SHALL be updated
- **AND** the WebP SHALL annotate the form interaction

#### Scenario: Blank capture handling

- **GIVEN** the password-change workflow is known to produce blank captures
- **WHEN** the capture produces a blank WebP
- **THEN** the image reference SHALL be removed from the documentation
- **AND** the documentation SHALL describe the workflow textually

### Requirement: Vacation Auto-Reply

The capture pipeline SHALL record configuring the vacation auto-reply feature.

#### Scenario: Enable vacation reply

- **GIVEN** the vacation settings page is open
- **WHEN** the user enables auto-reply and enters a message
- **THEN** the vacation reply SHALL be activated
- **AND** the WebP SHALL annotate the toggle and message input

#### Scenario: Blank capture handling

- **GIVEN** the vacation workflow is known to produce blank captures
- **WHEN** the capture produces a blank WebP
- **THEN** the image reference SHALL be removed from the documentation

### Requirement: Global Search

The capture pipeline SHALL record using the global search feature.

#### Scenario: Search across modules

- **GIVEN** an authenticated session
- **WHEN** the user enters a search query in the global search bar
- **THEN** results from mail, calendar, and contacts SHALL be displayed
- **AND** the WebP SHALL annotate the search input and results display

## Technical Notes

- **Implementation**: `capture/run_captures.py` — `record_preferences()`, `record_password_change()`, `record_vacation()`, `record_global_search()`
- **Dependencies**: auth-session, capture-pipeline (WorkflowRecorder)
- **Known issues**: preferences, password-change, vacation workflows produce blank captures — addressed textually in docs
