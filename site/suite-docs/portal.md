---
title: "The Portal"
sidebar_label: "Portal"
sidebar_position: 13
description: "Your digital workplace: news, events, and every openEduSuite app in one place"
---
import PageSEO from '@site/src/components/PageSEO';

<PageSEO
  title="The Portal"
  description="Your digital workplace: news, events, and every openEduSuite app in one place"
  keywords={["The", "Portal", "openEduSuite"]}
  suffix="openEduSuite"
  defaultKeywords={["higher education", "open source"]}
/>


# The Portal

The [portal](https://home.openedusuite.org) is the entry point of the
openEduSuite: your digital workplace. You can read it without signing in —
it then shows the weather for Marburg, the university news, and the events
calendar. The language selector in the top bar switches the portal between
Deutsch, English, Français and 中文.

![Portal (signed out): news, weather and events of the university](./assets/portal-public.png)

## Signing In

Choose **Anmelden** in the top bar (**Login** when the portal runs in
English) and sign in with your openEduSuite account — the same login that
works everywhere in the suite. See
[Signing In: One Login for All Apps](/suite/sso-login) for details.

After signing in, the portal shows your personal digital workplace: the
app tiles plus weather, news and events. The top bar now holds **Konto**
(**Account** in English), which opens the
[account console](/suite/sso-account) in a new tab, and **Abmelden**
(**Logout**), which signs you out.

![Portal (signed in): the full app tile list](./assets/portal-apps.png)

## The App Tiles

Signed in, the portal sorts its tiles under two headings:

- **Dienste** (**Services**) — the apps of the suite itself
- **Universität** (**University**) — tiles that lead out of the suite, to
  services of the university

Two buttons above the grid switch the view: **Kacheln** (**Tiles**) is the
grid you see first, **3D-Ansicht** (**3D view**) lays the tiles out as a
scene you can turn and zoom — the portal says "Drag to rotate · Scroll to
zoom · Click to open a service". The search field
**Dienste filtern …** (**Filter services…**) hides every tile that does
not match your text while you type.

Tile names follow the interface language, so the tables below give both
spellings. Where we have a guide, it is linked.

### Dienste (Services)

| Tile (German) | Tile (English) | Our guide |
|---------------|----------------|-----------|
| E-Mail & Kalender (SOGo6) | E-Mail & Calendar (SOGo6) | Mail, calendar, address book — the [SOGo 6 guides](/sogo6/) |
| SOGo Beschäftigten-Post | SOGo Staff Mail | [Mail classic: SOGo (Staff & Students)](/suite/sogo-classic), webmail for staff accounts |
| SOGo Studierenden-Post | SOGo Student Mail | [Mail classic: SOGo (Staff & Students)](/suite/sogo-classic), webmail for student accounts |
| Automatisierung (n8n) | Automation (n8n) | [Automation with n8n](/suite/n8n) |
| KI-Anwendungen (Dify) | AI Applications (Dify) | [Build Your Own AI Assistants (Dify)](/suite/dify) |
| Operaton | Operaton | [Processes and Tasks (Operaton)](/suite/operaton-tasks) |
| Scientific Workflows (EWOKS) | Scientific Workflows (EWOKS) | [Workflows (EWOKS)](/suite/ewoks) |
| OpenProject | OpenProject | [Projects and Tasks (OpenProject)](/suite/openproject) |
| Tickets & Service Desk (RT) | Tickets & Service Desk (RT) | [Helpdesk: Create a Ticket](/suite/helpdesk-create-ticket) |
| OpenCloud | OpenCloud | [Files with OpenCloud](/suite/files) |
| Nextcloud | Nextcloud | [Files (Nextcloud)](/suite/nextcloud) |
| Element Chat | Element Chat | [Chat (Element)](/suite/chat) |
| BigBlueButton (intern) | BigBlueButton (internal) | [Video Conferences (BigBlueButton)](/suite/bbb) |
| XWiki | XWiki | [Wiki (XWiki)](/suite/xwiki) |
| XWiki Beschäftigte | XWiki Staff | the staff wiki in [Wiki (XWiki)](/suite/xwiki) |
| Typst | Typst | [Writing Papers (Typst)](/suite/typst) |
| TOSS (Typst Server) | TOSS (Typst Server) | the writing studio in [Writing Papers (Typst)](/suite/typst) |
| Forum (Discourse) | Forum (Discourse) | [Forum (Discourse)](/suite/discourse) |
| HedgeDoc | HedgeDoc | [Notes (HedgeDoc)](/suite/hedgedoc) |
| Event-Management (Indico) | Event Management (Indico) | [Events (Indico)](/suite/indico) |
| Digitalisierung / Workflow (Kitodo) | Digitization / Workflow (Kitodo) | [Library (Kitodo)](/suite/kitodo) |
| Formulare & Erfassung (Grist) | Forms & Data Capture (Grist) | [Forms and Tables (Grist)](/suite/grist) |
| Terminbuchung (calrs) | Bookings (calrs) | [Bookings (calrs)](/suite/calrs) |
| Diagramme (draw.io) | Diagrams (draw.io) | [Diagrams (draw.io)](/suite/drawio) |
| Whiteboard (Excalidraw) | Whiteboard (Excalidraw) | [Whiteboard (Excalidraw)](/suite/excalidraw) |
| LaTeX (Overleaf) | LaTeX (Overleaf) | [LaTeX (Overleaf)](/suite/overleaf) |
| Lernplattform (ILIAS) | Learning platform (ILIAS) | [Learning platform (ILIAS)](/suite/lms) |
| Open WebUI | Open WebUI | [AI Chat (Open WebUI)](/suite/ai-chat) |
| OpenScience | OpenScience | [OpenScience](/suite/openscience) |
| F13 | F13 | [Text Assistance (F13)](/suite/f13) |

### Universität (University)

These tiles leave the suite for services of the university, so they have
no guide here: **MARVIN**, the campus management system; **ILIAS**, the
university-wide learning platform (the suite's own ILIAS is the
**Lernplattform (ILIAS)** tile above, described in
[Learning platform (ILIAS)](/suite/lms)); **next.hessenbox** for cloud
sync and share; the **Personenverzeichnis** staff directory; and
**BigBlueButton (Uni)**, the university's own video conference instance.

Not every tile is for everyone: what you see depends on your role and on
which services your institution runs. If a service you need is missing or
stays dark, ask at the [helpdesk](/suite/helpdesk-create-ticket).

## Accessibility

| Action | Key |
|--------|-----|
| Move through links and tiles | `Tab` |
| Open the focused link or app | `Enter` |

- The portal is built from ordinary links and tiles: `Tab` moves you
  through them in reading order, `Enter` opens the focused element. The
  filter field **Dienste filtern …** takes plain text — type a service
  name and the grid narrows to the matching tiles.
- Screenreader users reach the app list under the headings **Dienste**
  and **Universität**; every tile name is a heading of its own, sitting
  inside the link that opens the service.
- If you lose your orientation, press `Ctrl+Home` (German keyboards:
  `Strg+Pos1`) to return to the top of the page.

- **High contrast and dark mode:** contrast and dark themes come from the
  operating system or browser — Windows `Win+Ctrl+C`, macOS *Increase contrast*,
  or a browser extension such as Dark Reader. If the app offers its own dark
  theme, switch it in its settings; the navigation described above still applies.
