---
titel: Geheimnisse gehören nicht ins Repo
kurz: Schlüssel, Tokens, .env und was passiert, wenn doch eines durchrutscht
dauer: 35 Minuten
projekt: Shutter Call, MIus Notes, PräsenzTool
---
Jede deiner Anwendungen hat Geheimnisse: Datenbankpasswörter, SSH-Schlüssel für das Hochladen, den Signaturschlüssel der Android-App, Tokens für Schnittstellen. Gelangt eines davon in ein Repository, ist es öffentlich oder zumindest dauerhaft in der Versionsgeschichte, auch wenn die Datei später gelöscht wird.

## Warum Löschen nicht hilft

Git speichert jeden Stand. Wird ein Passwort in Commit 12 eingetragen und in Commit 13 entfernt, steht es in Commit 12 weiterhin. Wer das Repo klont, hat es. Die einzige sichere Reaktion auf ein durchgerutschtes Geheimnis ist: **sofort ungültig machen und ersetzen** («rotieren»). Die Geschichte umzuschreiben, ist danach nur noch Aufräumen.

## Wo Geheimnisse hingehören

- **In der Pipeline**: GitHub Secrets. Sie werden verschlüsselt gespeichert, in Protokollen geschwärzt und nur an Workflows im eigenen Repo gegeben.
- **Auf dem Server**: in einer Konfigurationsdatei ausserhalb des Webordners, mit Rechten, die nur der eigene Benutzer lesen darf (Unix: `600`).
- **Lokal**: in einer Datei wie `.env`, die in `.gitignore` steht.

## Vorbeugen und Erkennen

Menschen vergessen. Deshalb gibt es Werkzeuge, die vor dem Commit oder beim Push nach Mustern suchen: Schlüsselanfänge wie `-----BEGIN PRIVATE KEY-----`, Token-Formate wie `ghp_…` von GitHub oder `AKIA…` von AWS, Zuweisungen wie `password = "…"`. GitHub bietet das als **Secret Scanning** mit **Push Protection** an: Ein Push mit erkanntem Geheimnis wird abgewiesen. Die Übung unten baut einen einfachen solchen Scanner.

Solche Scanner haben Grenzen. Sie finden bekannte Formate, aber kein zufälliges Passwort ohne Hinweis davor. Und sie melden Fehlalarme. Ein Scanner ersetzt die Regel nicht, sondern fängt Fehler ab.

## Projektbezug

**Shutter Call** übergibt im Deploy-Workflow den SSH-Schlüssel, die Datenbankzugänge, den Android-Keystore und das Firebase-Dienstkonto aus GitHub Secrets. Der Keystore ist besonders heikel: Geht er verloren, kann die App im Play Store nicht mehr aktualisiert werden, ausser über Play App Signing. **MIus Notes** lässt den wichtigsten Schlüssel (`APP_KEY`) auf dem Server entstehen; er verlässt ihn nie, auch nicht Richtung GitHub. **Das PräsenzTool** erklärt im README, warum der Pepper nie geändert werden darf: Jede Änderung macht alle gedruckten Karten wertlos. Ob Secret Scanning und Push Protection in deinen Repos eingeschaltet sind, ist eine offene Frage aus dem Anforderungs-Dashboard.

## Karten

F: Warum reicht es nicht, ein versehentlich eingechecktes Passwort in einem neuen Commit zu löschen?
A: Git behält alle früheren Stände. Das Passwort bleibt in der Geschichte und bei allen, die geklont haben.

F: Was ist die richtige Reaktion auf ein durchgerutschtes Geheimnis?
A: Sofort ungültig machen und ein neues erzeugen (rotieren). Erst danach die Geschichte bereinigen.

F: Was bedeutet Dateirecht 600 unter Unix?
A: Nur der Besitzer darf lesen und schreiben, alle anderen nichts.

F: Was ist Push Protection bei GitHub?
A: Ein Push, in dem ein bekanntes Geheimnisformat erkannt wird, wird abgewiesen, bevor er im Repo landet.

F: Was findet ein Musterscanner nicht?
A: Geheimnisse ohne erkennbares Format oder Hinweis, zum Beispiel ein zufälliges Passwort in einer Liste.

## Prompt

```
Prüfe dieses Repository auf Geheimnisse: im aktuellen Stand und in der
Git-Geschichte (git log -p). Prüfe auch .gitignore, Beispielkonfigurationen
und Workflows: Werden Secrets in Protokolle geschrieben, an fremde Actions
übergeben oder in Artefakte gepackt? Zeig Fundstellen, aber nie den Wert.
```

## Literatur

- OWASP: Secrets Management Cheat Sheet. cheatsheetseries.owasp.org
- GitHub Docs: About secret scanning; Push protection. docs.github.com
- Meli, M., McNiece, M. R., Reaves, B. (2019). How Bad Can It Git? Characterizing Secret Leakage in Public GitHub Repositories. *Network and Distributed System Security Symposium (NDSS)*.
