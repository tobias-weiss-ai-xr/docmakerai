---
title: "Tasks / To-Do Module"
description: "Create and manage task lists in SOGo 5"
sidebar_label: "Tasks / To-Do"
---

import PageSEO from '@site/src/components/PageSEO';

<PageSEO title="Tasks / To-Do Module" description="Step-by-step tutorial to create and manage task lists in the SOGo 5 task management module" keywords={["tasks", "todo", "task management", "priorities", "productivity"]} />

# Tasks / To-Do Module

Organize tasks, set priorities, and manage to-do items within SOGo 5's task management module.

:::info
In many SOGo deployments, the Tasks module appears only when `SOGoDocumentsEnabled` is set to `YES` in the server configuration. Your administrator may also need to enable the Tasks module explicitly via additional server settings.
:::

## Prerequisites

- A SOGo 5 account with valid credentials
- Tasks module enabled in SOGo configuration
- You are logged into SOGo 5

## Features Overview

| Feature | Description |
|---------|-------------|
| **Task Lists** | Create multiple task categories (e.g., personal, work, projects) |
| **Priority Levels** | Urgent, High, Medium, Low tags |
| **Due Dates** | Set deadlines and过期 reminders |
| **Status Tracking** | Pending, In Progress, Completed, Deferred |
| **Integration** | Link tasks to events, contacts |

## Step-by-Step Instructions

### Step 1: Open Tasks Module

In the navigation sidebar, click **Tasks** or **To-Do** to enter the module.

:::tip
If Tasks does not appear in the sidebar, contact your administrator to enable it through the `SOGoDocumentsEnabled` configuration and restart SOGo.
:::

### Step 2: Create a New Task

#### Option A: Quick Add
1. Click the **+ Task** button (near the top of the task view)
2. Enter task title
3. Press Enter or click off the input field to save

#### Option B: Detailed Add
1. Click **New Task** or **Create Task**
2. Fill in the task details:
   - Title
   - Description
   - Priority
   - Due date
   - Related project or list

### Step 3: Edit Task Details

After creation, click on the task to open the detail view and modify:

| Field | Description |
|-------|-------------|
| **Title** | Short task name |
| **Description** | Detailed notes about the task |
| **Due Date** | When the task must be completed |
| **Priority** | Urgent, High, Normal, Low |
| **Status** | Pending, In Progress, Completed, Deferred |
| **Complete** | Checkbox to mark as done |
| **Percent Complete** | Slider for progress tracking |
| **Category / List** | Choose which task list to assign to |

### Step 4: Organize Tasks by Lists

Create or select task categories:

1. Click the **Lists** or **Categories** icon in the toolbar
2. Click **New List**
3. Name the list (e.g., "Work", "Personal", "Project X")
4. Click **Save**

Drag tasks to reorder within lists.

### Step 5: Set Reminders

For important tasks:

1. Click the task to open details
2. Click **Add Reminder**
3. Specify timing:
   - **On Due Date** — at the exact due time
   - **Minutes Before** — advance notification
   - **Days Before** — for longer reminders

:::note
Wait management relies on SOGo's mail and alert infrastructure. Ensure your email is configured properly to receive task reminders.
:::

## Views and Sorting

| View | Use Case |
|------|---------|
| **All Tasks** | Overview of everything pending |
| **Due Soon** | Focus on upcoming deadlines |
| **Priority** | Sort by urgency then by due date |
| **Category** | Filter by list/project |
| **Completed** | Review finished tasks |

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| New task | `Ctrl + N` / `⌘ + N` |
| Complete task | Checkmark next to item or `Ctrl + Enter` |
| Delete task | `Delete` key |
| Undo complete | `Ctrl + Z` / `⌘ + Z` |

## Tasks Integration

SOGo Tasks can be linked with:

| Integration | How To |
|------------|--------|
| **Calendar** | Convert an event invitation to a task; set task due date to event date |
| **Contacts** | Assign owner or delegate from address book |
| **Mail** | Create task from email content (forward to task list) |

:::tip
Use tasks to follow up on meeting actions. After a meeting, create tasks for deliverables or next steps.
:::

## Best practices

1. **Use clear, specific titles:** "Call Sarah" is better than "Phone" if it explains who and what.
2. **Set realistic due dates:** Avoid overcommitting on timing.
3. **Review regularly:** Schedule time weekly to review and update tasks.
4. **Delete completed tasks:** keep the task list clean. Archive rather than delete if you might need history.
5. **Delegate where appropriate:** If someone else should handle it, mention in the description or create a task for them.

## Troubleshooting

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Tasks module not visible | `SOGoDocumentsEnabled` set to NO | Ask admin to enable in SOGo config |
| Cannot create task | Write permissions missing on task list | Check ACLs on the task list |
| Task reminders not arriving | Mail not configured or tasks disabled | Verify mail server settings are correct |
| Task list not syncing | Network issue or server problem | Refresh the page or re-login |
| Cannot change priority or due date | Task locked by external system (e.g., mobile app) | Complete current change and retry after a sync cycle |
