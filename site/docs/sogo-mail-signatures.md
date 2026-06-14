---
title: "Mail Signatures & Identities"
description: "Set up email signatures and multiple sender identities"
sidebar_label: "Mail Signatures & Identities"
---

# Mail Signatures & Identities

Configure professional email signatures and manage multiple
sender identities (e.g., work vs. personal email).

## Part 1: Creating an Email Signature

### Step 1: Open Settings

1. Click the **gear icon** ⚙ (Settings) in the top toolbar
2. Select **Mail** → **Signatures**

![Mail signatures settings](./assets/01-mail-signatures.png)

### Step 2: Add a New Signature

Click **Add Signature** or the **+** button.

### Step 3: Write Your Signature

Enter your signature text. SOGo 5 supports **plain text** signatures.

**Recommended signature format:**
```
Best regards,
John Doe
Project Manager | Company Name
Phone: +49 123 456 789
Email: john.doe@company.com
```

### Step 4: Choose Signature Placement

Select when the signature is inserted:

| Option | Behavior |
|--------|----------|
| **Append to new messages only** | Signature added to new emails, not replies |
| **Append to all messages** | Added to both new and replied/forwarded messages |
| **No automatic insertion** | Manually insert via the compose toolbar |

### Step 5: Set as Default

If you have multiple signatures, choose which one is used by default.

### Step 6: Save

Click **Save** to apply.

## Part 2: Inserting Signature Manually

When composing a message, you can insert a signature:

1. Click the **Signature** button in the compose toolbar
2. Select which signature to insert
3. The signature is added at your cursor position

## Part 3: HTML Signatures (Advanced)

SOGo 5 primarily supports plain text signatures. For rich signatures
with images or formatting:

1. Create your HTML signature in an external editor
2. Copy the formatted content (e.g., from Gmail or Outlook)
3. Paste it into the signature field — SOGo 5 preserves basic formatting

:::tip
**Best practice:** Keep signatures plain text for maximum
compatibility across email clients.
:::

## Part 4: Managing Identities

Identities let you send email as different addresses from the same
SOGo 5 account.

### Step 1: Open Settings

Go to **Settings** → **Mail** → **Identities**

### Step 2: View Your Identities

You'll see your primary identity (the email address associated with
your SOGo 5 account). Additional identities may appear if configured
by your administrator.

### Step 3: Add an Auxiliary Identity

If enabled by your administrator (`SOGoMailAuxiliaryUserAccountsEnabled`):

1. Click **Add Identity**
2. Enter:
   - **Full Name** — Display name for recipients
   - **Email Address** — The address to send from
   - **Reply-to Address** — (optional) Different address for replies
3. Click **Save**

### Step 4: Switch Identity When Composing

When writing a new message:

1. Look for the **From** field in the compose window
2. Click the dropdown arrow next to your email address
3. Select which identity to send as

## Example: Work + Personal Setup

```
Identity 1 (Default):
  Name:  John Doe
  Email: john@company.com
  Signature: Professional (title, phone, company)

Identity 2 (Auxiliary):
  Name:  John D.
  Email: john.doe@gmail.com
  Signature: Casual (name only)

When composing a personal email, switch to Identity 2.
Work emails default to Identity 1.
```

## Conclusion

Signatures and identities help you communicate professionally.
Set up a clean signature and add auxiliary identities if you
manage multiple email addresses.
