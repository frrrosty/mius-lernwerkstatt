# Einrichten: SSH, Zugangsschutz, Deploy

Einmalig, etwa 20 Minuten. Jeder Schritt sagt, was er tut und warum.
Der private Schlüssel entsteht auf deinem Rechner und geht nur an GitHub, nie durch Claude.

## 1. Schlüsselpaar für den Deploy erzeugen

Auf deinem Rechner, im Terminal:

```bash
ssh-keygen -t ed25519 -C "github-deploy-lernwerkstatt" -f lernwerkstatt_deploy -N ""
```

Es entstehen zwei Dateien: `lernwerkstatt_deploy` (privat, geheim) und `lernwerkstatt_deploy.pub` (öffentlich).

- **ed25519** ist ein modernes Verfahren mit kurzen Schlüsseln und guter Sicherheit.
- **Ohne Passphrase** (`-N ""`), weil die Action den Schlüssel ohne Mensch benutzt. Das ist vertretbar, weil er nur für diesen Zweck dient und in GitHub Secrets verschlüsselt liegt. Ein eigener Schlüssel pro Projekt heisst: Wird er bekannt, ist nur dieses Projekt betroffen.

## 2. Öffentlichen Schlüssel bei Hostpoint hinterlegen

Im Hostpoint-Panel unter SSH-Zugang den Inhalt von `lernwerkstatt_deploy.pub` eintragen, oder auf dem Server an `~/.ssh/authorized_keys` anhängen. Der öffentliche Schlüssel darf jeder sehen. Er erlaubt nur, mit dem passenden privaten Schlüssel hereinzukommen.

## 3. Fingerabdruck des Servers festhalten

```bash
ssh-keyscan -t ed25519 <dein-ssh-host> > known_hosts_lernwerkstatt
ssh-keygen -lf known_hosts_lernwerkstatt
```

Vergleiche den angezeigten Fingerabdruck (`SHA256:…`) mit dem, den Hostpoint im Panel oder in der Hilfe angibt. Erst wenn beide gleich sind, ist die Zeile vertrauenswürdig. Warum so umständlich? Die Action soll sich nur mit dem echten Server verbinden. Würde sie bei jedem Lauf `ssh-keyscan` selbst ausführen, nähme sie jeden Server an, der sich unterwegs dazwischenschaltet.

## 4. Passwortdatei für den Zugangsschutz anlegen

Die Lernwerkstatt ist vorerst mit Basic Auth geschützt (Benutzername und Passwort über HTTPS). Auf dem Server, ausserhalb des Webordners:

```bash
htpasswd -B -c ~/lernwerkstatt.htpasswd samuel
```

`-B` heisst bcrypt, siehe Lernpfad Schritt 02. Ein langes Passwort aus dem Passwortmanager. Den vollständigen Pfad der Datei brauchst du gleich als Secret (`echo ~/lernwerkstatt.htpasswd` zeigt ihn).

## 5. Secrets bei GitHub eintragen

Im Repo unter *Settings → Secrets and variables → Actions*, und zwar in einer **Umgebung** namens `produktion` (*Settings → Environments → New environment*). In der Umgebung lässt sich einstellen, dass ein Deploy deine Freigabe braucht.

| Secret | Inhalt |
|---|---|
| `SSH_HOST` | der SSH-Host von Hostpoint |
| `SSH_USER` | dein Hostpoint-Benutzername |
| `SSH_PRIVATE_KEY` | der ganze Inhalt von `lernwerkstatt_deploy`, inklusive der BEGIN- und END-Zeile |
| `SSH_KNOWN_HOSTS` | der Inhalt von `known_hosts_lernwerkstatt` aus Schritt 3 |
| `SSH_TARGET_DIR` | der Webordner der Subdomain |
| `HTPASSWD_PFAD` | der vollständige Pfad aus Schritt 4 |

## 6. Aufräumen

```bash
rm lernwerkstatt_deploy known_hosts_lernwerkstatt
```

Der private Schlüssel liegt jetzt nur noch in GitHub. Geht etwas schief, erzeugst du einfach einen neuen und ersetzt den alten bei Hostpoint und in GitHub. Das ist «Rotieren» aus Schritt 05.

## 7. Ausliefern

*Actions → Deploy → Run workflow*. Die Action prüft die Übungen, baut die Seite, prüft die Pyodide-Prüfsumme, trägt den Pfad der Passwortdatei ein und lädt alles per rsync hoch.

## Danach prüfen

- Die Subdomain fragt nach Benutzername und Passwort.
- Eine Übung lösen: Python lädt beim ersten Mal einige Sekunden.
- In den Entwicklerwerkzeugen des Browsers (Netzwerk) sind keine Anfragen an fremde Server zu sehen, und unter Antwort-Header steht die Content-Security-Policy.

## Später

Basic Auth ist eine Übergangslösung: Der Browser merkt sich das Passwort, Abmelden ist umständlich, und es gibt keine Bremse gegen Raten auf Anwendungsebene (Hostpoint drosselt selbst, wie stark, ist offen). Der nächste Schritt ist die Anmeldung über das MIUS-Konto, siehe KONZEPT.md.
