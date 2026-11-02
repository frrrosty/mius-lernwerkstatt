# Lernwerkstatt

Persönliche Lernplattform Informatik: Sie macht verständlich, welche Informatik in den eigenen Projekten steckt, und führt von dort in die Grundlagen. Konzept: [KONZEPT.md](KONZEPT.md).

## Stand

Prototyp mit dem Lernpfad **Sicherheit von Grund auf**: acht Schritte, je Text, Python-Übung, Karten und Prompt für Claude.

## Lokal

```bash
pip install -r requirements.txt
python pruefen.py 03          # deine Lösung in inhalte/sicherheit/03-*/aufgabe.py prüfen
python -m pytest tests        # alle Übungen: Lösungen bestehen, Vorlagen noch nicht
python bauen.py               # Seite nach dist/, mit Python für den Browser
python werkzeug/vorschau.py   # http://localhost:8710, mit derselben CSP wie auf dem Server
```

## Aufbau

```
inhalte/sicherheit/NN-name/   schritt.md (Text, Karten, Prompt, Literatur)
                              aufgabe.py · tests.py · loesung.py
werkzeug/runner.py            führt Code und Tests aus, im Browser und lokal
bauen.py                      erzeugt dist/, holt Pyodide mit Prüfsumme
web/                          Oberfläche: app.js, rechner.js (Python im Worker), sw.js, .htaccess
.github/workflows/            ci.yml bei jedem Push, deploy.yml von Hand
docs/einrichten.md            SSH, Zugangsschutz, Secrets
```

## Ausliefern

Einmal einrichten nach [docs/einrichten.md](docs/einrichten.md), dann *Actions → Deploy → Run workflow*.
