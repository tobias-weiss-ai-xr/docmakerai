---
title: "Aufgaben / To-Do-Modul"
description: "Aufgabenlisten in SOGo 6 erstellen und verwalten"
sidebar_label: "Aufgaben / To-Do"
---

# Aufgaben / To-Do-Modul

Organisieren Sie Aufgaben, setzen Sie Prioritäten und verwalten Sie To-Do-Artikel im Aufgabenverwaltungsmodul von SOGo 6.

:::info
In vielen SOGo-Installationen erscheint das Aufgabenmodul nur, wenn `SOGoDocumentsEnabled` in der Serverkonfiguration auf `YES` gesetzt ist. Ihr Administrator muss möglicherweise auch das Aufgabenmodul über zusätzliche Servereinstellungen aktivieren.
:::

## Voraussetzungen

- Ein SOGo 6-Konto mit gültigen Anmeldedaten
- Aufgabenmodul in der SOGo-Konfiguration aktiviert
- Sie sind bei SOGo 6 angemeldet

## Funktionsübersicht

| Funktion | Beschreibung |
|----------|-------------|
| **Aufgabenlisten** | Mehrere Aufgabenkategorien erstellen (z. B. persönlich, Arbeit, Projekte) |
| **Prioritätsstufen** | Markierungen für Dringend, Hoch, Mittel, Niedrig |
| **Fälligkeitsdaten** | Fristen und Erinnerungen festlegen |
| **Statusverfolgung** | Ausstehend, In Bearbeitung, Abgeschlossen, Zurückgestellt |
| **Integration** | Aufgaben mit Ereignissen, Kontakten verknüpfen |

## Schritt-für-Schritt-Anleitung

### Schritt 1: Aufgabenmodul öffnen

Klicken Sie in der Navigationsseitenleiste auf **Aufgaben** oder **To-Do**, um das Modul zu öffnen.

:::tip
Wenn Aufgaben nicht in der Navigationsleiste erscheinen, kontaktieren Sie Ihren Administrator, um es über die `SOGoDocumentsEnabled`-Konfiguration zu aktivieren und SOGo neu zu starten.
:::

### Schritt 2: Neue Aufgabe erstellen

#### Option A: Schnellerfassung
1. Klicken Sie auf die Schaltfläche **+ Aufgabe** (oben im Aufgabenbereich)
2. Geben Sie einen Aufgabentitel ein
3. Drücken Sie die Eingabetaste oder klicken Sie außerhalb des Eingabefelds, um zu speichern

#### Option B: Detaillierte Erfassung
1. Klicken Sie auf **Neue Aufgabe** oder **Aufgabe erstellen**
2. Füllen Sie die Aufgabendetails aus:
   - Titel
   - Beschreibung
   - Priorität
   - Fälligkeitsdatum
   - Zugehöriges Projekt oder Liste

### Schritt 3: Aufgabendetails bearbeiten

Klicken Sie nach der Erstellung auf die Aufgabe, um die Detailansicht zu öffnen und zu ändern:

| Eingabefeld | Beschreibung |
|------|-------------|
| **Titel** | Kurzer Aufgabenname |
| **Beschreibung** | Detaillierte Notizen zur Aufgabe |
| **Fälligkeitsdatum** | Bis wann die Aufgabe abgeschlossen sein muss |
| **Priorität** | Dringend, Hoch, Normal, Niedrig |
| **Status** | Ausstehend, In Bearbeitung, Abgeschlossen, Zurückgestellt |
| **Erledigt** | Kontrollkästchen zum Markieren als erledigt |
| **Fortschritt in %** | Schieberegler zur Fortschrittsverfolgung |
| **Kategorie / Liste** | Wählen Sie, welcher Aufgabenliste zugeordnet werden soll |

### Schritt 4: Aufgaben nach Listen organisieren

Aufgabenkategorien erstellen oder auswählen:

