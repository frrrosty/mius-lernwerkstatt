from aufgabe import *


def test_bis_zur_grenze():
    """Bis zur Grenze ist alles erlaubt, danach nicht mehr"""
    b = Bremse(3, 60)
    assert [b.erlaubt("ip-1", t) for t in (0, 1, 2, 3)] == [True, True, True, False]


def test_kennungen_getrennt():
    """Jede Kennung hat ihr eigenes Kontingent"""
    b = Bremse(1, 60)
    assert b.erlaubt("anna", 0) and b.erlaubt("ben", 0)
    assert not b.erlaubt("anna", 1)


def test_gleitendes_fenster():
    """Nach Ablauf des Fensters ist wieder Platz"""
    b = Bremse(2, 60)
    b.erlaubt("x", 0)
    b.erlaubt("x", 30)
    assert not b.erlaubt("x", 59), "Bei 59 s liegen beide Versuche noch im Fenster."
    assert b.erlaubt("x", 60), "Bei 60 s ist der Versuch von 0 s abgelaufen."
    assert not b.erlaubt("x", 61), "Bei 61 s liegen 30 s und 60 s im Fenster."


def test_keine_fenstergrenze():
    """Das Fenster gleitet: an einer festen Grenze lässt sich nicht doppelt zählen"""
    b = Bremse(5, 900)
    erlaubt = sum(b.erlaubt("ip", t) for t in [899, 899, 899, 899, 899, 901, 901, 901, 901, 901])
    assert erlaubt == 5, f"{erlaubt} statt 5 Versuche durchgelassen."


def test_abgelehnte_zaehlen_nicht():
    """Abgelehnte Versuche verlängern die Sperre nicht"""
    b = Bremse(1, 10)
    b.erlaubt("x", 0)
    for t in range(1, 10):
        b.erlaubt("x", t)
    assert b.erlaubt("x", 10), "Abgelehnte Versuche wurden mitgezählt."
