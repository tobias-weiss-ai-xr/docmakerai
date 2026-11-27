---
title: "E-Mail-Ordner und Filter"
description: "Organisieren Sie Ihren Posteingang mit Ordnern und automatischen E-Mail-Filtern"
sidebar_label: "E-Mail-Ordner und Filter"
---

import VideoFallback from '@site/src/components/VideoFallback';

# E-Mail-Ordner und Filter

Erfahren Sie, wie Sie Ihren Posteingang mit Ordnern und
automatischen Nachrichtenfiltern (Sieve-Skripte) organisiert halten.

## Teil 1: Ordner verwalten

### Schritt 1: E-Mail-Modul öffnen

Klicken Sie oben in der Navigationsleiste auf **E-Mail**. Ihre Ordner werden links aufgelistet:

- **Posteingang** — Empfangene Nachrichten
- **Gesendet** — Von Ihnen gesendete Nachrichten
- **Entwürfe** — Ungespeicherte Nachrichten
- **Papierkorb** — Gelöschte Nachrichten
- **Spam** — Junk-E-Mail (falls aktiviert)

### Schritt 2: Neuen Ordner erstellen

1. Klicken Sie auf das Dreipunkt-Menü (⋯) neben einen beliebigen Ordner (z. B. Posteingang)
2. Wählen Sie **Neuer Ordner** oder **Ordner hinzufügen**
3. Geben Sie einen Namen ein (z. B. "Projekte", "Kunden", "Archiv")
4. Klicken Sie auf **OK**

Alternativ klicken Sie auf das **+**-Symbol neben der Ordnerlisten-Überschrift.

### Schritt 3: Verschachtelte Unterordner erstellen

Für eine bessere Strukturierung erstellen Sie Unterordner:

1. Klicken Sie auf das Dreipunkt-Menü (⋯) neben einen von Ihnen erstellten Ordner
2. Wählen Sie **Neuer Unterordner**
3. Benennen Sie ihn (z. B. "Projekte/Aktiv", "Projekte/Abgeschlossen")

**Ergebnis:**
```
📁 Posteingang
📁 Gesendet
📁 Projekte
  📁 Aktiv
  📁 Abgeschlossen
📁 Kunden
```

### Schritt 4: Nachrichten in Ordner verschieben

**Drag & Drop:** Klicken Sie auf eine Nachricht und ziehen Sie sie auf einen Ordner
**Dreipunkt-Menü (⋯):** Dreipunkt-Menü (⋯) bei einer Nachricht → **In Ordner verschieben** → Ziel auswählen
**Tastatur:** Nachrichten auswählen, `V` drücken, dann Ordner wählen

### Schritt 5: Ordner umbenennen oder löschen

- **Umbenennen:** Dreipunkt-Menü (⋯) neben Ordner → **Umbenennen**
- **Löschen:** Dreipunkt-Menü (⋯) neben Ordner → **Löschen** (leert den Ordner zuvor)

:::warning
Das Löschen eines Ordners löscht auch alle darin enthaltenen Nachrichten.
Verschieben Sie wichtige Nachrichten vorher an einen anderen Ort.
:::

## Teil 2: Automatische Filter (Sieve)

SOGo 6 verwendet **Sieve**-Skripte für die serverseitige E-Mail-Filterung.
Filter werden beim Eintreffen von E-Mails ausgeführt — bevor Sie sie in Ihrem Posteingang sehen.

### Schritt 1: Filtereinstellungen öffnen

1. Klicken Sie auf das **Dreipunkt-Menü** (⋯) (Einstellungen) in der oberen Symbolleiste
2. Wählen Sie **E-Mail** → **Filter**

![E-Mail-Filtereinstellungen](./assets/mail-filters.png)

<VideoFallback
  srcMp4="/docmakerai/clips/mail-filters.mp4"
  poster="/docmakerai/clips/mail-filters.png"
  alt="Kurzclip: E-Mail-Filter mit Bedingung und Aktion in den SOGo-6-Einstellungen anlegen"
  width="640"
  height="400"
