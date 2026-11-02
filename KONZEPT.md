# Lernwerkstatt: Konzept

**Status:** Prototyp Etappe 1 gebaut (Lernpfad Sicherheit), noch nicht ausgeliefert
**Erfasst:** 2026-11-02
**Grundlage:** Anforderungs-Dashboard «Lernwerkstatt Anforderungen» (Claude-Artefakt), Antworten vom 2. November 2026, festgehalten in [docs/anforderungen-2026-11-02.md](docs/anforderungen-2026-11-02.md)

## Kurzbeschreibung

Eine Lernplattform nur für Samuel. Sie macht verständlich, welche Informatik in den eigenen Projekten der letzten Jahre steckt, und führt von dort in die Grundlagen der Informatik, die dahinter liegen. Ziel ist Weiterbildung: fachlich sicherer werden, mitreden und prüfen können, und erklären können, was gebaut wurde.

## Warum

In den letzten Jahren sind mit KI-Unterstützung mehrere Anwendungen entstanden: MIus Notes, Shutter Call, das PräsenzTool, die neue Website mius.ch, der noScribe-Editor, der OLAT Builder und weitere. Sie enthalten viel Informatik: CI/CD, Geheimnisverwaltung, Datenbanken, Schnittstellen, Anmeldung, Web-Sicherheit, Signatur und Play Store, Synchronisation. Gebaut hat sie zum grössten Teil Claude. Samuel hat die Anforderungen gestellt, entschieden, geprüft und die Anwendungen eingesetzt.

Das Verständnis ist dabei oft an der Oberfläche geblieben. Das zeigt sich am deutlichsten bei der Sicherheit: Zu allen neun Prüfpunkten im Dashboard lautete die Antwort «weiss nicht».

Dazu kommt ein konkreter Anlass. In der Disputation geht es nicht um diese Anwendungen. Es kann aber sein, dass das informatische Fachwissen in Frage gestellt oder diskutiert wird. Dann soll Samuel ehrlich und sicher erklären können, was er gemacht hat, mit welcher Rolle und mit welchem Verständnis.

## Haltung

**Ehrlich über die Rolle.** Die Plattform hilft nicht dabei, mehr Programmierleistung zu behaupten, als da war. Sie hilft, die tatsächliche Rolle gut zu vertreten: Anforderungen stellen, Architektur entscheiden, Sicherheit und Datenschutz verlangen, Ergebnisse prüfen, im Einsatz erproben. Diese Kompetenz ist echt und lässt sich verteidigen, wenn das Fachwissen dahinter stimmt.

**Verstehen heisst erklären können.** Lesen erzeugt das Gefühl von Verständnis. Jede Lerneinheit endet deshalb mit etwas, das Samuel selbst tut: eine Frage in eigenen Worten beantworten, eine Stelle im Code finden, eine kleine Änderung machen.

**Vom eigenen Code in die Grundlagen.** Jedes Thema beginnt bei einem Projekt und führt von dort in die allgemeine Informatik. Was die Projekte nicht berühren, zeigt eine Lückenkarte, damit später entschieden werden kann, was ergänzt wird.

## Anforderungen

Aus dem Dashboard, verdichtet. Wo die Antworten breit waren (alle Ziele, alle Lernformen), ist hier eine Reihenfolge festgelegt.

