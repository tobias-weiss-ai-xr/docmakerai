---
title: "Workflows (EWOKS)"
sidebar_label: "Workflows (EWOKS)"
sidebar_position: 28
description: "Build scientific workflows in the browser and follow their execution"
---

# Workflows (EWOKS)

[EWOKS](https://ewoks.openedusuite.org) is the openEduSuite's
workflow editor, built on the [ewoks](https://ewoks.readthedocs.io)
workflow system of the ESRF. Open the [portal](/suite/portal) tile
**Scientific Workflows (EWOKS)** and sign in with SSO — the editor
starts in the **Edit** view. The header names the app **EwoksWeb** and
offers two tabs:

- **Edit** — build a workflow as a graph: tasks are nodes, connections
  carry data from one task to the next.
- **Monitor** — the execution view: it reads the execution events the
  server records. It needs that events backend to be running; when the
  backend is down, the view reports a failed request instead of
  listing executions.

![The EWOKS workflow editor](./assets/ewoks.png)

## Building a Workflow in Edit

The heading above the canvas names the workflow — a fresh one is
**Untitled workflow (unsaved)**. The toolbar beside it holds:

- **Quick Open** — a search field listing the workflows saved on the
  server, grouped by category; the **Open** icon in the toolbar leads
  to the same field. This instance offers the **demo** workflow under
  **No category**: picking an entry loads it into the editor, and the
  heading then shows its name.
- the save button — an icon that carries its state in its accessible
  name: **no changes**, or **changes pending** once you have edited.
- a menu with more actions: **New workflow** (`Ctrl+Shift+N`),
  **Open from disk**, **Download**, **Execute workflow**
  (`Ctrl+Shift+X`), **Save as...**, **Delete workflow**,
  **Manage icons**, and **Create new task**.

**DISCOVER TASKS** on the left lists the task packages, ready to be
unfolded. **ewokscore** holds computing tasks (such as `add`,
`append`, or `SumTask`); **General** holds the building blocks
`graphInput`, `graphOutput`, `taskSkeleton`, `note`, and
`subworkflow`. The **DISCOVER TASKS** button opens a dialog of the
same name: enter a **Module name** — or tick
**Discover from all modules in the current Python environment** —
and press **Discover** to pull further packages into the panel.

Drag a task from the list onto the canvas; the node appears with a
generated label such as `SumTask0`, and the empty canvas says so
itself: "Drag and drop tasks here to start building your workflow".
Connect the nodes so the data has a path. Icon buttons at the canvas
edge offer **Zoom In**, **Zoom Out**, **Fit View**, and
**Toggle Interactivity**.

The panel on the right edits whatever is selected:

- Nothing selected — **Workflow** properties: Label, Comment,
  Category, and Canvas Background Color.
- Node selected — **Node** properties: Label and Comment,
  **Default Inputs** (columns Name, Type, Value, plus **ADD**),
  **Advanced** with **Force start node** and **Default Error Node**,
  **Task Info** (task identifier, node id, task type, category,
  required and optional inputs, outputs), and **Appearance**.

## When EWOKS, and When Not

- **Yes** — recurring, multi-step data processing: "whenever new
  data arrives, run these steps in this order" — reproducible and
  observable instead of a pile of scripts.
- **No** — one-off ad-hoc analysis (a notebook in
  [OpenScience](/suite/openscience) fits better) or simple automations
  that glue suite services together — that is [n8n](/suite/n8n)
  territory.

EWOKS workloads often run inside the workspaces of
[OpenScience](/suite/openscience); both tiles share the same SSO
account.

If the service stays closed to you, the
[helpdesk](/suite/helpdesk-create-ticket) reaches its operators.

## Accessibility

| Action | Key |
|--------|-----|
| Move through tabs, buttons, and dialogs | `Tab` |
| Open the focused link or button | `Enter` |

- Both tabs are ordinary links; toolbar, task list, canvas controls,
  and dialogs are buttons — `Tab` reaches them in order.
- The editor states its canvas keys itself: select a node with Enter
  or Space, move it with the arrow keys, remove it with Delete,
  cancel with Escape. Edges behave the same way.
- The action menu shows its shortcuts: `Ctrl+Shift+N` for
  **New workflow**, `Ctrl+Shift+X` for **Execute workflow**.
- `Ctrl+Home` (German keyboards: `Strg+Pos1`) jumps back to the
  top of the page.

- **High contrast and dark mode:** contrast and dark themes come from the
  operating system or browser — Windows `Win+Ctrl+C`, macOS *Increase contrast*,
  or a browser extension such as Dark Reader. If the app offers its own dark
  theme, switch it in its settings; the navigation described above still applies.
