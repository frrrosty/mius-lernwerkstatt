"""Sicherung für alle Übungen, läuft in der CI bei jedem Push.

Zwei Regeln:
1. Jede Musterlösung besteht alle ihre Tests.
2. Jede Vorlage (aufgabe.py) besteht sie NICHT. Sonst wäre die Übung schon gelöst,
   bevor du anfängst, oder die Tests prüfen zu wenig.
"""
import sys
from pathlib import Path

import pytest

WURZEL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WURZEL / "werkzeug"))
from runner import ausfuehren  # noqa: E402

SCHRITTE = sorted(p for p in (WURZEL / "inhalte" / "sicherheit").iterdir() if (p / "tests.py").exists())


@pytest.mark.parametrize("ordner", SCHRITTE, ids=lambda p: p.name)
def test_loesung_besteht(ordner):
    r = ausfuehren((ordner / "loesung.py").read_text(encoding="utf-8"), (ordner / "tests.py").read_text(encoding="utf-8"))
    assert "fehler" not in r, r.get("fehler")
    assert r["tests"], "keine Tests gefunden"
    durchgefallen = [t for t in r["tests"] if not t[1]]
    assert not durchgefallen, durchgefallen


@pytest.mark.parametrize("ordner", SCHRITTE, ids=lambda p: p.name)
def test_vorlage_noch_nicht_geloest(ordner):
    r = ausfuehren((ordner / "aufgabe.py").read_text(encoding="utf-8"), (ordner / "tests.py").read_text(encoding="utf-8"))
    assert "fehler" not in r, "Die Vorlage muss ohne Fehler starten: " + r.get("fehler", "")
    assert any(not t[1] for t in r["tests"]), "Die Vorlage besteht schon alle Tests"