1. Klicken Sie auf das Symbol **Listen** oder **Kategorien** in der Symbolleiste
2. Klicken Sie auf **Neue Liste**
3. Benennen Sie die Liste (z. B. „Arbeit", „Persönlich", „Projekt X")
4. Klicken Sie auf **Speichern**

Ziehen Sie Aufgaben, um sie innerhalb von Listen neu anzuordnen.

### Schritt 5: Erinnerungen einstellen

Für wichtige Aufgaben:

1. Klicken Sie auf die Aufgabe, um Details zu öffnen
2. Klicken Sie auf **Erinnerung hinzufügen**
3. Geben Sie den Zeitpunkt an:
   - **Am Fälligkeitsdatum** — zur genauen Fälligkeitszeit
   - **Minuten vorher** — Vorabbenachrichtigung
   - **Tage vorher** — für längere Erinnerungen

:::note
Die Erinnerungsverwaltung nutzt die E-Mail- und Benachrichtigungsinfrastruktur von SOGo. Stellen Sie sicher, dass Ihre E-Mail korrekt konfiguriert ist, um Aufgabenerinnerungen zu erhalten.
:::

## Ansichten und Sortierung

| Ansicht | Verwendungszweck |
|---------|-----------------|
| **Alle Aufgaben** | Übersicht über alle ausstehenden Aufgaben |
| **Fällig bald** | Fokus auf anstehende Fristen |
| **Priorität** | Sortieren nach Dringlichkeit, dann nach Fälligkeitsdatum |
| **Kategorie** | Nach Liste/Projekt filtern |
| **Erledigt** | Abgeschlossene Aufgaben überprüfen |

## Tastenkombinationen

| Aktion | Tastenkombination |
|--------|------------------|
| Neue Aufgabe | `Strg + N` / `⌘ + N` |
| Aufgabe erledigen | Häkchen neben dem Element oder `Strg + Eingabetaste` |
| Aufgabe löschen | `Entf`-Taste |
| Erledigt rückgängig | `Strg + Z` / `⌘ + Z` |

## Aufgabenintegration

SOGo-Aufgaben können verknüpft werden mit:

| Integration | Vorgehen |
|-------------|---------|
| **Kalender** | Eine Ereigniseinladung in eine Aufgabe umwandeln; Aufgabendatum auf Ereignisdatum setzen |
| **Kontakte** | Besitzer oder Delegierten aus dem Adressbuch zuweisen |
| **E-Mail** | Aufgabe aus E-Mail-Inhalt erstellen (an Aufgabenliste weiterleiten) |

:::tip
Verwenden Sie Aufgaben, um Besprechungsaktionen nachzuverfolgen. Erstellen Sie nach einer Besprechung Aufgaben für Ergebnisse oder nächste Schritte.
:::

## Best Practices

1. **Verwenden Sie klare, spezifische Titel:** „Sarah anrufen" ist besser als „Telefon", da es erklärt, wen und was es betrifft.
2. **Setzen Sie realistische Fälligkeitsdaten:** Vermeiden Sie Überlastung bei der Terminplanung.
3. **Regelmäßig überprüfen:** Planen Sie wöchentlich Zeit ein, um Aufgaben zu überprüfen und zu aktualisieren.
4. **Erledigte Aufgaben löschen:** Halten Sie die Aufgabenliste sauber. Archivieren Sie statt zu löschen, falls Sie den Verlauf benötigen.
5. **Delegate bei Bedarf:** Wenn jemand anderes sich darum kümmern sollte, erwähnen Sie es in der Beschreibung oder erstellen Sie eine Aufgabe für diese Person.

## Fehlerbehebung

| Problem | Mögliche Ursache | Lösung |
|---------|-----------------|--------|
| Aufgabenmodul nicht sichtbar | `SOGoDocumentsEnabled` auf NO gesetzt | Bitten Sie den Admin, es in der SOGo-Konfiguration zu aktivieren |
| Aufgabe kann nicht erstellt werden | Schreibberechtigung für Aufgabenliste fehlt | Überprüfen Sie die ACLs für die Aufgabenliste |
| Aufgabenerinnerungen kommen nicht an | E-Mail nicht konfiguriert oder Aufgaben deaktiviert | Überprüfen Sie, ob die Mailserver-Einstellungen korrekt sind |
| Aufgabenliste wird nicht synchronisiert | Netzwerkproblem oder Serverproblem | Aktualisieren Sie die Seite oder melden Sie sich erneut an |
| Priorität oder Fälligkeitsdatum kann nicht geändert werden | Aufgabe durch externes System gesperrt (z. B. mobile App) | Schließen Sie die aktuelle Änderung ab und versuchen Sie es nach einem Synchronisationszyklus erneut |

## Fazit

Sie haben erfolgreich gelernt, wie Sie Aufgaben im SOGo 6-Aufgabenmodul erstellen und verwalten.
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
