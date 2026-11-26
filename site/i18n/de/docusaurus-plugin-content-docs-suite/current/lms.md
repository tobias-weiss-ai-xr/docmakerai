---
title: "Lernplattform (ILIAS)"
sidebar_label: "Lernplattform (ILIAS)"
sidebar_position: 38
description: "Kurse und Lernmaterialien der Suite"
---
import PageSEO from '@site/src/components/PageSEO';

<PageSEO
  title="Lernplattform (ILIAS)"
  description="Kurse und Lernmaterialien der Suite"
  keywords={["Lernplattform", "ILIAS", "openEduSuite"]}
  suffix="openEduSuite"
  defaultKeywords={["Hochschule", "Open Source"]}
/>


# Lernplattform (ILIAS)

Die openEduSuite betreibt eine eigene Lernplattform:
[ILIAS](https://lms.openedusuite.org) — die Fußzeile meldet
*powered by ILIAS (v9.23)*. Kurse, Lernmaterialien und Tests der
Suite leben hier. Die [Portal](/suite/portal)kachel
**Lernplattform (ILIAS)** und das Suite-Konto öffnen das
**Dashboard** direkt.

![ILIAS-Dashboard nach der Suite-Anmeldung](./assets/lms.png)

Die Suite-Instanz zeigt ihre Oberfläche auf Englisch; die
Beschriftungen unten stehen also so im Bildschirm.

## Dashboard

Das **Dashboard** (Seitentitel *Dashboard: ILIAS*) ist Ihr
persönlicher Schreibtisch nach der Suite-Anmeldung. Es stapelt
vier Blöcke:

- **Favourites** (Favoriten): Lernobjekte, die Sie angeheftet
  haben. Ein frisches Konto zeigt stattdessen einen Hinweis in
  zwei Schritten: das **Repository** öffnen, ein Lernobjekt
  wählen (zum Beispiel ein Lernmodul oder ein Forum) und im
  Actions-Menü *Add to favourites* wählen.
- **My Courses and Groups**: Ihre Kurse und Gruppen — bis Sie
  einem beigetreten sind, steht hier nur *You are currently not
  yet a member of a course or group*.
- **Tasks**: Ihre offenen Aufgaben, oder *There are no tasks for
  you*.
- **Calendar**: der aktuelle Monat, dazu ein Link **Subscribe**.

## Hauptmenü

Das Hauptmenü läuft den linken Bildschirmrand hinunter; das
**User Menu** mit Ihrem Avatar sitzt in der oberen rechten Ecke.

- **Dashboard** führt zurück zum oben beschriebenen Dashboard.
- **Personal Workspace** öffnet ein Panel mit *Tags*,
  *Calendar*, *Tasks*, *Portfolio*, *Personal and Shared
  Resources* und *Private Notes*.
- **Achievements** öffnet ein Panel mit *Badges*.
- **Communication** öffnet ein Panel mit *Contacts* und
  *Comments*.
- **User Menu** enthält *Profile and Privacy*, *Settings* und
  *Logout*.

Die Fußzeile endet mit den Links **Legal Notice** und
**Accessibility**.

Hinweis: Die Kachel **ILIAS** unter *UNIVERSITÄT* zeigt auf das
uni-weite ILIAS der Philipps-Universität (extern) — die
Suite-Instanz hier ist die eigene der openEduSuite, mit Ihrem
Suite-Konto.

Bleibt Ihnen der Dienst verschlossen, erreicht das
[Helpdesk](/suite/helpdesk-create-ticket) seine Betreiber.

## Barrierefreiheit

| Aktion | Taste |
|--------|-------|
| Durch Menüs und Inhalte bewegen | `Tab` |
| Fokussiertes Element öffnen | `Enter` |

- ILIAS ist eine klassische Webanwendung in Lesereihenfolge:
  Hauptmenü, Inhaltsbereich — `Tab` führt hindurch.
- Die Menü-Panels sind als Menüs ausgezeichnet
  (`role=menuitem`); ihre Einträge tauchen so auch in der
  Element-Navigation eines Screenreaders auf.
- `Strg+Pos1` bringt Sie zum Seitenanfang zurück.

- **Hochkontrast und Dunkelmodus:** Kontrast und dunkle Themes kommen vom
  Betriebssystem oder Browser — Windows `Win+Strg+C`, macOS „Kontrast erhöhen“
  oder eine Browser-Erweiterung wie Dark Reader. Bietet die App ein eigenes
  dunkles Theme, schalten Sie es in den Einstellungen; die oben beschriebene
  Bedienung gilt weiterhin.