| Bereich | Entscheid | Folge für den Bau |
|---|---|---|
| Ziel | Zuerst verstehen und mitreden, dann selbst bauen, später auch lehren | Etappe 1 zielt auf Erklären, nicht auf Programmieren |
| Niveau | Wie im Informatikstudium; Grundwissen vorhanden, aber oberflächlich | Fachbegriffe mit Erklärung, Hintergründe, Literatur |
| Breite | Projekte als Einstieg, dann in die Tiefe; Lücken sichtbar machen | Lückenkarte gehört zu Etappe 1 |
| Lernformen | Erklärseiten, Lernpfade, Übungen, Wiederholung, Claude als Tutor | In dieser Reihenfolge, siehe Etappen |
| Zeit | Mal drei Minuten, meist ein bis zwei Stunden pro Woche | Zwei Modi: Häppchen auf dem Handy, Vertiefung am Laptop |
| Geräte | Handy, Tablet und Laptop | Mobil zuerst, als installierbare Web-App |
| Notizen | In MIus Notes, eigener Bereich «Lernwerkstatt» | Keine eigene Notizfunktion, Anbindung über die bestehende Schnittstelle |
| Inhalte | Gerüst automatisch aus den Repos, Erklärungen kuratiert | Ein Skript liest Workflows, Abhängigkeiten, Commits; Texte liegen als Markdown im Repo |
| Hosting | Hostpoint, eigene Subdomain | `lernwerkstatt.mius.ch` |
| Bauen | Zusammen, Claude baut viel | Claude baut, erklärt jeden Schritt, Samuel entscheidet und setzt einzelne kleine Teile selbst um |
| Zugriff | Nur Samuel, Kolleginnen und Kollegen höchstens als Demo | Anmeldung über das bestehende MIUS-Konto, eine Demo-Fassung ohne private Inhalte später |
| Lernprotokoll | Später entscheiden, aber möglich machen | Fortschritt mit Datum speichern, nichts auswerten |

Horizont-Themen mit hohem Interesse: Softwarearchitektur, Datenbanken, verteilte Systeme, Kryptografie, theoretische Informatik, Mensch-Computer-Interaktion, Informatik und Gesellschaft. Mit mittlerem Interesse: Algorithmen, Rechnernetze, Betriebssysteme, KI, Software Engineering.

## Inhalt

Vier Arten von Inhalten, alle als Markdown-Dateien im Repo unter `inhalte/`:

1. **Projektseiten** (`inhalte/projekte/`). Pro Projekt eine Seite, die sich in zwei Minuten erzählen lässt: welches Problem es löst, wie es aufgebaut ist (Schema), welche Entscheide getroffen wurden, wer was gebaut hat, wo welche Informatik drinsteckt. Dazu Links auf die Stellen im Code.
2. **Fachgebiete** (`inhalte/gebiete/`). Pro Gebiet eine Erklärseite auf Studienniveau: Begriffe, Zusammenhänge, Literatur. Mit Beispielen aus den Projekten, aber auch ohne sie verständlich. Am Ende Fragen zum Selbsterklären.
3. **Lernpfade** (`inhalte/pfade/`). Geordnete Folgen von Schritten, zum Beispiel «Sicherheit von Grund auf» oder «Vom Push bis zum Play Store». Jeder Schritt verweist auf Gebiete und Projektstellen und endet mit einer Aufgabe.
4. **Karten** (`inhalte/karten/`). Kurze Frage-Antwort-Paare für den Drei-Minuten-Modus, mit Wiederholung in wachsenden Abständen.

Dazu automatisch erzeugt:

- **Landkarte** Projekte × Fachgebiete, mit Belegen aus den Repos (wie im Dashboard).
- **Lückenkarte** der Fachgebiete, die kein Projekt berührt.

## Funktionen

- Lesen: Projektseiten, Gebiete, Pfade; Suche; auf dem Handy gut lesbar.
- Üben: Karten mit Wiederholung (Leitner-System, fünf Fächer), Fragen zum Selbsterklären mit Musterantwort zum Aufdecken.
- Fortschritt: pro Gebiet die eigene Einschätzung (Stufe 0 bis 3, wie im Dashboard), pro Pfad erledigte Schritte, Verlauf mit Datum.
- Notieren: Knopf «In MIus Notes festhalten» auf jeder Seite. Die Notiz landet im Bereich «Lernwerkstatt», mit Link zurück.
- Fragen (Etappe 3): Claude erklärt eine Datei oder einen Commit auf dem gewählten Niveau und fragt zurück.

## Technik

Die Wahl ist so getroffen, dass die Technik selbst Lernstoff ist und auf dem aufbaut, was schon läuft.

