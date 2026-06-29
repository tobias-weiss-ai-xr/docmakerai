---
title: "Delegation & Berechtigungen"
description: "Kalender und E-Mail-Ordner mit bestimmten Berechtigungen teilen"
sidebar_label: "Delegation & Berechtigungen"
---

# Delegation & Berechtigungen

Delegieren Sie Zugriff auf Ihre Kalender, E-Mail-Ordner und andere Ressourcen, indem Sie anderen Benutzern bestimmte Berechtigungen zuweisen.

## Voraussetzungen

- Ein SOGo 5-Konto mit gültigen Anmeldedaten
- Sie sind bei SOGo 5 angemeldet
- Mindestens zwei Benutzer mit SOGo-Konten (für die Delegationsdemonstration)
- Berechtigungen werden pro Ordner oder pro Kalender verwaltet

## Delegationsübersicht

SOGo unterstützt granulare ACL-basierte Berechtigungen für:

| Ressourcentyp: Description | Was geteilt werden kann |
|---------------|------------------------|
| **Kalender** | Schreibgeschützt, Vollzugriff, vertrauliche Verfügbarkeit |
| **Adressbuch** | Lese-, Schreib-, Änderungsberechtigungen |
| **E-Mail-Ordner** | Ansicht, Lesen, Senden, Erstellen, Löschen-Zugriff |
| **Kategorien** | Berechtigungsstufen für Ereigniskategorisierung |

## Berechtigungsstufen

| Berechtigung: Description | Beschreibung |
|-------------|-------------|
| **Besitzer** | Vollzugriff, kann Berechtigungen ändern |
| **Kann lesen** | Nur Elemente anzeigen |
| **Kann bearbeiten** | Vorhandene Elemente ändern |
| **Kann erstellen** | Neue Elemente hinzufügen |
| **Kann löschen** | Elemente entfernen |
| **Prüfer** | Kombination aus Lesen + Genehmigen/Ablehnen |

:::tip
Verwenden Sie verschiedene Berechtigungsstufen basierend auf der Vertrauensebene. Ein Kollege kann beispielsweise „Kann lesen"-Zugriff auf Ihren Kalender erhalten, während ein delegierter Assistent „Kann bearbeiten" plus „Kann erstellen" bekommen kann.
:::

## Schritt-für-Schritt-Anleitung

### Schritt 1: Ressourceneinstellungen öffnen

Klicken Sie in dem Modul, das Sie teilen möchten (Kalender oder Kontakte), auf das **Einstellungen**-Zahnradsymbol oder die **Teilen**-Schaltfläche.

:::info
Nicht alle Module in dieser Testumgebung zeigen die Teilen-Schaltfläche. In einer Produktionsumgebung mit vollständig freigegebenen ACLs erscheinen Freigabeoptionen auf einzelnen Elementen und Sammlungen.
:::

### Schritt 2: Aktuelle Berechtigungen anzeigen

Das Freigabe-/ACL-Panel zeigt:

- Aktuellen Besitzer
- Vorhandene delegierte Benutzer/Gruppen
- Aktuelle Berechtigungsstufe für jeden

### Schritt 3: Benutzer oder Gruppe hinzufügen

1. Klicken Sie auf **Hinzufügen** oder **Teilen**
2. Suchen Sie nach dem Empfänger per Benutzername oder E-Mail-Adresse
3. Wählen Sie das Ziel aus den Suchergebnissen

### Schritt 4: Berechtigungsstufe zuweisen

Wählen Sie die entsprechende Berechtigung aus dem Dropdown:

- **Betrachter**
- **Teilnehmer**
- **Editor**
- **Administrator (Vollzugriff)**

### Schritt 5: Benachrichtigung senden

Schalten Sie **E-Mail-Benachrichtigung senden** um, wenn SOGo den Empfänger über die freigegebene Ressource informieren soll.

### Schritt 6: Speichern

Klicken Sie auf **Übernehmen** oder **Speichern**, um die Freigabe zu aktivieren.

