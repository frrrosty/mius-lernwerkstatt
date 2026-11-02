from aufgabe import *
import html as _html


def test_spitze_klammern():
    """< und > werden maskiert"""
    assert maskiere("<script>") == "&lt;script&gt;"


def test_kaufmanns_und_zuerst():
    """& wird zuerst ersetzt, sonst entsteht &amp;lt;"""
    assert maskiere("<") == "&lt;", f"Erhalten: {maskiere('<')}"
    assert maskiere("A & B") == "A &amp; B"


def test_anfuehrungszeichen():
    """Doppelte und einfache Anführungszeichen werden maskiert"""
    assert maskiere('"\'') == "&quot;&#39;"


def test_wie_die_standardbibliothek():
    """Das Ergebnis entspricht html.escape aus der Standardbibliothek"""
    probe = """<img src=x onerror="alert('hi')"> & Co."""
    assert maskiere(probe) == _html.escape(probe, quote=True).replace("&#x27;", "&#39;")


def test_karte_maskiert_titel():
    """karte() maskiert den Titel"""
    assert karte("<b>Fett</b>", "/notiz/1") == '<a class="karte" href="/notiz/1">&lt;b&gt;Fett&lt;/b&gt;</a>'


def test_karte_attribut_ausbruch():
    """karte() verhindert den Ausbruch aus dem href-Attribut"""
    h = karte("x", '/a" onmouseover="alert(1)')
    assert 'onmouseover="' not in h, "Mit einem \" im Link lässt sich ein neues Attribut einschleusen."


def test_karte_javascript_link():
    """karte() ersetzt javascript:-Links durch #"""
    assert 'href="#"' in karte("Klick", "javascript:alert(1)")
    assert 'href="#"' in karte("Klick", " JavaScript:alert(1)")


def test_karte_https_bleibt():
    """karte() lässt https-Links stehen"""
    assert 'href="https://mius.ch/"' in karte("MIUS", "https://mius.ch/")
