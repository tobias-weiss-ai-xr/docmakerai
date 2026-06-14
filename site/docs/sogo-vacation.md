---
title: "Vacation & Out-of-Office"
description: "Set up automatic email replies and calendar blocks for your absence"
sidebar_label: "Vacation & Out-of-Office"
---

# Vacation & Out-of-Office

Configure automatic email replies and mark yourself as away
in the calendar when you're on vacation or out of office.

## Prerequisites

- A SOGo account with valid credentials
- You are logged into SOGo
- Vacation/auto-reply must be enabled by your administrator
  (`SOGoVacationEnabled = YES`)

## Step-by-Step Instructions

### Step 1: Open Vacation Settings

1. Click the **gear icon** ⚙ (Settings) in the top toolbar
2. Select **Vacation** from the settings menu

![Vacation settings menu](./assets/02-dashboard.png)

### Step 2: Enable Auto-Reply

Toggle **Enable auto-reply** to **ON**.

### Step 3: Set the Date Range

| Field | Description | Example |
|-------|-------------|---------|
| **Start date** | When your absence begins | 2026-07-15 |
| **End date** | When you return | 2026-07-28 |
| **Time zone** | Your local timezone | Europe/Berlin |

The auto-reply activates on the start date at 00:00 and deactivates
after the end date at 23:59.

:::tip
Set the range to include travel days — enable it the evening before
you leave and disable it the morning after you return.
:::

### Step 4: Write Your Auto-Reply Message

Compose the message that will be sent to people who email you:

```
Subject: Out of office — John Doe

Thank you for your message.

I am out of the office from July 15 to July 28, 2026,
with limited access to email.

For urgent matters, please contact Jane Smith
(jane.smith@company.com).

Best regards,
John Doe
```

### Step 5: Choose Reply Options

| Option | Description |
|--------|-------------|
| **Send reply to** | Everyone, or only people in your contacts/address book |
| **Repeated replies** | Send once per sender (default) or every time they write |
| **Keep original subject** | Add `Re:` or keep the original subject line |

**Recommended:** Send once per sender to avoid flooding colleagues
who email multiple times.

### Step 6: Save

Click **Save** or **Apply**. The Sieve script is activated on the
mail server.

## Calendar: Marking Your Absence

While you're configuring vacation, also block your calendar:

### Create a Vacation Event

1. Open the **Calendar** module
2. Create a new event covering your absence period
3. Set it as an **All-day** event
4. Add "Out of Office" or "Vacation" as the title
5. Mark it as **Busy** or **Out of Office** in the visibility settings
6. Save

This blocks the time so colleagues see you're unavailable when
checking free/busy.

## Testing Your Setup

### Send a Test Email

1. Send an email to your SOGo address from another account
2. You should receive the auto-reply within a few minutes
3. The auto-reply only fires once per sender (per configured rule)

### Check Vacation Status

Re-open **Settings** → **Vacation** to verify:
- The toggle shows **ON**
- Date range is correct
- Message is saved

## Disabling Auto-Reply

When you return:

1. Go to **Settings** → **Vacation**
2. Toggle **Enable auto-reply** to **OFF**
3. Click **Save**

The auto-reply stops immediately. Optionally delete the
calendar block event.

## Troubleshooting

### Auto-reply not sending

- Check that vacation is enabled by your administrator
- Verify the Sieve server is running (`SOGoSieveScriptsEnabled`)
- The auto-reply only sends once per sender — test with a different
  email address
- Check that the date range includes the current date

### "Sieve script error" when saving

- The Sieve server may be unavailable
- Contact your administrator to check the Sieve service
- Simplify the message text (special characters can cause issues)

## Conclusion

Vacation auto-reply ensures people know you're away without
leaving them wondering. Combined with a calendar block,
colleagues can see your availability at a glance.