| Teil | Wahl | Warum | Was Samuel daran lernt |
|---|---|---|---|
| Inhalte | Markdown im Git-Repo | Versioniert, offline lesbar, mit jedem Editor bearbeitbar | Git, Branches, Pull Requests an eigenem Material |
| Seite | Statisch erzeugt mit einem Python-Skript | Gleiches Muster wie `site/bauen.py` bei mius.ch, schnell, sicher, keine Laufzeit nötig | Wie ein Generator funktioniert |
| App-Teil | Kleine PHP-App auf der MIUS-Plattform | Fortschritt und Karten brauchen Speicher; die Plattform liefert Konto, Sitzung, CSRF-Schutz und SQLite | Schnittstellen, Sitzungen, Datenbankschema |
| Anmeldung | MIUS-Konto (`konto.mius.ch`) | Schon vorhanden, ein Konto für alle Apps | Vergleich mit MIus Notes: dort Argon2id und Zwei-Faktor, hier bcrypt ohne zweiten Faktor. Warum? Reicht das? |
| Mobil | Installierbare Web-App mit Service Worker | Handy und Tablet ohne App Store | Offline, Caching, was ein Service Worker darf |
| Auslieferung | GitHub Action baut und lädt per rsync auf Hostpoint | Gleiches Muster wie Shutter Call und PräsenzTool | CI/CD, Secrets, Actions auf Commits festlegen |
| Notizen | REST-Schnittstelle von MIus Notes | Kein zweiter Ort für Wissen | Token mit minimalen Rechten, was passiert, wenn MIus Notes nicht antwortet |

**Entscheid zur Plattform:** Die App läuft als eigene Subdomain auf der MIUS-Plattform, nicht als Teil von MIus Notes. MIus Notes hält die echten Daten und ist das sicherheitskritischste Projekt; jeder zusätzliche Teil dort vergrössert die Angriffsfläche.

**Offen zu klären:** Die App-Vorlage (`plattform/einkaufsliste`) liegt im Repo mius-website und bindet den Kern über einen Pfad ein. Die Lernwerkstatt hat ein eigenes Repo. Für den Bau muss entschieden werden, ob der Kern auf dem Server eingebunden wird (wie heute für Apps vorgesehen, `~/mius-kern/`) oder ob die Lernwerkstatt als Ordner in mius-website lebt. Vorschlag: eigenes Repo, Kern auf dem Server.

## Sicherheit

Die Lernwerkstatt enthält Wissen über die eigenen Systeme: Aufbau, Schwachstellen, Prüfpunkte. Das ist für Angreifer wertvoll.

- Alles hinter Anmeldung, auch die statischen Seiten. Keine öffentliche Fassung mit Projektinhalten.
- Keine Geheimnisse in den Inhalten: keine Server-Namen, Pfade auf dem Server, Secret-Namen mit Werten, Datenbankschemas mit echten Daten.
- `robots.txt` sperrt alles, `noindex` auf allen Seiten.
- Die Demo-Fassung für Kolleginnen und Kollegen (später) wird aus denselben Quellen ohne Projektseiten erzeugt.
- Der Lernpfad Sicherheit beginnt mit einem Bedrohungsmodell für genau diese App.

## Entscheide vom 2. November 2026

Nach dem Lesen des Konzepts: Samuel will an einem echten Prototyp starten, mit **Programmieraufgaben in Python** (Anknüpfen an die Grundlagen aus dem Studium) und **Sicherheit früh**, damit er künftig gezielter auf Sicherheitsaspekte prüfen und prompten kann. Daraus folgt für Etappe 1:

