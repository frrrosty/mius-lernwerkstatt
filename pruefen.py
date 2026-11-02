#!/usr/bin/env python3
"""Prüft deine Lösung auf dem eigenen Rechner, genau wie im Browser.

  python pruefen.py 03            prüft inhalte/sicherheit/03-*/aufgabe.py
  python pruefen.py 03 loesung    prüft die Musterlösung (zum Vergleichen)

Arbeite in aufgabe.py. Die Datei ist versioniert: Mit git siehst du jederzeit,
was du geändert hast (git diff), und kannst zurück (git restore).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "werkzeug"))
from runner import ausfuehren  # noqa: E402

PFAD = Path(__file__).parent / "inhalte" / "sicherheit"


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    nr = sys.argv[1].split("-")[0]   # «03» oder «03-eingaben», beides geht
    treffer = sorted(PFAD.glob(nr.zfill(2) + "-*"))
    if not treffer:
        print(f"Keinen Schritt {sys.argv[1]} gefunden.")
        return 1
    ordner = treffer[0]
    datei = "loesung.py" if len(sys.argv) > 2 and sys.argv[2] == "loesung" else "aufgabe.py"
    r = ausfuehren((ordner / datei).read_text(encoding="utf-8"), (ordner / "tests.py").read_text(encoding="utf-8"))
    print(f"{ordner.name} · {datei}\n")
    if r.get("ausgabe"):
        print("Ausgabe deines Codes:\n" + r["ausgabe"])
    if "fehler" in r:
        print("Dein Code startet nicht:\n" + r["fehler"])
        return 1
    for beschreibung, ok, meldung in r["tests"]:
        print(("  ✓ " if ok else "  ✗ ") + beschreibung + ("" if ok else f"\n      {meldung}"))
    bestanden = sum(1 for t in r["tests"] if t[1])
    print(f"\n{bestanden} von {len(r['tests'])} bestanden")
    return 0 if bestanden == len(r["tests"]) else 1


if __name__ == "__main__":
    sys.exit(main())
