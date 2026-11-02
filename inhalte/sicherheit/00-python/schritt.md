---
titel: Python auffrischen
kurz: Funktionen, Listen, Wörterbücher und Tests, alles, was die Übungen brauchen
dauer: 20 Minuten
projekt: alle
---
Du hattest Python im Studium. Dieser Schritt holt das Wichtigste zurück, damit die Sicherheitsübungen danach nicht an der Sprache scheitern. Wenn dir das alles vertraut vorkommt: Übung lösen und weiter.

## Die vier Bausteine

**Funktionen** nehmen Werte entgegen und geben einen Wert zurück. In Python stehen Typangaben freiwillig hinter dem Doppelpunkt. Sie ändern nichts am Verhalten, helfen aber beim Lesen und Prüfen.

```python
def begruessen(name: str) -> str:
    return "Hallo " + name
```

**Listen** sind geordnet und veränderbar: `[3, 1, 2]`. Mit `for x in liste:` gehst du sie durch, mit `sorted(liste)` bekommst du eine sortierte Kopie.

**Wörterbücher** (`dict`) ordnen Schlüsseln Werte zu: `{"rolle": "Lehrperson", "stufe": 2}`. Sie sind die wichtigste Datenstruktur in Python. Auch JSON aus einer Schnittstelle landet in Python als Wörterbuch.

**Tests** prüfen, ob eine Funktion tut, was sie soll. Ein Test ist eine Funktion, die mit `test_` beginnt und `assert` verwendet. Ist die Bedingung falsch, bricht `assert` ab, und der Test gilt als nicht bestanden.

```python
def test_begruessen():
    assert begruessen("Samuel") == "Hallo Samuel"
```

## Warum Tests hier wichtig sind

Alle Übungen in der Lernwerkstatt werden mit Tests geprüft. Das ist kein Schulsystem, sondern genau das, was in deinen Projekten passiert: Das PräsenzTool hat 388 Prüfungen, MIus Notes lässt bei jedem Push PHPUnit laufen. Ein Test ist eine ausführbare Behauptung über den Code. Wenn du künftig Claude etwas bauen lässt, ist «schreib auch Tests dazu, und zeig mir, dass sie vorher scheitern» einer der wirksamsten Sätze, die du sagen kannst.

## Wo du programmierst

Im Browser: Das Feld unten ist ein Editor, «Prüfen» führt deinen Code mit Python aus, direkt auf deinem Gerät. Nichts wird an einen Server geschickt.

Auf dem Rechner: Im Repo liegt dieselbe Übung unter `inhalte/sicherheit/00-python/aufgabe.py`. Mit `python pruefen.py 00` prüfst du sie dort. Das lohnt sich, sobald die Übungen länger werden.

## Projektbezug

Die Wollfaden-Umfrage auf mius.ch zählt, wie viele Fäden durch jeden Nagel laufen. Das ist genau die Übung unten: Häufigkeiten in einem Wörterbuch zählen. Die Funktion `zaehle()` in `site/faden.js` macht dasselbe in JavaScript.

## Karten

F: Was ist der Unterschied zwischen einer Liste und einem Wörterbuch?
A: Eine Liste ist eine geordnete Folge von Werten, angesprochen über die Position (`liste[0]`). Ein Wörterbuch ordnet Schlüsseln Werte zu, angesprochen über den Schlüssel (`d["rolle"]`).

F: Was passiert, wenn ein `assert` falsch ist?
A: Python wirft einen `AssertionError`. Im Test heisst das: nicht bestanden. Der Text nach dem Komma (`assert x == 1, "Text"`) erscheint als Meldung.

F: Wozu dienen Typangaben wie `-> str` in Python?
A: Sie dokumentieren, was eine Funktion erwartet und zurückgibt. Python prüft sie zur Laufzeit nicht, Werkzeuge wie mypy oder der Editor schon.

F: Warum soll ein Test zuerst scheitern?
A: Ein Test, der nie scheitern kann, prüft nichts. Erst wenn er bei falschem Code rot und bei richtigem grün wird, ist er ein Beleg.

## Prompt

Wenn du Claude Code schreiben lässt, verlange Tests, die du lesen kannst:

```
Schreib die Funktion und dazu Tests mit pytest. Jeder Test hat einen Docstring,
der in einem Satz sagt, was er prüft. Zeig mir zuerst die Tests und wie sie
mit einer leeren Funktion scheitern, dann die Umsetzung.
```

## Literatur

- Python Software Foundation: The Python Tutorial, Kapitel 3 bis 5. docs.python.org/3/tutorial
- Okken, B. (2022). *Python Testing with pytest* (2. Aufl.). Pragmatic Bookshelf.
