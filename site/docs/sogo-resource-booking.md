---
title: "Resource Booking (Rooms, Equipment)"
description: "Book shared resources like meeting rooms and equipment"
sidebar_label: "Resource Booking"
---

# Resource Booking

Reserve and schedule shared resources — meeting rooms, projectors, labs, or equipment — through SOGo's integrated calendar resource booking.

:::info
Resource booking in SOGo is typically implemented as special calendar accounts marked as resources. Your administrator configures these resource accounts, and they appear as available rooms or equipment when scheduling meetings.
:::

## Prerequisites

- A SOGo 5 account with valid credentials
- Logged into SOGo 5
- Resource accounts configured by administrator
- Calendar module access

## Resource Booking Overview

| Resource Type | Example Use Case |
|---------------|------------------|
| **Meeting Room** | Small team huddle room, board room, conference hall |
| **Equipment** | Projector, video conference system, specialized lab equipment |
| **Vehicle** | Company car, maintenance vehicle |
| **Other** | Training workstation, demo environment |

## Step-by-Step Instructions

### Step 1: Open Calendar

Click **Calendar** in the navigation sidebar.

### Step 2: Create a New Event

1. Click the **+** (plus) button
2. Or double-click on a time slot in the calendar grid

### Step 3: Add Attendees

In the event dialog:

1. Expand or click **Attendees**
2. Search for or select your colleagues (for notification purposes)
3. Find and add the **resource** — this may appear as:
   - A special resource tab or icon
   - A list of rooms/equipment you can choose from
   - An auto-complete suggestion when you type resource name

:::tip
Resources often appear with a location icon (📍) or are labeled as [Room] or equipment name in the auto-complete.
:::

### Step 4: Select Time Slot

Choose the date/time for the booking. SOGo shows resource availability:

| Visual Indicator | Meaning |
|------------------|---------|
| **Green/H highlighted** | Resource available (can book) |
| **Grayed out** | Already booked (conflict) |
| **Partially h available** | Partial availability (some resource in use) |

### Step 5: Confirm Booking

1. Add event title and details
2. Confirm resource is listed in attendees
3. Click **Save** or **Create**

SOGo checks for conflicts:
- **No conflict:** resource is booked, attendees notified
- **Conflict exists:** SOGo may:
  - Show conflict, prevent booking
  - Allow booking but show warning

### Step 6: View Resource Availability

Optionally, to view a resource's schedule:

1. In Calendar, find the **Resources** section or navigation
2. Click on the resource (e.g., "Conference Room A")
3. View the resource's calendar as a separate tab

:::info
Some configurations allow you to overlay multiple resources to find common availability.
:::

## Resource Configuration (Administrator)

Resource accounts are typically created with these attributes:

| Setting | Value |
|---------|-------|
| **User Role** | Resource (not person) |
| **Location** | Physical address or room number |
| **Capacity** | Number of people that can be accommodated |
| **Equipment List** | Specific equipment available in resource |

:::note
Setting up resources requires administrative access to SOGo automated scripts or direct database edits. Ask your admin if a resource you need is not available.
:::

## Best Practices

1. **Book in advance** — resources are shared; last-minute booking may fail.
2. **Provide details** — in the event description, include meeting purpose, needed preparation, number of attendees.
3. **Be considerate** — if you just need a few minutes, don't block for a full day if not necessary.
4. **Release when done** — if you finish early or the meeting cancels, remove the event/booking.
5. **Avoid double-booking yourself** — resource system checks conflicts for you, but be judicious.

## Managing Bookings

| Action | How To |
|--------|--------|
| **Modify booking** | Find event in calendar, edit start/end time or update attendees, save |
| **Cancel booking** | Delete event (if you are the event owner) |
| **Check availability** | View resource calendar directly; see all bookings |
| **Resolve conflicts** | If conflict warning appears, choose alternative time slot |

## Permissions and Delegation

- Only users with permission to schedule on a resource can book it
- An administrator may restrict who can book certain high-demand resources
- Some resources auto-accept bookings, others require confirmation by resource manager

## Troubleshooting

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Cannot find resource in attendees | Resource not configured outside calendars | Ask admin to make resource bookable; ensure it's listed as a shareable calendar |
| Booking fails with conflict | Time slot already booked | Choose another time slot with available resource |
| Resource not appearing as category | Configured for specific groups only | Check with admin if you have permission to book this resource |
| Resource calendar can't be viewed | Permissions restrict read access | Contact admin for view access |

## Integration with Other Features

| Integration | Notes |
|------------|-------|
| **Free/busy** | Resource busy times shown in free/busy free-for-all queries |
| **Calendar sharing** | Share your calendar with resource team to coordinate scheduling |
| **Email notifications** | Attendees and resource managers can receive booking confirmations |

:::info
In larger organizations, resource booking may require additional scheduling tools or connector integrations. This covers the core SOGo scenario where resources are modeled as special calendars.
:::
