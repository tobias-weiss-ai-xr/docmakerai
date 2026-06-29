---
title: "Ressourcenbuchung (Räume, Ausrüstung)"
description: "Gemeinsam genutzte Ressourcen wie Besprechungsräume und Ausrüstung buchen"
sidebar_label: "Ressourcenbuchung"
---

# Ressourcenbuchung

Reservieren und planen Sie gemeinsam genutzte Ressourcen — Besprechungsräume, Projektoren, Labore oder Ausrüstung — über die integrierte Kalender-Ressourcenbuchung von SOGo.

:::info
Die Ressourcenbuchung in SOGo wird typischerweise als spezielle Kalenderkonten implementiert, die als Ressourcen markiert sind. Ihr Administrator konfiguriert diese Ressourcenkonten, und sie erscheinen als verfügbare Räume oder Ausrüstung bei der Planung von Besprechungen.
:::

## Voraussetzungen

- Ein SOGo 5-Konto mit gültigen Anmeldedaten
- Sie sind bei SOGo 5 angemeldet
- Ressourcenkonten vom Administrator konfiguriert
- Zugriff auf das Kalendermodul

## Übersicht über die Ressourcenbuchung

| Ressourcentyp: Description | Beispiel-Anwendungsfall |
|---------------|------------------------|
| **Besprechungsraum** | Kleiner Team-Besprechungsraum, Konferenzraum, Veranstaltungssaal |
| **Ausrüstung** | Projektor, Videokonferenzsystem, spezielle Laborausrüstung |
| **Fahrzeug** | Firmenwagen, Servicefahrzeug |
| **Sonstiges** | Trainingsarbeitsplatz, Demo-Umgebung |

## Schritt-für-Schritt-Anleitung

### Schritt 1: Kalender öffnen

Klicken Sie in der Navigationsseitenleiste auf **Kalender**.

### Schritt 2: Neues Ereignis erstellen

1. Klicken Sie auf die **+** (Plus)-Schaltfläche
2. Oder doppelklicken Sie auf einen Zeitraum im Kalenderraster

### Schritt 3: Teilnehmer hinzufügen

Im Ereignisdialog:

1. Erweitern oder klicken Sie auf **Teilnehmer**
2. Suchen Sie nach Ihren Kollegen oder wählen Sie sie aus (zu Benachrichtigungszwecken)
3. Suchen und fügen Sie die **Ressource** hinzu — diese kann erscheinen als:
   - Ein spezieller Ressourcen-Tab oder ein Ressourcensymbol
   - Eine Liste von Räumen/Ausrüstung, die Sie auswählen können
   - Ein Auto-Vervollständigungsvorschlag bei Eingabe des Ressourcennamens

:::tip
Ressourcen erscheinen oft mit einem Ortsymbol (📍) oder sind als [Raum] oder Ausrüstungsname in der Auto-Vervollständigung gekennzeichnet.
:::

### Schritt 4: Zeitfenster auswählen

Wählen Sie Datum/Uhrzeit für die Buchung. SOGo zeigt die Ressourcenverfügbarkeit an:

| Visueller Hinweis: Description | Bedeutung |
|-------------------|-----------|
| **Grün/markiert** | Ressource verfügbar (buchbar) |
| **Abgegraut** | Bereits gebucht (Konflikt) |
| **Teilweise verfügbar** | Teilweise Verfügbarkeit (Ressource teilweise genutzt) |

### Schritt 5: Buchung bestätigen

1. Fügen Sie Ereignistitel und Details hinzu
2. Bestätigen Sie, dass die Ressource in den Teilnehmern aufgeführt ist
3. Klicken Sie auf **Speichern** oder **Erstellen**

SOGo prüft auf Konflikte:
- **Kein Konflikt:** Ressource gebucht, Teilnehmer benachrichtigt
- **Konflikt vorhanden:** SOGo kann:
  - Konflikt anzeigen, Buchung verhindern
  - Buchung zulassen, aber Warnung anzeigen

### Schritt 6: Ressourcenverfügbarkeit anzeigen

Optional, um den Zeitplan einer Ressource anzuzeigen:

