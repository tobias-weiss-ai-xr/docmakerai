---
title: "Delegation & Permissions"
description: "Share calendars and mail folders with specific permissions"
sidebar_label: "Delegation & Permissions"
---

import PageSEO from '@site/src/components/PageSEO';

<PageSEO title="Delegation & Permissions" description="Share calendars and mail folders with specific permissions in SOGo 5. Step-by-step tutorial covers ACL-based delegation and access control." keywords="SOGo 5, delegation, permissions, ACL, calendars, mail folders" />

# Delegation & Permissions

Delegate access to your calendars, mail folders and other resources by assigning specific permissions to other users.

## Prerequisites

- A SOGo 5 account with valid credentials
- You are logged into SOGo 5
- At least two users with SOGo accounts (for delegation demonstration)
- Permissions managed per-folder or per-calendar

## Delegation Overview

SOGo supports granular ACL-based permissions for:

| Resource Type | What Can Be Shared |
|---------------|-------------------|
| **Calendar** | Read-only, Full Control, Confidential availability |
| **Address Book** | Read, Write, Modify permissions |
| **Mail Folders** | View, Read, Post, Create, Delete access |
| **Categories** | Permission levels for event categorization |

## Permission Levels

| Permission | Description |
|------------|-------------|
| **Owner** | Full control, can change permissions |
| **Can Read** | View items only |
| **Can Edit** | Modify existing items |
| **Can Create** | Add new items |
| **Can Delete** | Remove items |
| **Reviewer** | Combination of read + approve/reject |

:::tip
Use different permission levels based on trust level. For example, a colleague may get "Can Read" access to your calendar, while a delegated assistant may get "Can Edit" plus "Can Create."
:::

## Step-by-Step Instructions

### Step 1: Open Resource Settings

In the module you want to share (Calendar or Contacts), click the **Settings** gear icon or **Share** button.

:::info
Not all modules in this test environment show the Share button. In a production setup with fully-permissive ACLs enabled, sharing options appear on individual items and collections.
:::

### Step 2: View Current Permissions

The Share/Acl panel displays:

- Current owner
- Existing delegated users/groups
- Current permission level for each

### Step 3: Add User or Group

1. Click **Add** or **Share** button
2. Search for recipient by username, email address
3. Select the target from search results

### Step 4: Assign Permission Level

Choose the appropriate permission from the dropdown:

- **Viewer (Markiert als Viewer)**
- **Participant (Markiert als Participant)**
- **Editor (Markiert als Editor)**
- **Administrator (Vollzugriff)**

### Step 5: Send Notification

Toggle **Send email notification** if you want SOGo to email the recipient about the shared resource.

### Step 6: Save

Click **Apply** or **Save** to activate the sharing.

## Practical Delegation Examples

| Scenario | Recommended Permission | Why |
|----------|------------------------|-----|
| **Assistant** | Administrator | Needs full control to manage calendar on your behalf |
| **Team Lead** | Participant | Can create/edit events to schedule team meetings |
| **Colleague** | Viewer | Should see your availability without modifying |
| **Project Team** | Viewer (time-focused) | Only needs to know when you're busy/free |

:::warning
Changes to delegation permissions take effect immediately. Double-check permission levels before saving.
:::

## Recipient-Side View

When a resource is shared to you:

1. The shared resource appears in your module navigation (e.g., Calendar → Shared Calendars)
2. Permission level determines what you can do:
   - **Viewer:** Items appear fused or overlaid but are read-only
   - **Participant:** Appears in your view, you can add/edit but deletions restricted
   - **Administrator:** Full edit and delete access

## Troubleshooting

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Share button not visible | ACLs disabled in configuration | Ask administrator to enable `SOGoACLsSendEMailNotifications` |
| Cannot find user in search | User doesn't exist in SOGo | Verify recipient has SOGo account |
| Cannot select Admin permission | You are not resource owner | Only owner can grant Administrator access |
| Shared resource not appearing | Sharing not yet synced or network issue | Refresh the page or re-login after a few seconds |
| Delegation not working for mail | Mail sharing disabled | Check `SOGoMailAuxiliaryUserAccountsEnabled` in SOGo config |

## Security Considerations

1. **Principle of Least Privilege** — Grant the minimum permission needed
2. **Auditing** — Periodically review who has access to your resources
3. **When to Revoke** — Remove delegation when collaboration ends or roles change
4. **Confidential Information** — Be cautious with shared calendars that contain sensitive meetings

## Advanced Delegation with Resources

For rooms, projectors, or equipment:

| Resource Type | How to Set Up |
|---------------|---------------|
| **Meeting Room** | Create resource account, set as resource type |
| **Projector** | Add to calendar, mark as resource, grant booking permissions |
| **Equipment** | Create as shared calendar item, enable resource booking |

:::info
Resource configuration typically requires administrator-level access to SOGo automated setup. Individual users delegate calendar items as regular events.
:::