/>

### Schritt 2: Neuen Filter erstellen

Klicken Sie auf **Filter erstellen**.

### Schritt 3: Bedingungen festlegen

Legen Sie fest, wann der Filter angewendet werden soll:

| Bedingung | Beispiel |
|-----------|---------|
| **Von enthält** | `@example.com` → alle E-Mails von dieser Domain |
| **Betreff enthält** | `[Spam]` → potenziellen Spam markieren |
| **An enthält** | `team@firma.com` → Mailinglisten-Nachrichten |
| **Größer als** | `5M` → große Anhänge |

Sie können mehrere Bedingungen kombinieren:
- **Alle Bedingungen müssen zutreffen** (UND)
- **Jede Bedingung kann zutreffen** (ODER)

### Schritt 4: Aktionen festlegen

Wählen Sie, was passiert, wenn die Bedingungen erfüllt sind. Die genauen Bezeichnungen können je nach Version leicht variieren — typische Aktionen:

| Aktion | Anwendungsfall |
|--------|---------------|
| **In Ordner verschieben** | In den richtigen Ordner sortieren |
| **In Ordner kopieren** | Kopie im Posteingang behalten + in Ordner ablegen |
| **Weiterleiten an** | An eine andere Adresse senden |
| **Als gelesen markieren** | Newsletter automatisch archivieren |
| **Als markiert kennzeichnen** | Wichtige Absender hervorheben |
| **Verwerfen** | Spam löschen (mit Vorsicht verwenden) |
| **Mit Nachricht ablehnen** | Unerwünschte E-Mails mit eigener Nachricht zurückweisen |

**Wichtig:** Die Mails werden nur dann tatsächlich verschoben, wenn Sie als letzte Aktion **Beende die Filterverarbeitung** hinzufügen.

### Schritt 5: Filterpriorität festlegen

Filter werden von oben nach unten ausgeführt. Ziehen Sie Filter, um die Reihenfolge zu ändern.
Die Aktion des ersten zutreffenden Filters wird angewendet.

### Schritt 6: Filter speichern

Klicken Sie auf **Speichern** oder **Übernehmen**. Das Sieve-Skript wird kompiliert und
sofort auf dem Server aktiviert.

## Beispielfilter

### Beispiel 1: Arbeits-E-Mails sortieren

Ziel: Alle E-Mails von `@firma.com` in den Ordner „Arbeit" verschieben.

1. Legen Sie vorher den Ordner „Arbeit" an (Teil 1, Schritt 2)
2. Filtereinstellungen öffnen → **Filter erstellen**
3. Bedingung: **Von enthält** `@firma.com`
4. Aktion: **In Ordner verschieben** → Ordner „Arbeit" wählen
5. Letzte Aktion: **Beende die Filterverarbeitung**
6. Klicken Sie auf **Speichern**

### Beispiel 2: Dringende Nachrichten markieren

```
Bedingung: Betreff enthält "DRINGEND"
Aktion:    Als markiert kennzeichnen
```

### Beispiel 3: Newsletter archivieren

```
Bedingung: Von enthält "newsletter@"
Aktion:    In Ordner "Newsletter" verschieben
```

## Fehlerbehebung

### Filter funktionieren nicht

- Prüfen Sie, ob die letzte Aktion des Filters **Beende die Filterverarbeitung** ist (siehe Schritt 4)
- Testen Sie zuerst mit einem einfachen Filter (z. B. alle E-Mails von sich selbst verschieben)
- Ob Sieve aktiviert ist (`SOGoSieveScriptsEnabled = YES`), welche Sieve-Server-Adresse konfiguriert ist und ob die Server-Protokolle Sieve-Kompilierungsfehler zeigen, gehört zur Serverkonfiguration — das ist Aufgabe Ihrer IT-Administration. Fragen Sie im Zweifel Ihren Administrator.

### Ordner wird nicht angezeigt

