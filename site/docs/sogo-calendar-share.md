---
title: "Share a Calendar"
description: "Share your SOGo calendar with colleagues and set permissions"
sidebar_label: "Share a Calendar"
---

# Share a Calendar

This tutorial explains how to share your SOGo calendar with other users
and control what they can see or do.

## Prerequisites

- A SOGo account with valid credentials
- You are logged into SOGo
- You have at least one calendar (e.g., the default "Personal" calendar)

## Step-by-Step Instructions

### Step 1: Open Calendar Settings

1. In the sidebar navigation, click **Calendar**
2. In the top toolbar, click the **gear icon** ⚙ (Settings)
3. Select **Calendar** from the settings menu

Alternatively, right-click on a calendar name in the left sidebar
and select **Properties** or **Sharing**.

### Step 2: Choose a Calendar to Share

![Calendar settings with sharing options](./assets/01-calendar-settings.png)

In the calendar list, you will see all your calendars:

- **Personal** — Your default calendar
- Any additional calendars you have created

Select the calendar you want to share.

### Step 3: Add a User

1. In the **Permissions** or **Sharing** tab, click **Add User**
2. Start typing the person's name or email address
3. Select them from the auto-complete list

### Step 4: Set Permission Level

Choose what the user can do:

| Permission | Can View | Can Create / Edit | Can Delete | Can Share |
|------------|----------|-------------------|------------|-----------|
| **Free/Busy** | ✅ Time slots only | ❌ | ❌ | ❌ |
| **View (read-only)** | ✅ All details | ❌ | ❌ | ❌ |
| **View + Respond** | ✅ All details | ❌ | ❌ | ❌ |
| **Modify** | ✅ All details | ✅ Own events | ✅ Own events | ❌ |
| **Modify All** | ✅ All details | ✅ Any event | ✅ Any event | ❌ |
| **Admin** | ✅ All details | ✅ Any event | ✅ Any event | ✅ Can add others |

**Recommended for most cases:** **Modify** allows a colleague to create
and edit events in your calendar.

### Step 5: Confirm the Share

Click **OK** or **Save** to apply the permission. The user will now be
able to access your calendar according to the permission level you set.

### Step 6: Verify (Optional)

To verify the share is working:

1. Open a **private/incognito browser window**
2. Log in as the user you shared with
3. Open the Calendar module
4. Check that your shared calendar appears in their calendar list

## Sharing via CalDAV (Advanced)

If you use a CalDAV client (Thunderbird, macOS Calendar, iOS):

1. Open your CalDAV client
2. Add a new calendar with the URL:
   ```
   https://your-sogo-instance/SOGo/dav/your-username/calendar/personal/
   ```
3. Enter your SOGo credentials
4. The calendar will sync automatically

Shared calendars will appear under the same CalDAV endpoint for users
who have been granted access.

## Remove or Change Sharing

To revoke or change access later:

1. Go to **Calendar Settings** → **Permissions**
2. Find the user in the list
3. To change: select a different permission level
4. To remove: click the **X** or **Remove** button next to their name

## Conclusion

You have successfully shared your calendar. Shared calendars are a great
way to coordinate team schedules, plan meetings, and keep everyone
on the same page.
