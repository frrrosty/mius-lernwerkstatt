from aufgabe import *


def test_zaehlt_einfach():
    """zaehle() zählt jede Antwort"""
    assert zaehle(["Lehrperson", "ICT", "Lehrperson"]) == {"Lehrperson": 2, "ICT": 1}


def test_leer():
    """zaehle() gibt bei einer leeren Liste ein leeres Wörterbuch zurück"""
    assert zaehle([]) == {}


def test_veraendert_eingabe_nicht():
    """zaehle() verändert die übergebene Liste nicht"""
    liste = ["a", "b", "a"]
    zaehle(liste)
    assert liste == ["a", "b", "a"], "Die Liste wurde verändert."


def test_haeufigste():
    """haeufigste() findet die häufigste Antwort"""
    assert haeufigste(["ab und zu", "täglich", "täglich", "gar nicht"]) == "täglich"


def test_haeufigste_leer():
    """haeufigste() gibt bei einer leeren Liste None zurück"""
    assert haeufigste([]) is None
