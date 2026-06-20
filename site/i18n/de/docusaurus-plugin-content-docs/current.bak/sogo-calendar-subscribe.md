---
title: "iCal-Feed abonnieren"
description: "Externe Kalender (Feiertage, Teamkalender) in SOGo 5 importieren"
sidebar_label: "iCal-Feed abonnieren"
---

# iCal-Feed abonnieren

Importieren Sie externe Kalender in Ihren SOGo 5-Kalender — öffentliche Feiertage,
Teamkalender oder jeden online verfügbaren `.ics`-Feed.

## Voraussetzungen

- Ein SOGo 5-Konto mit gültigen Anmeldedaten
- Sie sind bei SOGo 5 angemeldet
- Eine URL zu einem iCal-Feed (`.ics`-Datei oder CalDAV-Endpunkt)

## Schritt-für-Schritt-Anleitung

### Schritt 1: iCal-Feed-URL finden

Sie benötigen die Webadresse (URL) eines iCal-Feeds. Häufige Beispiele:

| Quelle | Beispiel-URL |
|--------|-------------|
| Öffentliche Feiertage | `https://calendar.google.com/calendar/ical/.../basic.ics` |
| Team-Kalender | `https://teamup.com/.../events.ics` |
| Freigegebener SOGo 5-Kalender | `https://sogo.example.com/SOGo/dav/benutzername/calendar/shared/` |

### Schritt 2: Kalendereinstellungen öffnen

1. Klicken Sie in der Seitenleiste auf **Kalender**
2. Suchen Sie die Kalenderliste auf der linken Seite
3. Klicken Sie auf das **Zahnradsymbol** ⚙ neben der Kalenderbereichsüberschrift
4. Wählen Sie **URL abonnieren**

![Kalenderansicht mit Abonnementoptionen](./assets/01-calendar-view.png)

### Schritt 3: Feed-URL eingeben

Im Abonnement-Dialog:

1. **URL:** Fügen Sie die iCal-Feed-URL ein
2. **Name:** Geben Sie einen Anzeigenamen ein (z. B. "Deutsche Feiertage")
3. **Farbe:** Wählen Sie eine Kalenderfarbe zur besseren Sichtbarkeit

### Schritt 4: Sync-Optionen konfigurieren

| Option | Beschreibung |
|--------|-------------|
| **Aktualisierungsintervall** | Wie oft auf Updates geprüft wird (stündlich, täglich usw.) |
| **Erinnerungen entfernen** | Alarminformationen aus externen Ereignissen entfernen |
| **Anhänge entfernen** | Externe Dateianhänge nicht herunterladen |

Empfohlene Voreinstellungen: Aktualisierung **täglich**, Erinnerungen entfernen (externe
Kalender haben oft irrelevante Alarme).

### Schritt 5: Abonnement speichern

Klicken Sie auf **Abonnieren** oder **OK**. Der Kalender erscheint in Ihrer
Kalenderliste mit einem Abonnementsymbol 📡.

## Abonnements verwalten

### Abonnierte Ereignisse anzeigen

Abonnierte Kalender funktionieren wie Ihre eigenen — Ereignisse werden in der
Kalenderansicht angezeigt. Sie können die Sichtbarkeit durch Aktivieren/Deaktivieren
des Kalenders in der Liste umschalten.

### Manuell aktualisieren

Klicken Sie mit der rechten Maustaste auf den abonnierten Kalender → **Aktualisieren**,
um die neuesten Daten sofort abzurufen.

### Abonnement-Eigenschaften bearbeiten

Rechtsklick auf den Kalender → **Eigenschaften**:
- Anzeigenamen oder Farbe ändern
- Feed-URL aktualisieren
- Aktualisierungsintervall anpassen

### Abonnement kündigen

Rechtsklick auf den Kalender → **Abonnement kündigen** oder **Löschen**.
Der Kalender wird aus Ihrer Ansicht entfernt. Die Quelle bleibt unverändert.

## Fehlerbehebung

### "Ungültige Kalender-URL"

- Überprüfen Sie, ob die URL erreichbar ist (versuchen Sie, sie im Browser zu öffnen)
- Die URL muss gültige iCalendar-Daten (`.ics`) zurückgeben
- Einige öffentliche Feeds erfordern eine Authentifizierung

### Kalender wird nicht aktualisiert

- Überprüfen Sie die Einstellung des Aktualisierungsintervalls
- Manuell aktualisieren: Rechtsklick → **Aktualisieren**
- Der Feed-Anbieter hat möglicherweise die URL geändert

### Ereignisse haben falsche Uhrzeiten

- SOGo 5 konvertiert alle Daten in Ihre konfigurierte Zeitzone
- Überprüfen Sie Ihre Zeitzone unter **Einstellungen** → **Allgemein** → **Zeitzone**
- Einige iCal-Feeds enthalten keine Zeitzoneninformationen — diese werden standardmäßig auf UTC gesetzt

## Fazit

iCal-Abonnements ermöglichen es Ihnen, externe Kalender in Ihre
SOGo 5-Ansicht einzublenden — perfekt für öffentliche Feiertage, Teamtermine und
Kalenderfeeds von Drittanbietern.
