---
title: "Login to SOGo 5"
description: "Step-by-step guide to logging into SOGo 5"
sidebar_label: "Login to SOGo 5"
---

import PageSEO from '@site/src/components/PageSEO';

<PageSEO title="Login to SOGo 5" description="Step-by-step guide to logging into SOGo 5 webmail. Tutorial covers navigating to the login page and accessing your account." keywords="SOGo 5, login, webmail, sign in, authentication" />

# Login to SOGo 5

This tutorial will guide you through logging into your SOGo 5 webmail account.

## Prerequisites

- A SOGo 5 account with valid credentials
- Access to the SOGo 5 web interface

## Step-by-Step Instructions

### Step 1: Navigate to the Login Page

Open your web browser and navigate to your SOGo 5 instance URL (e.g.,
`https://demo.sogo.nu/SOGo/`). You will see the SOGo 5 login page with
username and password fields.

![SOGo 5 login page](./assets/00-login-page.png)

### Step 2: Enter Your Username

Type your SOGo 5 username into the **Username** field. This is typically
the email address or username provided by your system administrator.

### Step 3: Enter Your Password

Type your password into the **Password** field.

### Step 4: Click Login

Click the **Login** button to submit your credentials. SOGo 5 will
authenticate you against the configured backend (LDAP, SQL, etc.).

### Step 5: Verify Dashboard

After successful login, you will see the SOGo 5 main dashboard with the
application navigation sidebar. This confirms you are authenticated and
ready to use SOGo 5's features.

## Conclusion

You have successfully logged into SOGo 5. You can now access your email,
calendar, contacts, and other modules from the sidebar navigation.

## Accessibility

### Keyboard Navigation

SOGo 5 supports full keyboard navigation. No mouse required for login.

| Action | Keyboard Shortcut: What key to press | Notes: Additional information |
|--------|----------------------------------|---------------------------|
| | Focus username field | `Tab` | First form field |
| | Focus password field | `Tab` | Second form field |
| | Submit login | `Enter` | Activates Login button |
| | Focus remember toggle | `Tab` | Remember login checkbox |
| | Navigate after login | `Tab` | Explores UI alternatives |

**Screen Reader Workflow:**

**Step 1: Navigate to SOGo URL**
- Enter `https://demo.sogo.nu/SOGo/` in browser address bar
- Screen reader announces login page with username and password fields

**Step 2: Enter Username**
- `Tab` to username field
- Type your SOGo username
- Screen reader announces: "Username, edit"

**Step 3: Enter Password**
- `Tab` to password field
- Type your password
- Screen reader announces: "Password, edit, type asterisks"
- Note: Password not announced for security (asterisks displayed)

**Step 4: Optional: Remember Login**
- `Tab` to remember login checkbox
- Press `Space` to toggle check
- Screen reader announces: "Remember login, checkbox, not checked" or "checked"

**Step 5: Submit Login**
- `Tab` to Login button
- Press `Enter` or `Space`
- Screen reader announces: "Login, button"

**Step 6: Verify Success**
- Screen reader announces: "Dashboard" or main navigation items
- Confirmation: You are now logged in with access to Mail, Calendar, Contacts

**Common Screen Reader Announcements:**

| Announcement: What screen reader says | Meaning: What it means | Action: What to do |
|-------------------------------|----------------------|-----------------|
| "Username, edit" | Field ready for input | Type your username |
| "Password, edit" | Field ready for input | Type your password |
| "Invalid username" | Authentication failed | Check credentials and retry |
| "Login, button" | Submit login action | Press Enter to submit |
| "Dashboard" | Login successful | Proceed to use SOGo features |

### Visual Content Descriptions

**Login page:** Standard login form with username and password fields, "Remember login" checkbox, and Login button. Clean, centered layout on white background.

**Duration:** Static image  
**Size:** 33 KB

### High Contrast Mode

SOGo 5's dark mode and high contrast mode work with all sections described above. Toggle via: Settings button (gear icon) → General → Theme → Dark/High Contrast.