- Melden Sie sich ab und wieder an
- Überprüfen Sie, ob der Ordner erstellt wurde (nicht versehentlich mit Schrägstrichen benannt)

## Fazit

Ordner und Filter helfen Ihnen, einen sauberen Posteingang ohne manuellen Aufwand zu erhalten.
Beginnen Sie mit 2–3 Filtern für Ihre häufigsten E-Mail-Muster.
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

### Screenreader-Workflow

**E-Mail-Ordner und Filter einrichten**

**Schritt 1: E-Mail-Modul öffnen**
1. `Tab` zur Modul-Navigation
2. Pfeiltasten zur Option **E-Mail**
3. `Eingabetaste`, um die E-Mail-Ansicht zu öffnen

**Schritt 2: Ordner erstellen**
1. `Tab` zum **Dreipunkt-Menü** (⋯) neben dem E-Mail-Konto
2. Menü mit `Eingabetaste` öffnen, dann **Neuer Ordner** oder **Ordner hinzufügen** wählen
3. Ordnernamen eingeben
4. `Eingabetaste` zum Anlegen

**Schritt 3: Filtereinstellungen öffnen**
1. `Tab` zum **Dreipunkt-Menü** (⋯) (Einstellungen) in der oberen Symbolleiste
2. Pfeiltasten zu **E-Mail** → **Filter**
3. `Eingabetaste`

**Schritt 4: Filter erstellen**
1. Fokus auf der Schaltfläche **Filter erstellen**, `Eingabetaste`
2. Filternamen eingeben
3. `Tab` zur Bedingungsauswahl
4. Bedingung wählen (z. B. „Von enthält“)
5. `Tab` zum Wertfeld, Wert eingeben
6. `Tab` zu den Aktionen, Aktion festlegen (z. B. „In Ordner verschieben“)
7. Falls gewünscht, als letzte Aktion **Beende die Filterverarbeitung** hinzufügen
8. `Tab` zur Schaltfläche **Speichern**, `Eingabetaste`

**Häufige Screenreader-Ansagen:**

| Ansage | Bedeutung | Aktion |
|--------|-----------|--------|
| „E-Mail, Baumansicht“ | E-Mail-Ordnerliste | Durch Ordner navigieren |
| „Neuer Ordner, Schaltfläche“ | Aktion zum Ordneranlegen | `Eingabetaste`, Namen eingeben |
| „Filter, Dialog“ | Filterverwaltung geöffnet | Neuen Filter erstellen |
| „Bedingung, Kombinationsfeld“ | Dropdown für Filterbedingung | Mit Pfeiltasten auswählen |
| „Aktion, Listenraster“ | Verfügbare Filteraktionen | Aktion mit Pfeiltasten wählen |
| „Filter gespeichert“ | Erfolg | Filter ist nun aktiv |

### Beschreibungen der visuellen Inhalte

**mail-filters.png:** Der statische Screenshot zeigt die E-Mail-Filtereinstellungen in SOGo 6, in denen Sie Filter mit Bedingungen und Aktionen anlegen.

**Screenreader-Alternative:** Wenn Sie dieses Bild nicht anzeigen können, verwenden Sie den Abschnitt **Screenreader-Workflow** weiter oben. Er bietet dieselben Informationen in Textform, die für Screenreader geeignet ist.

### Hochkontrastmodus

SOGo unterstützt den Hochkontrast- und Dunkelmodus. Aktivierung über Benutzereinstellungen oder systemweite Barrierefreiheitseinstellungen:
- **Windows:** `Win+Strg+C` schaltet den Hochkontrast um
- **macOS:** Systemeinstellungen → Bedienungshilfen → Anzeige → Kontrast erhöhen
- **Browser-Erweiterungen:** Dark Reader, High Contrast (Chrome)

- **Orientierung:** verlieren Sie Ihren Platz, drücken Sie `Strg+Pos1`, um zum
  Seitenanfang zurückzukehren und von dort weiterzunavigieren.