- **Der erste Lernpfad ist «Sicherheit von Grund auf»**, acht Schritte: Python auffrischen, Bedrohungsmodell, Passwörter, Eingaben, Ausgaben, Geheimnisse, Bremsen, Lieferkette. Jeder Schritt hat Text auf Studienniveau mit Literatur, Projektbezug, eine Python-Übung mit Tests, Karten und einen **Prompt-Baustein**, mit dem Claude die eigenen Projekte genau zu diesem Punkt prüft.
- **Python läuft im Browser** (Pyodide, Python als WebAssembly). Übungen funktionieren damit auf Handy, Tablet und Laptop ohne Installation, und der Code verlässt das Gerät nie. Die gleichen Übungen laufen auch lokal mit `python pruefen.py NN`.
- **Pyodide kommt vom eigenen Server**, nicht von einem CDN. `bauen.py` lädt es aus npm und prüft die SHA-512-Prüfsumme. So bleibt die Content-Security-Policy streng (`script-src 'self' 'wasm-unsafe-eval'`).
- **Übergangslösungen im Prototyp**, beide bewusst: Fortschritt, Code und Notizen liegen im Browser (localStorage), also nicht zwischen Geräten synchronisiert. Der Zugang ist mit Basic Auth geschützt statt mit dem MIUS-Konto. Beides wird in Etappe 1b ersetzt.
- **Projektseiten zum Erklären** (MIus Notes, Shutter Call, PräsenzTool) folgen nach dem Lernpfad.
- **Auslieferung** per GitHub Action auf Knopfdruck, SSH mit festem Server-Fingerabdruck, Actions auf Commit-Hash festgelegt. Einrichtung: [docs/einrichten.md](docs/einrichten.md).

## Etappen

Jede Etappe ist für sich nutzbar.

**Etappe 1: Sicherheit und Python.** (Prototyp gebaut)
- Lernpfad «Sicherheit von Grund auf», acht Schritte mit Python-Übungen, 39 Karten, Prompt-Bausteinen
- Kartentraining mit fünf Fächern (Leitner)
- Installierbare Web-App, offline lesbar
- Auslieferung auf `lernwerkstatt.mius.ch` hinter Basic Auth

**Etappe 1b: Erklären können.**
- Projektseiten für MIus Notes, Shutter Call, PräsenzTool
- Gebiete: CI/CD, Anmeldung und Sitzungen, Datenbanken
- Landkarte und Lückenkarte
- Anmeldung über das MIUS-Konto, Fortschritt auf dem Server statt im Browser

**Etappe 2: Üben am eigenen Code.** Übungs-Repo mit Aufgaben, Lösungen als Pull Request. Fortschritt pro Gebiet. Weitere Projektseiten (mius.ch, noScribe-Editor, OLAT Builder, Auto-Distanzmesser).

**Etappe 3: Claude als Tutor.** Erklärungen zu einer Datei oder einem Commit auf dem gewählten Niveau, Rückfragen, Notizen nach MIus Notes.

**Etappe 4: Horizont.** Gebiete ohne Projektbezug nach der Lückenkarte: theoretische Informatik, verteilte Systeme in der Tiefe, Kryptografie. Ein kleines Projekt von Grund auf, das Samuel selbst schreibt.

## Kritische Einordnung

- **Gefahr eines weiteren Werkzeugs.** Die grösste Gefahr ist, dass eine schöne Plattform entsteht und das Verständnis trotzdem nicht wächst. Gegenmittel: Etappe 1 klein halten, früh benutzen, an der Frage messen: «Kann ich das jetzt erklären?»
- **Inhalte von Claude über Claudes Arbeit.** Die Erklärungen schreibt zum grossen Teil Claude, über Code, den Claude geschrieben hat. Fehler können sich so fortsetzen. Gegenmittel: Literaturangaben bei jedem Gebiet, Fragen, die gegen eine zweite Quelle geprüft werden, und Samuels eigene Formulierung als Prüfstein.
- **Pflege.** Die Projekte ändern sich laufend. Was automatisch aus den Repos kommt, bleibt aktuell; die kuratierten Texte brauchen ab und zu einen Blick. Jede Projektseite trägt das Datum ihres Stands.

## Erfolg

Etappe 1 ist gelungen, wenn Samuel ohne Unterlagen:
- jedes der drei Projekte in zwei Minuten erklären kann, mit ehrlicher Rolle,
- die neun Sicherheitspunkte aus dem Dashboard einordnen kann,
- auf eine Fachfrage zu Anmeldung, CI/CD oder Datenbanken mit einem Beispiel aus dem eigenen Code antworten kann.
