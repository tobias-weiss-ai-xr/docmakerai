---
title: "Logout"
description: "How to securely log out of SOGo 6"
sidebar_label: "Logout"
---

import PageSEO from '@site/src/components/PageSEO';

<PageSEO title="Logout" description="How to securely log out of SOGo 6 — end your session with the power icon" keywords={["logout", "sign out", "session", "security", "SOGo 6"]} />

# Logout

Click the **power icon** ⏻ in the top-right toolbar to end your SOGo 6 session. You'll be redirected to the login page.

:::tip
On shared or public computers, always log out when you're done. Don't just close the browser tab.
:::

## Troubleshooting

| Issue: Description | Cause: What went wrong | Solution: How to fix it |
|-------|-------|----------|
| Logout button not visible | Narrow screen | Widen the window or click the menu (☰) first |
| Session still active after logout | Cached page | Clear browser cache and close all SOGo tabs |

## Accessibility

### Keyboard Navigation

SOGo 6 supports full keyboard navigation for logout.

| Action | Keyboard Shortcut: What key to press | Notes: Additional information |
|--------|----------------------------------|---------------------------|
| | Navigate to power icon | `Tab` to top toolbar |
| | Activate logout | `Enter` on power icon |
| | Confirm logout | `Enter` on dialog (if shown) |

### Screen Reader Workflow

1. `Tab` through toolbar until "Power icon, button" is announced
2. `Enter` to click logout
3. Screen reader announces: "Logout successful" or redirect to login page
4. You are returned to the login page, session ended

### High Contrast Mode

SOGo 6 currently does not have built-in high contrast mode. Browser/OS-level alternatives:
- **Windows:** `Win+Ctrl+C` toggles high contrast
- **macOS:** System Preferences → Accessibility → Display → Increase contrast
- **Browser Extensions:** Dark Reader, High Contrast (Chrome)
