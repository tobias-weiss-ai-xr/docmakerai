---
title: "Writing Papers (Typst)"
sidebar_label: "Papers (Typst)"
sidebar_position: 23
description: "Typesetting papers in the browser — Typst collaboration with live preview"
---
import PageSEO from '@site/src/components/PageSEO';

<PageSEO
  title="Writing Papers (Typst)"
  description="Typesetting papers in the browser — Typst collaboration with live preview"
  keywords={["Writing", "Papers", "Typst", "openEduSuite"]}
  suffix="openEduSuite"
  defaultKeywords={["higher education", "open source"]}
/>


# Writing Papers (Typst)

The openEduSuite's [writing studio](https://toss.openedusuite.org) is
built around [Typst](https://typst.app) — the modern typesetting
engine that turns plain text into polished PDFs, without LaTeX's
steep edges. In the browser you write, the preview builds itself
live, and the PDF export is one click.

![Typst projects: create a new project](./assets/toss-projects.png)

## Signing In

From the [portal](/suite/portal) tile, sign in with your openEduSuite account — single sign-on takes you
straight to your **Projects** page. It lists your papers with
owner and last-edited date, each with **Open**, **Rename**,
**Copy**, and **Archive** actions, and switches between **Active**
and **Archived**. The navigation offers **Gallery**, **Profile**,
and **Tasks** alongside, plus **Help** — a help center with guides
on getting started, editing and preview, packages, and LaTeX
projects.

## Starting a Paper

**Create Project** opens the small form: give your paper a
**Project name**, pick **Typst** as the project type (LaTeX sits
next to it), and **Create** opens the editor. **Browse templates**
leads to the gallery of maintained starting points. The editor
carries the tabs **View**, **Files**, **Preview**, **Settings**,
and **Revisions**; source text on one side, the rendered preview
on the other. Typst's markup is lighter than LaTeX: `=`
headings, `-` lists, `$…$` math. When the paper is ready, the
preview panel's **Download PDF** button exports it.

## Why Typst

- **Fast feedback** — the preview follows your typing, not a compiler
- **Gentle syntax** — readable source that still typesets tables,
  figures, math, and bibliographies
- **In the browser** — nothing to install; your projects wait in
  the studio wherever you sign in

For longer documents that outgrow a chat or the [wiki](/suite/xwiki),
the studio is the place — and finished PDFs fit right into your
[cloud files](/suite/files).

If the service stays closed to you, the
[helpdesk](/suite/helpdesk-create-ticket) reaches its operators.

## Accessibility

| Action | Key |
|--------|-----|
| Move through projects and forms | `Tab` |
| Confirm the focused form control | `Enter` |

- The pages are ordinary web elements: `Tab` moves you through the
  project list and the create form, `Enter` confirms.
- In the editor, `Escape` closes overlays and dialogs; if you lose
  your orientation, `Ctrl+Home` (German keyboards: `Strg+Pos1`)
  returns you to the top of the page.

- **High contrast and dark mode:** contrast and dark themes come from the
  operating system or browser — Windows `Win+Ctrl+C`, macOS *Increase contrast*,
  or a browser extension such as Dark Reader. If the app offers its own dark
  theme, switch it in its settings; the navigation described above still applies.
