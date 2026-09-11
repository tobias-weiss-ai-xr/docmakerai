---
title: "Preferences — Spec-Based Guide"
description: "Spec-based guide covering SOGo preferences and utility workflows including general settings, password change, and vacation auto-reply."
sidebar_label: "Preferences Specification Guide"
---

import PageSEO from '@site/src/components/PageSEO';

<PageSEO title="Preferences — Spec-Based Guide" description="Spec-based guide covering SOGo preferences and utility workflows including general settings, password change, and vacation auto-reply." keywords="SOGo 6, preferences, settings, password, vacation, global search, spec" />

# SOGo Preferences

Capture SOGo preferences and utility workflows as annotated WebP animations
for the user guide. Covers general settings, password change, vacation
auto-reply configuration, and global search.

## Prerequisites

- authenticated session
- The user is in the password change settings
- The vacation settings page is open

## Step-by-Step Instructions

### Preferences and Settings

The capture pipeline will record navigating and modifying SOGo general
preferences and settings.

#### Step 1: Open the preferences/settings panel

The user opens the preferences/settings panel

**Expected result:**

- the general settings categories will be visible
- the WebP will annotate the navigation through settings

#### Step 2: The capture produces a >90% white frame

The capture produces a >90% white frame

**Expected result:**

- the pipeline will fall back to a textual description
- the documentation will note the capture was blank

:::note
This workflow is known to produce blank captures in the current pipeline. The documentation describes the expected behavior textually.
:::

### Password Change

The capture pipeline will record the password change workflow.

#### Step 1: Enter the current and new passwords

The user enters the current and new passwords

**Expected result:**

- the password will be updated
- the WebP will annotate the form interaction

#### Step 2: The capture produces a blank WebP

The capture produces a blank WebP

**Expected result:**

- the image reference will be removed from the documentation
- the documentation will describe the workflow textually

:::note
This workflow is known to produce blank captures in the current pipeline. The documentation describes the expected behavior textually.
:::

### Vacation Auto-Reply

The capture pipeline will record configuring the vacation auto-reply feature.

#### Step 1: Enable auto-reply and enters a message

The user enables auto-reply and enters a message

**Expected result:**

- the vacation reply will be activated
- the WebP will annotate the toggle and message input

#### Step 2: The capture produces a blank WebP

The capture produces a blank WebP

**Expected result:**

- the image reference will be removed from the documentation

:::note
This workflow is known to produce blank captures in the current pipeline. The documentation describes the expected behavior textually.
:::

### Global Search

The capture pipeline will record using the global search feature.

#### Step 1: Enter a search query in the global search bar

The user enters a search query in the global search bar

**Expected result:**

- results from mail, calendar, and contacts will be displayed
- the WebP will annotate the search input and results display

## Troubleshooting

preferences, password-change, vacation workflows produce blank captures — addressed textually in docs

## Related Sections

- [Auth Session](./sogo-spec-auth-session)

## Implementation Reference

Source: `capture/run_captures.py` — `record_preferences()`, `record_password_change()`, `record_vacation()`, `record_global_search()`

## Appendix: Scenario Reference

| Scenario | Precondition | Action | Expected Result |
|---|---|---|---|
| View preferences | an authenticated session | the user opens the preferences/settings panel | the general settings categories will be visible |
| Blank capture fallback | the preferences workflow is known to produce blank captures | the capture produces a >90% white frame | the pipeline will fall back to a textual description |
| Change password | the user is in the password change settings | the user enters the current and new passwords | the password will be updated |
| Blank capture handling | the password-change workflow is known to produce blank captures | the capture produces a blank WebP | the image reference will be removed from the documentation |
| Enable vacation reply | the vacation settings page is open | the user enables auto-reply and enters a message | the vacation reply will be activated |
| Blank capture handling | the vacation workflow is known to produce blank captures | the capture produces a blank WebP | the image reference will be removed from the documentation |
| Search across modules | an authenticated session | the user enters a search query in the global search bar | results from mail, calendar, and contacts will be displayed |
## Barrierefreiheit

### Tastaturnavigation

Diese Anwendung unterstützt die Tastaturnavigation. Keine Maus erforderlich.

| Aktion | Tastenkombination | Hinweise |
|--------|-------------------|----------|
| Module navigieren | `Tab` / `Umschalt+Tab` | Wechselt zwischen Bereichen |
| Auswählen/Aktivieren | `Eingabetaste` oder `Leertaste` | Link oder Schaltfläche aktivieren |
| Abbrechen/Schließen | `Escape` | Aktuelle Aktion abbrechen |
| Listen navigieren | `Pfeiltasten` | Durch Einträge bewegen |

**Reihenfolge der Screenreader-Navigation:**
1. Modul-Navigation → `Tab` zum Betreten
2. Modulinhalte → `Pfeiltasten` zum Navigieren
3. Aktionsschaltflächen → `Leertaste` oder `Eingabetaste` zum Aktivieren
4. Formulare → `Tab` zwischen Feldern, Pfeiltasten für Dropdowns

### Hochkontrastmodus

SOGo unterstützt den Hochkontrast- und Dunkelmodus. Aktivierung über Benutzereinstellungen oder systemweite Barrierefreiheitseinstellungen:
- **Windows:** `Win+Strg+C` schaltet den Hochkontrast um
- **macOS:** Systemeinstellungen → Bedienungshilfen → Anzeige → Kontrast erhöhen
- **Browser-Erweiterungen:** Dark Reader, High Contrast (Chrome)
