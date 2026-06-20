# calendar Specification

> Source files: capture/run_captures.py (record_calendar_* functions)
> Last updated: 2025-06-20

## Purpose

Capture SOGo calendar module workflows as annotated WebP animations for the
user guide. Covers event creation, recurring events, editing, deletion, view
switching, sharing, subscriptions, free/busy scheduling, and iCal import/export.

## Requirements

### Requirement: Calendar Event Creation

The capture pipeline SHALL record the workflow for creating a new calendar
event via double-click on a time slot, filling the event dialog, and saving.

#### Scenario: Create event via double-click

- **GIVEN** an authenticated session and the calendar in week view
- **WHEN** the user double-clicks the time slot at Monday 10:00
- **THEN** the event dialog SHALL open
- **AND** the title and location fields SHALL be filled
- **AND** the event SHALL be saved
- **AND** the workflow SHALL produce an annotated WebP with step indicators and UI highlights

#### Scenario: Annotation markers

- **GIVEN** the calendar create event workflow is being recorded
- **WHEN** the double-click action occurs
- **THEN** red circle highlights SHALL mark the day cell and hour cell
- **AND** a step header SHALL display "Doppelklick auf Montag 10:00"

### Requirement: Recurring Events

The capture pipeline SHALL record creating a weekly recurring event series.

#### Scenario: Weekly recurrence

- **GIVEN** an event dialog is open
- **WHEN** the repeat dropdown is set to "Weekly"
- **THEN** the event SHALL be saved as a recurring series
- **AND** the resulting calendar SHALL show the repeating pattern
- **AND** the WebP SHALL annotate the repeat selection and saved series

### Requirement: Calendar Views

The capture pipeline SHALL record switching between calendar view modes
(day, week, month).

#### Scenario: View switching

- **GIVEN** the calendar module is open
- **WHEN** the user clicks the view selector buttons
- **THEN** the calendar SHALL transition between day, week, and month views
- **AND** each transition SHALL be captured as an annotated frame

### Requirement: Event Edit and Delete

The capture pipeline SHALL record editing an existing event and deleting it.

#### Scenario: Edit then delete

- **GIVEN** an existing calendar event exists
- **WHEN** the user clicks the event to open the dialog
- **THEN** the title SHALL be modified and saved
- **AND** the event SHALL then be deleted via the delete action
- **AND** the WebP SHALL show both the edit and delete steps

### Requirement: Calendar Sharing

The capture pipeline SHALL record sharing a calendar with another user.

#### Scenario: Share with user

- **GIVEN** a calendar exists in the user's account
- **WHEN** the user opens the sharing dialog
- **THEN** a recipient SHALL be added with permissions
- **AND** the sharing SHALL be confirmed
- **AND** the WebP SHALL annotate the sharing workflow

### Requirement: Calendar Subscription

The capture pipeline SHALL record subscribing to an external iCal calendar feed.

#### Scenario: Subscribe to iCal feed

- **GIVEN** the calendar module is open
- **WHEN** the user opens the subscription dialog
- **THEN** an iCal URL SHALL be entered
- **AND** the subscription SHALL be confirmed
- **AND** the subscribed calendar SHALL appear in the sidebar

### Requirement: Free/Busy Scheduling

The capture pipeline SHALL record scheduling a meeting using the free/busy grid.

#### Scenario: Schedule with attendees

- **GIVEN** an event dialog with attendees is open
- **WHEN** the free/busy grid is displayed
- **THEN** attendee availability SHALL be visible
- **AND** a suitable time slot SHALL be selected
- **AND** the WebP SHALL annotate the grid interaction

### Requirement: iCal Import/Export

The capture pipeline SHALL record importing and exporting calendar data via iCal format.

#### Scenario: Export calendar

- **GIVEN** a calendar exists with events
- **WHEN** the user selects the export option
- **THEN** an iCal file SHALL be downloaded
- **AND** the WebP SHALL show the export workflow

## Technical Notes

- **Implementation**: `capture/run_captures.py` — `record_calendar_create_event()`, `record_calendar_recurring()`, `record_calendar_views()`, `record_calendar_edit_delete()`, `record_calendar_share()`, `record_calendar_subscribe()`, `record_freebusy()`, `record_calendar_ical()`
- **Dependencies**: auth-session, capture-pipeline (WorkflowRecorder)
- **Known issues**: 8 workflows produce blank captures (see capture-pipeline spec for reliability requirements)
