---
title: "Kalender freigeben"
description: "Ihren SOGo 5-Kalender mit Kollegen teilen und Berechtigungen festlegen"
sidebar_label: "Kalender freigeben"
---

# Kalender freigeben

Dieses Tutorial erklärt, wie Sie Ihren SOGo 5-Kalender für andere Benutzer freigeben
und steuern, was diese sehen oder tun können.

## Voraussetzungen

- Ein SOGo 5-Konto mit gültigen Anmeldedaten
- Sie sind bei SOGo 5 angemeldet
- Sie haben mindestens einen Kalender (Ihr Standardkalender trägt das Account-Kürzel, das das Hochschulrechenzentrum individuell vergibt)

## Schritt-für-Schritt-Anleitung

### Schritt 1: Freigaben-Dialog öffnen

1. Klicken Sie oben in der Navigationsleiste auf **Kalender**
2. Klicken Sie in der Kalenderliste auf das **Dreipunkt-Menü** (⋯) neben dem Kalender, den Sie freigeben möchten
3. Wählen Sie **Freigaben…**

Hinweis: Ihr Standardkalender trägt nicht den Namen „Persönlich", sondern das
Account-Kürzel, das das Hochschulrechenzentrum individuell vergibt.

### Schritt 2: Person eintragen

Im Freigaben-Dialog geben Sie direkt die Person ein, die die Freigabe erhalten soll:

1. Beginnen Sie mit der Eingabe des Namens oder der E-Mail-Adresse der Person
2. Wählen Sie sie aus der automatischen Vervollständigungsliste aus

### Schritt 3: Berechtigung festlegen

Wählen Sie für die eingetragene Person die gewünschte Berechtigung — von reinem
Ansehen bis zur Bearbeitungsberechtigung. Für die Zusammenarbeit in einem Team
genügt in der Regel eine Berechtigung, die das Anzeigen sowie das Erstellen und
Bearbeiten von Ereignissen erlaubt.

### Schritt 4: Freigabe bestätigen

Speichern Sie die Freigabe. Die Person kann nun auf Ihren Kalender entsprechend
der festgelegten Berechtigung zugreifen.

### Schritt 5: Überprüfen (Optional)

Um zu überprüfen, ob die Freigabe funktioniert:

1. Öffnen Sie ein **privates/Inkognito-Browserfenster**
2. Melden Sie sich als der Benutzer an, mit dem Sie geteilt haben
3. Öffnen Sie das Kalendermodul
4. Prüfen Sie, ob Ihr freigegebener Kalender in dessen Kalenderliste erscheint

## Freigabe über CalDAV (Erweitert)

Wenn Sie einen CalDAV-Client verwenden (Thunderbird, macOS-Kalender, iOS):

1. Öffnen Sie Ihren CalDAV-Client
2. Fügen Sie einen neuen Kalender mit der URL hinzu:
   ```
   https://ihre-sogo-instanz/SOGo/dav/ihr-benutzername/calendar/personal/
   ```
3. Geben Sie Ihre SOGo 5-Anmeldedaten ein
4. Der Kalender wird automatisch synchronisiert

Freigegebene Kalender erscheinen unter demselben CalDAV-Endpunkt für Benutzer,
die Zugriff erhalten haben.

## Freigabe entfernen oder ändern

Öffnen Sie erneut das **Dreipunkt-Menü** (⋯) neben dem Kalender und wählen Sie **Freigaben…**:

- **Ändern:** Passen Sie die Berechtigung der Person an
- **Entfernen:** Entfernen Sie den Eintrag der Person aus der Freigabeliste
- Speichern Sie anschließend die Änderung

## Fazit

Sie haben Ihren Kalender erfolgreich freigegeben. Freigegebene Kalender sind eine nützliche
Möglichkeit, Teamtermine zu koordinieren, Besprechungen zu planen und alle
auf dem gleichen Stand zu halten.
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

**Kalender freigeben: Kollegen mit Bearbeitungsberechtigung hinzufügen**

**Schritt 1: Kalendermodul öffnen**
- `Tab` zum Kalender-Modul, dann `Eingabetaste`
- Sie hören: „Kalender, Modul-Überschrift“

**Schritt 2: Freigaben-Dialog öffnen**
- `Tab` durch die Kalenderliste
- Pfeiltasten (auf/ab) zum gewünschten Kalender
- `Tab` zum **Dreipunkt-Menü** (⋯) daneben, `Eingabetaste` zum Öffnen
- Pfeiltasten zu **Freigaben…**, `Eingabetaste`

**Schritt 3: Person eintragen**
- `Tab` zum Eingabefeld
- Beginnen Sie, den Namen oder die E-Mail-Adresse des Kollegen einzutippen
- Sie hören: „Bearbeiten, AutoVervollständigung, Vorschläge verfügbar“
- Pfeil nach unten durch die Vorschläge, `Eingabetaste` zur Auswahl

**Schritt 4: Berechtigung festlegen**
- `Tab` zum Berechtigungsfeld
- Wählen Sie „Nur ansehen“ oder Bearbeitungsberechtigung für die Person
- Sie hören die gewählte Option

**Schritt 5: Bestätigen und speichern**
- `Tab` zur Schaltfläche **Speichern**
- `Eingabetaste` zum Übernehmen der Freigabe
- Sie hören: „Erfolgreich gespeichert“ oder eine ähnliche Bestätigung

**Schritt 6: Überprüfen (Optional)**
- Öffnen Sie ein privates/Inkognito-Browserfenster
- Melden Sie sich als der freigegebene Benutzer an
- Öffnen Sie das Kalendermodul
- Der freigegebene Kalender erscheint in dessen Liste mit Ihrem Namen

**Häufige Screenreader-Ansagen:**

| Ansage | Bedeutung | Aktion |
|--------|-----------|--------|
| „Kalender, Modul-Überschrift“ | Kalenderliste geladen | Zur Freigabe-Dialognavigation beginnen |
| „Freigaben…, Menüpunkt“ | Freigaben-Dialog öffnet sich | Person eintragen |
| „Bearbeiten, AutoVervollständigung, Vorschläge verfügbar“ | Personensuchfeld aktiv | Kollegenname eingeben und aus Liste wählen |
| „Ändern, ausgewählt“ | Berechtigungsstufe gesetzt | Stufe bestätigen oder ändern |
| „Erfolgreich gespeichert“ | Freigabe übernommen | Freigabe ist aktiv – die Person informieren |
| „Benutzer hat bereits Zugriff“ | Doppelte Freigabe | Berechtigungsstufe ändern oder entfernen und neu hinzufügen |
| „Ungültiger Benutzer“ | Person in SOGo nicht gefunden | Schreibweise oder vollständige E-Mail-Adresse prüfen |

### Hochkontrastmodus

SOGo unterstützt den Hochkontrast- und Dunkelmodus. Aktivierung über Benutzereinstellungen oder systemweite Barrierefreiheitseinstellungen:
- **Windows:** `Win+Strg+C` schaltet den Hochkontrast um
- **macOS:** Systemeinstellungen → Bedienungshilfen → Anzeige → Kontrast erhöhen
- **Browser-Erweiterungen:** Dark Reader, High Contrast (Chrome)

- **Orientierung:** verlieren Sie Ihren Platz, drücken Sie `Strg+Pos1`, um zum
  Seitenanfang zurückzukehren und von dort weiterzunavigieren.
