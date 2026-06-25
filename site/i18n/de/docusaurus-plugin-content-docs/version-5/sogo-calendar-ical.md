---
title: "Kalender — Import & Export (iCal)"
description: "Kalender mit dem iCal-Format (.ics) in SOGo 5 importieren und exportieren"
sidebar_label: "Import & Export (iCal)"
---

# Kalender — Import & Export (iCal)

Teilen Sie Ihren Kalender mit anderen, indem Sie ihn als iCal-Datei exportieren, oder importieren Sie Kalender aus anderen Anwendungen in SOGo.

## Voraussetzungen

- Ein SOGo 5-Konto mit gültigen Anmeldedaten
- Sie sind bei SOGo 5 angemeldet

## Schritt-für-Schritt-Anleitung

### Schritt 1: Kalendermodul öffnen

Klicken Sie in der linken Seitenleiste auf **Kalender**, um die Kalenderansicht zu öffnen.

### Schritt 2: Kalendereinstellungen aufrufen

Klicken Sie auf das **Einstellungen**-Zahnradsymbol in der Kalender-Symbolleiste.

### Schritt 3: Kalender exportieren

Das Kalendereinstellungsfeld zeigt Exportoptionen an:

1. Suchen Sie den Abschnitt **Export** oder **Teilen**
2. Klicken Sie auf den Download-Link oder kopieren Sie die Kalender-URL
3. Der Kalender wird als `.ics`-Datei (iCal) exportiert

### Schritt 4: Kalender importieren

1. Klicken Sie auf die Schaltfläche **Import** in den Kalendereinstellungen
2. Wählen Sie die `.ics`-Datei aus, die Sie importieren möchten
3. Wählen Sie den Zielkalender für den Import
4. Klicken Sie auf **Importieren**, um zu beginnen

:::info
iCal (`.ics`) ist ein Standard-Kalenderdateiformat, das von den meisten Kalenderanwendungen unterstützt wird, einschließlich Google Kalender, Microsoft Outlook und Apple Kalender.
:::

## Importoptionen

| Option | Beschreibung | Verwenden wenn |
|--------|-------------|---------------|
| **Alle Ereignisse hinzufügen** | Importiert alle Ereignisse aus der Datei | Erster Import |
| **Duplikate zusammenführen** | Überspringt Ereignisse mit gleichem Datum und Titel | Vorhandenen Kalender aktualisieren |
| **Vorhandene aktualisieren** | Ersetzt Ereignisse mit übereinstimmenden Zeiten | Freigegebenen Kalender aktualisieren |

:::warning
Der Import eines Kalenders mit Hunderten von Ereignissen kann mehrere Minuten dauern. Schließen Sie die Seite nicht, während der Import läuft.
:::

## Freigabe über iCal

Sie können Ihren Kalender teilen, indem Sie die iCal-URL bereitstellen:

1. Kopieren Sie die **Kalender-URL** aus den Export-Einstellungen
2. Teilen Sie die URL mit anderen
3. Diese können Ihren Kalender in ihrer eigenen Anwendung abonnieren

## Fehlerbehebung

| Problem | Mögliche Ursache | Lösung |
|---------|-----------------|--------|
| Import-Button nicht sichtbar | Kalenderfreigabe nicht aktiviert | Kontaktieren Sie Ihren Administrator, um die Freigabe zu aktivieren |
| Import schlägt fehl | Ungültiges `.ics`-Dateiformat | Überprüfen Sie, ob die Datei in einer Kalenderanwendung geöffnet werden kann |
| Exportdatei ist leer | Kalender hat keine Ereignisse | Fügen Sie vor dem Export Ereignisse zum Kalender hinzu |

## Fazit

Sie haben erfolgreich gelernt, wie Sie Kalender im iCal-Format in SOGo 5 importieren und exportieren.
