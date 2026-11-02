---
titel: Eingaben nie trauen
kurz: Injection und Pfadmanipulation, und warum man prüft statt repariert
dauer: 45 Minuten
projekt: MIus Notes, noScribe-Editor, mius.ch
---
Die grösste Familie von Sicherheitslücken hat eine gemeinsame Ursache: Daten von aussen werden so verwendet, als wären sie Programmcode oder vertrauenswürdige Anweisungen. In der OWASP Top 10 von 2021 steht «Injection» auf Platz drei.

## Injection

Das klassische Beispiel ist SQL. Ein Programm baut eine Abfrage aus Text zusammen:

```python
sql = "SELECT * FROM notizen WHERE titel = '" + suchbegriff + "'"
```

Gibt jemand als Suchbegriff `' OR '1'='1` ein, entsteht `... WHERE titel = '' OR '1'='1'`, und die Bedingung ist immer wahr. Mit etwas mehr Aufwand lassen sich so Tabellen auslesen oder löschen. Das Problem ist nicht der Apostroph. Das Problem ist, dass Daten und Befehl im selben Text landen und die Datenbank sie nicht mehr unterscheiden kann.

Die Lösung heisst **Prepared Statements**: Die Abfrage wird mit Platzhaltern an die Datenbank geschickt, die Werte separat. Die Datenbank behandelt die Werte dann immer als Daten.

```python
db.execute("SELECT * FROM notizen WHERE titel = ?", (suchbegriff,))
```

Dasselbe Muster gibt es überall, wo Text zu Befehlen wird: Shell-Befehle (`subprocess` mit Liste statt Text), HTML (nächster Schritt), Dateipfade (unten), und neu auch Sprachmodelle: Wenn eine KI Text aus einer Webseite liest und darin Anweisungen findet, ist das **Prompt Injection**.

## Pfadmanipulation

Eine Anwendung liefert Dateien aus einem Ordner aus, der Dateiname kommt aus der Anfrage: `/datei?name=bericht.pdf`. Was passiert bei `name=../../konfig.php`? Das `..` führt eine Ebene nach oben, und plötzlich liefert die Anwendung Dateien ausserhalb des erlaubten Ordners aus. Das heisst **Path Traversal**.

Die falsche Lösung ist, `..` aus dem Namen zu löschen. `....//` wird nach dem Löschen wieder zu `../`, und es gibt weitere Schreibweisen. Die richtige Lösung ist, den vollständigen Pfad aufzulösen und zu prüfen, ob er noch im erlaubten Ordner liegt. Wenn nicht: ablehnen, nicht reparieren.

## Erlaubnisliste statt Verbotsliste

Daraus folgt ein allgemeines Prinzip: Prüfe gegen das, was erlaubt ist, nicht gegen das, was verboten ist. Eine Verbotsliste übersieht immer etwas. Die Antworten der Wollfaden-Umfrage auf mius.ch werden so geprüft: Nur Zahlen innerhalb der bekannten Antworten sind gültig, alles andere wird abgewiesen.

## Projektbezug

**MIus Notes** nutzt ausschliesslich Prepared Statements, und jede Abfrage ist an die eigene Benutzer-ID gebunden. Der **noScribe-Editor** hat einen lokalen Server, der laut README «ausschliesslich Dateien unterhalb des gewählten Interviewordners» herausgibt. Das ist die Pfadprüfung aus der Übung. **mius.ch** prüft in `antworten_pruefen()`, dass jede Antwort eine ganze Zahl im gültigen Bereich ist.

## Karten

F: Was ist die gemeinsame Ursache aller Injection-Lücken?
A: Daten von aussen werden in einen Befehl eingebaut, und das ausführende System kann Daten und Befehl nicht mehr unterscheiden.

F: Wie verhindern Prepared Statements SQL-Injection?
A: Abfrage und Werte gehen getrennt an die Datenbank. Die Werte werden immer als Daten behandelt, nie als Teil des Befehls.

F: Warum reicht es nicht, «..» aus einem Dateinamen zu entfernen?
A: Es gibt andere Schreibweisen, und das Entfernen kann neue `..` erzeugen (`....//`). Richtig ist: Pfad vollständig auflösen und prüfen, ob er im erlaubten Ordner liegt.

F: Was ist besser, eine Erlaubnisliste oder eine Verbotsliste?
A: Eine Erlaubnisliste. Sie lässt nur Bekanntes durch, eine Verbotsliste übersieht immer etwas.

F: Was ist Prompt Injection?
A: Anweisungen, die in Daten versteckt sind (eine Webseite, eine Datei), werden von einem Sprachmodell als Auftrag gelesen. Dieselbe Ursache wie bei SQL-Injection: Daten und Befehl im selben Text.

## Prompt

```
Liste alle Stellen in diesem Code, an denen Daten von aussen (Formular, URL,
Datei, Schnittstelle, Datenbankinhalt anderer Personen) in einen Befehl
gelangen: SQL, Shell, Dateipfad, HTML, Weiterleitung. Gib zu jeder Stelle
an, wie sie geschützt ist, und ob gegen eine Erlaubnisliste oder eine
Verbotsliste geprüft wird.
```

## Literatur

- OWASP (2021). *OWASP Top 10:2021*, A03 Injection. owasp.org/Top10
- OWASP: SQL Injection Prevention Cheat Sheet; Input Validation Cheat Sheet. cheatsheetseries.owasp.org
- MITRE: CWE-22, Improper Limitation of a Pathname to a Restricted Directory. cwe.mitre.org
- Greshake, K. et al. (2023). Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection. *ACM Workshop on Artificial Intelligence and Security*.
