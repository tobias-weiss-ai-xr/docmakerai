---
title: "Auth Session — Spec-Based Guide"
description: "Manage SOGo demo authentication and session lifecycle for the capture pipeline. The auth-session domain establishes an authenticated browser context tha..."
sidebar_label: "Auth Session Specification Guide"
---

import PageSEO from '@site/src/components/PageSEO';

<PageSEO title="Auth Session — Spec-Based Guide" description="Manage SOGo demo authentication and session lifecycle for the capture pipeline. The auth-session domain establishes an authenticated browser context tha..." keywords="SOGo 5, login, logout, session, authentication, spec" />

# SOGo Authentication and Sessions

Manage SOGo demo authentication and session lifecycle for the capture pipeline.
The auth-session domain establishes an authenticated browser context that all
subsequent workflow captures reuse via Playwright storage state.

## Prerequisites

- The environment variables `SOGO_URL`, `SOGO_USERNAME`, and `SOGO_PASSWORD` are set
- The SOGo login page has loaded
- No environment variables are set
- successful login has occurred in a dedicated login context
- The storage state has been extracted from the login context
- authenticated browser context with video recording enabled

## Step-by-Step Instructions

### Login Flow

The capture pipeline will authenticate against the SOGo demo instance using
credentials from environment variables before any workflow capture begins.

#### Step 1: Navigate to `SOGO_URL` and submits the credential form

The login function navigates to `SOGO_URL` and submits the credential form

**Expected result:**

- the browser context will contain a valid authenticated session
- the session storage state will be extractable for reuse by workflow contexts

#### Step 2: Fill the username field, password field, and toggles the "remember me" switch

The login function fills the username field, password field, and toggles the "remember me" switch

**Expected result:**

- the submit button will be clicked
- a 5000ms wait will follow to allow session establishment

#### Step 3: Starts

The pipeline starts

**Expected result:**

- the default URL will be `https://demo.sogo.nu/SOGo/`
- the default username and password will be `demo`

### Session Reuse

The capture pipeline will establish a single authenticated session and reuse
its storage state across all workflow capture contexts.

#### Step 1: Create a new browser context for a workflow capture

The pipeline creates a new browser context for a workflow capture

**Expected result:**

- the new context will be initialized with the login context's storage state
- the workflow will NOT need to re-authenticate

#### Step 2: The login context is no longer needed

The login context is no longer needed

**Expected result:**

- the login context will be closed
- no video recording will occur during login

### Logout Capture

The capture pipeline will provide a logout workflow that records the user
signing out of the SOGo session.

#### Step 1: The logout workflow runs

The logout workflow runs

**Expected result:**

- the workflow will navigate to the logout trigger
- the transition to the login screen will be captured as annotated frames

## Related Sections

- [Playwright](./sogo-spec-playwright)
- [Capture Domain (Workflowrecorder)](./sogo-spec-capture-pipeline-domain-workflowrecorder)

## Implementation Reference

Source: ``capture/run_captures.py` — `login()`, `record_logout()``

## Appendix: Scenario Reference

| Scenario | Precondition | Action | Expected Result |
|---|---|---|---|
| Successful login with valid credentials | the environment variables `SOGO_URL`, `SOGO_USERNAME`, and `SOGO_PASSWORD` are set | the login function navigates to `SOGO_URL` and submits the credential form | the browser context will contain a valid authenticated session |
| Login form interaction | the SOGo login page has loaded | the login function fills the username field, password field, and toggles the "remember me" switch | the submit button will be clicked |
| Default credentials | no environment variables are set | the pipeline starts | the default URL will be `https://demo.sogo.nu/SOGo/` |
| Shared storage state | a successful login has occurred in a dedicated login context | the pipeline creates a new browser context for a workflow capture | the new context will be initialized with the login context's storage state |
| Login context cleanup | the storage state has been extracted from the login context | the login context is no longer needed | the login context will be closed |
| Logout workflow recording | an authenticated browser context with video recording enabled | the logout workflow runs | the workflow will navigate to the logout trigger |
