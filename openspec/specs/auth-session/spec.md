# auth-session Specification

> Source files: capture/run_captures.py (login, logout functions)
> Last updated: 2025-06-20

## Purpose

Manage SOGo demo authentication and session lifecycle for the capture pipeline.
The auth-session domain establishes an authenticated browser context that all
subsequent workflow captures reuse via Playwright storage state.

## Requirements

### Requirement: Login Flow

The capture pipeline SHALL authenticate against the SOGo demo instance using
credentials from environment variables before any workflow capture begins.

#### Scenario: Successful login with valid credentials

- **GIVEN** the environment variables `SOGO_URL`, `SOGO_USERNAME`, and `SOGO_PASSWORD` are set
- **WHEN** the login function navigates to `SOGO_URL` and submits the credential form
- **THEN** the browser context SHALL contain a valid authenticated session
- **AND** the session storage state SHALL be extractable for reuse by workflow contexts

#### Scenario: Login form interaction

- **GIVEN** the SOGo login page has loaded
- **WHEN** the login function fills the username field, password field, and toggles the "remember me" switch
- **THEN** the submit button SHALL be clicked
- **AND** a 5000ms wait SHALL follow to allow session establishment

#### Scenario: Default credentials

- **GIVEN** no environment variables are set
- **WHEN** the pipeline starts
- **THEN** the default URL SHALL be `https://demo.sogo.nu/SOGo/`
- **AND** the default username and password SHALL be `demo`

### Requirement: Session Reuse

The capture pipeline SHALL establish a single authenticated session and reuse
its storage state across all workflow capture contexts.

#### Scenario: Shared storage state

- **GIVEN** a successful login has occurred in a dedicated login context
- **WHEN** the pipeline creates a new browser context for a workflow capture
- **THEN** the new context SHALL be initialized with the login context's storage state
- **AND** the workflow SHALL NOT need to re-authenticate

#### Scenario: Login context cleanup

- **GIVEN** the storage state has been extracted from the login context
- **WHEN** the login context is no longer needed
- **THEN** the login context SHALL be closed
- **AND** no video recording SHALL occur during login

### Requirement: Logout Capture

The capture pipeline SHALL provide a logout workflow that records the user
signing out of the SOGo session.

#### Scenario: Logout workflow recording

- **GIVEN** an authenticated browser context with video recording enabled
- **WHEN** the logout workflow runs
- **THEN** the workflow SHALL navigate to the logout trigger
- **AND** the transition to the login screen SHALL be captured as annotated frames

## Technical Notes

- **Implementation**: `capture/run_captures.py` — `login()`, `record_logout()`
- **Dependencies**: playwright, capture-pipeline domain (WorkflowRecorder)
- **Configuration**: `SOGO_URL`, `SOGO_USERNAME`, `SOGO_PASSWORD`, `SOGO_RECIPIENT` env vars