1. Suchen Sie im Kalender den Bereich **Ressourcen** oder die Navigation
2. Klicken Sie auf die Ressource (z. B. „Konferenzraum A")
3. Zeigen Sie den Kalender der Ressource in einem separaten Tab an

:::info
Einige Konfigurationen erlauben es, mehrere Ressourcen zu überlagern, um gemeinsame Verfügbarkeit zu finden.
:::

## Ressourcenkonfiguration (Administrator)

Ressourcenkonten werden typischerweise mit diesen Attributen erstellt:

| Einstellung: Description | Wert |
|-------------|------|
| **Benutzerrolle** | Ressource (keine Person) |
| **Standort** | Physische Adresse oder Raumnummer |
| **Kapazität** | Anzahl der Personen, die untergebracht werden können |
| **Ausrüstungsliste** | Spezifische Ausrüstung, die in der Ressource verfügbar ist |

:::note
Die Einrichtung von Ressourcen erfordert Administratorzugriff auf SOGo-Automatisierungsskripte oder direkte Datenbankbearbeitungen. Fragen Sie Ihren Admin, wenn eine benötigte Ressource nicht verfügbar ist.
:::

## Best Practices

1. **Buchen Sie im Voraus** — Ressourcen werden gemeinsam genutzt; Last-Minute-Buchungen können fehlschlagen.
2. **Geben Sie Details an** — Fügen Sie in der Ereignisbeschreibung den Besprechungszweck, benötigte Vorbereitungen und die Anzahl der Teilnehmer hinzu.
3. **Seien Sie rücksichtsvoll** — Wenn Sie nur wenige Minuten benötigen, blockieren Sie nicht unnötig einen ganzen Tag.
4. **Freigeben, wenn erledigt** — Wenn Sie früher fertig sind oder das Treffen ausfällt, entfernen Sie das Ereignis/die Buchung.
5. **Vermeiden Sie Doppelbuchungen** — Das Ressourcensystem prüft Konflikte für Sie, aber seien Sie umsichtig.

## Buchungen verwalten

| Aktion: Description | Vorgehen |
|--------|---------|
| **Buchung ändern** | Ereignis im Kalender finden, Start-/Endzeit bearbeiten oder Teilnehmer aktualisieren, speichern |
| **Buchung stornieren** | Ereignis löschen (wenn Sie der Ereignisbesitzer sind) |
| **Verfügbarkeit prüfen** | Ressourcenkalender direkt anzeigen; alle Buchungen sehen |
| **Konflikte lösen** | Wenn Konfliktwarnung erscheint, alternative Zeit wählen |

## Berechtigungen und Delegation

- Nur Benutzer mit Berechtigung zur Ressourcenplanung können buchen
- Ein Administrator kann einschränken, wer bestimmte stark nachgefragte Ressourcen buchen darf
- Einige Ressourcen akzeptieren Buchungen automatisch, andere erfordern Bestätigung durch den Ressourcenverwalter

## Fehlerbehebung

| Problem: Description | Mögliche Ursache | Lösung |
|---------|-----------------|--------|
| Ressource in Teilnehmern nicht gefunden | Ressource außerhalb von Kalendern nicht konfiguriert | Bitten Sie den Admin, die Ressource buchbar zu machen; stellen Sie sicher, dass sie als freigebbarer Kalender aufgeführt ist |
| Buchung schlägt mit Konflikt fehl | Zeitfenster bereits gebucht | Wählen Sie ein anderes Zeitfenster mit verfügbarer Ressource |
| Ressource erscheint nicht als Kategorie | Nur für bestimmte Gruppen konfiguriert | Fragen Sie beim Admin nach, ob Sie Berechtigung zum Buchen dieser Ressource haben |
| Ressourcenkalender kann nicht angezeigt werden | Berechtigungen schränken Lesezugriff ein | Kontaktieren Sie den Admin für Ansichtsberechtigungen |

## Integration mit anderen Funktionen

| Integration: Description | Hinweise |
|-------------|---------|
| **Belegt/Frei** | Belegte Zeiten der Ressource werden in Belegt/Frei-Abfragen angezeigt |
| **Kalenderfreigabe** | Teilen Sie Ihren Kalender mit dem Ressourcenteam zur Koordination der Terminplanung |
| **E-Mail-Benachrichtigungen** | Teilnehmer und Ressourcenverwalter können Buchungsbestätigungen erhalten |

:::info
In größeren Organisationen kann die Ressourcenbuchung zusätzliche Planungstools oder Connector-Integrationen erfordern. Dies deckt das Kern-SOGo-Szenario ab, in dem Ressourcen als spezielle Kalender modelliert werden.
:::

## Fazit

Sie haben erfolgreich gelernt, wie Sie Ressourcen in SOGo 5 buchen.
## Accessibility

### Keyboard Navigation

This application supports keyboard navigation. No mouse required for completing this task.

| Action | Keyboard Shortcut: What key to press | Notes: Additional information |
|--------|--------------------------------------|------------------------------|
| | Navigate modules | `Tab` / `Shift+Tab` | Cycles through sections |
| | Select/activate | `Enter` or `Space` | Activate button or link |
| | Cancel/close | `Escape` | Cancel current action |
| | Navigate lists | `Arrow keys` | Move through items |

**Screen Reader Navigation Order:**
1. Sidebar navigation → `Tab` to enter
2. Module content → `Arrow keys` to navigate
3. Action buttons → `Space` or `Enter` to activate
4. Forms → `Tab` between fields, arrows for dropdowns

### High Contrast Mode

SOGo supports high contrast and dark mode. Toggle via user preferences or use browser/OS-level accessibility settings:
- **Windows:** `Win+Ctrl+C` toggles high contrast
- **macOS:** System Preferences → Accessibility → Display → Increase contrast
- **Browser Extensions:** Dark Reader, High Contrast (Chrome)

