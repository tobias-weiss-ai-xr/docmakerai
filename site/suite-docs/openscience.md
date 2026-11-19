---
title: "OpenScience"
sidebar_label: "OpenScience"
sidebar_position: 29
description: "Research workspaces, sessions, and files in one place"
---

# OpenScience

[OpenScience](https://science.openedusuite.org) is the suite's AI
research workbench — the portal tile describes it as agents, tools,
and data workflows directly in the browser. Reach it through the
portal tile **OpenScience** and sign in with SSO; the projects
overview opens right away.

![OpenScience projects overview](./assets/science.png)

## The Projects Overview

The page opens on a list titled **Projects** — "Research workspaces,
sessions, and files in one place."

- Each project card shows its name, its session count, and its status
  with the last activity as a relative time ("Active", with a German
  browser "vor 10 Tagen").
- Each card offers **Pin** and **Archive**. The **Archived** filter
  carries a count and lists archived projects, each with a
  **Restore** button.
- **New project** opens a **Create project** dialog: name the
  workspace, optionally connect source folders now or later, then
  choose **Create** or **Cancel**.

## Inside a Project

Opening a project leads to its workspace. The sidebar carries:

- **New** — starts a new session; the command palette calls it
  "Start a new research conversation".
- **Search** — the command palette. It searches sessions, transcript
  messages, workspace files, artifacts, and project actions, and
  gathers the app's actions in one list (from **New session** to
  **Open settings** and **Open documentation**).
- **Customize** — the settings (see below).
- The workspace actions **Files**, **Terminal**, **Compute**, and
  **Autoresearch**.
- **Sessions** — the project's session list, with a **New session**
  button.

What the workspace actions show:

- **Files** — the project's files, with a **More** menu ("Add
  folder…", "Manage workspace folders…"). An empty folder says
  "This folder is empty".
- **Terminal** — commands inside the project; without a connection
  to the local OpenScience server it reports "Local terminal
  unavailable".
- **Compute** — the machine behind the project ("This computer"):
  active and running counts, memory, and CPU cores.
- **Autoresearch** — studies that hill-climb a metric, each with its
  score, its runs, and its queue. An empty project says "No studies
  yet" and suggests asking in a session for a study: the metric to
  improve, the budget, and the script to run.

## Settings and Language

**Customize** opens the **Settings** dialog with sections for
Account, General, Workspaces, Models, Research, Skills, Tools,
Connectors, Credentials, and System (compute, permissions, network,
sandbox, storage). **General** holds the theme (System, Light, Dark)
and the display language: OpenScience follows your browser's
language, so with a German browser much of the interface appears in
German ("Erscheinungsbild", "Hell" and "Dunkel", "Terminal
umschalten") while the rest stays English. The **Open documentation**
entry in the command palette leads to the project's README on GitHub.

## OpenScience and Its Neighbors

- **[EWOKS](/suite/ewoks)** — reproducible, multi-step processing as
  a workflow; OpenScience's autoresearch studies instead hill-climb
  a single metric, run by run.
- **[Nextcloud](/suite/nextcloud)** and
  **[OpenCloud](/suite/files)** — plain file storage without compute
  sessions.
- A project is the unit: its sessions, files, and artifacts are all
  reachable from its command palette.

## Accessibility

| Action | Key |
|--------|-----|
| Move through projects, buttons, and menus | `Tab` |
| Open the focused element | `Enter` |

- The projects overview is an ordinary list with buttons — `Tab`
  walks it in order.
- The command palette is keyboard-first: its footer shows the keys
  (arrow keys navigate, `Enter` opens, `Esc` closes).
- The palette lists Ctrl+` (the backtick key) as the shortcut for
  toggling the project terminal.
- `Ctrl+Home` (German keyboards: `Strg+Pos1`) returns you to the
  top of the page.
