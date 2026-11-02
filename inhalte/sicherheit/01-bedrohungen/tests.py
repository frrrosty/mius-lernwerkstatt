from aufgabe import *

MODELL = [
    {"name": "Fremde QR-Karte", "art": "S", "wahrscheinlichkeit": 3, "schaden": 2},
    {"name": "Klarnamen auf dem Server", "art": "I", "wahrscheinlichkeit": 2, "schaden": 5},
    {"name": "Formular fluten", "art": "D", "wahrscheinlichkeit": 4, "schaden": 2},
    {"name": "Antwort nachträglich ändern", "art": "T", "wahrscheinlichkeit": 2, "schaden": 4},
]


def test_risiko():
    """risiko() multipliziert Wahrscheinlichkeit und Schaden"""
    assert risiko(MODELL[1]) == 10


def test_risiko_prueft_skala():
    """risiko() lehnt Werte ausserhalb von 1 bis 5 ab"""
    for falsch in (0, 6, -1):
        try:
            risiko({"name": "x", "art": "S", "wahrscheinlichkeit": falsch, "schaden": 3})
        except ValueError:
            continue
        assert False, f"Wahrscheinlichkeit {falsch} hätte einen ValueError geben müssen."


def test_wichtigste_reihenfolge():
    """wichtigste() sortiert nach Risiko, bei Gleichstand nach Schaden"""
    # Klarnamen 10 (Schaden 5), Fluten 8 (Schaden 2), Ändern 8 (Schaden 4), QR 6
    assert wichtigste(MODELL, 3) == ["Klarnamen auf dem Server", "Antwort nachträglich ändern", "Formular fluten"]


def test_wichtigste_mehr_als_vorhanden():
    """wichtigste() gibt höchstens so viele zurück, wie es gibt"""
    assert len(wichtigste(MODELL, 10)) == 4


def test_luecken():
    """luecken() findet die STRIDE-Arten ohne Bedrohung, in fester Reihenfolge"""
    assert luecken(MODELL) == ["R", "E"]


def test_luecken_leer():
    """luecken() meldet bei einem leeren Modell alle sechs Arten"""
    assert luecken([]) == list("STRIDE")