## Praktische Delegationsbeispiele

| Szenario: Description | Empfohlene Berechtigung | Warum |
|----------|------------------------|-------|
| **Assistent** | Administrator | Benötigt Vollzugriff, um den Kalender in Ihrem Namen zu verwalten |
| **Teamleiter** | Teilnehmer | Kann Ereignisse erstellen/bearbeiten, um Team-Meetings zu planen |
| **Kollege** | Betrachter | Soll Ihre Verfügbarkeit sehen, ohne Änderungen vorzunehmen |
| **Projektteam** | Betrachter (zeitfokussiert) | Muss nur wissen, wann Sie beschäftigt/frei sind |

:::warning
Änderungen an Delegationsberechtigungen treten sofort in Kraft. Überprüfen Sie die Berechtigungsstufen sorgfältig vor dem Speichern.
:::

## Empfängerseite

Wenn eine Ressource für Sie freigegeben wurde:

1. Die freigegebene Ressource erscheint in Ihrer Modulnavigation (z. B. Kalender → Freigegebene Kalender)
2. Die Berechtigungsstufe bestimmt, was Sie tun können:
   - **Betrachter:** Elemente erscheinen eingeblendet oder überlagert, sind aber schreibgeschützt
   - **Teilnehmer:** Erscheint in Ihrer Ansicht, Sie können hinzufügen/bearbeiten, aber Löschungen sind eingeschränkt
   - **Administrator:** Vollständiger Bearbeitungs- und Löschzugriff

## Fehlerbehebung

| Problem: Description | Mögliche Ursache | Lösung |
|---------|-----------------|--------|
| Teilen-Button nicht sichtbar | ACLs in der Konfiguration deaktiviert | Bitten Sie den Administrator, `SOGoACLsSendEMailNotifications` zu aktivieren |
| Benutzer in der Suche nicht gefunden | Benutzer existiert nicht in SOGo | Überprüfen Sie, ob der Empfänger ein SOGo-Konto hat |
| Admin-Berechtigung kann nicht ausgewählt werden | Sie sind nicht der Ressourcenbesitzer | Nur der Besitzer kann Administratorzugriff gewähren |
| Freigegebene Ressource erscheint nicht | Freigabe noch nicht synchronisiert oder Netzwerkproblem | Aktualisieren Sie die Seite oder melden Sie sich nach einigen Sekunden erneut an |
| Delegation funktioniert nicht für E-Mail | E-Mail-Freigabe deaktiviert | Überprüfen Sie `SOGoMailAuxiliaryUserAccountsEnabled` in der SOGo-Konfiguration |

## Sicherheitshinweise

1. **Prinzip der minimalen Rechte** — Gewähren Sie die minimal benötigte Berechtigung
2. **Überwachung** — Überprüfen Sie regelmäßig, wer Zugriff auf Ihre Ressourcen hat
3. **Wann widerrufen** — Entfernen Sie die Delegation, wenn die Zusammenarbeit endet oder sich Rollen ändern
4. **Vertrauliche Informationen** — Seien Sie vorsichtig bei freigegebenen Kalendern, die sensible Besprechungen enthalten

## Erweiterte Delegation mit Ressourcen

Für Räume, Projektoren oder Ausrüstung:

| Ressourcentyp: Description | Einrichtung |
|---------------|------------|
| **Besprechungsraum** | Ressourcenkonto erstellen, als Ressourcentyp festlegen |
| **Projektor** | Zum Kalender hinzufügen, als Ressource markieren, Buchungsberechtigungen erteilen |
| **Ausrüstung** | Als freigegebenes Kalenderelement erstellen, Ressourcenbuchung aktivieren |

:::info
Die Ressourcenkonfiguration erfordert in der Regel Administratorzugriff auf die SOGo-Automatisierungseinrichtung. Einzelne Benutzer delegieren Kalenderelemente als reguläre Ereignisse.
:::

## Fazit

Sie haben erfolgreich gelernt, wie Sie Delegation und Berechtigungen in SOGo 5 verwenden.
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

