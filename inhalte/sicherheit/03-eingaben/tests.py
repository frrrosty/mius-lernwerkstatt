from aufgabe import *
import os as _os
import tempfile as _tempfile

_BASIS = _tempfile.mkdtemp(prefix="interviews-")
_os.makedirs(_os.path.join(_BASIS, "2026"), exist_ok=True)


def _abgelehnt(name):
    try:
        sicherer_pfad(_BASIS, name)
    except ValueError:
        return True
    return False


def test_normaler_name():
    """Ein gewöhnlicher Dateiname ist erlaubt"""
    p = sicherer_pfad(_BASIS, "rotach.docx")
    assert str(p).endswith("rotach.docx") and str(p).startswith(str(Path(_BASIS).resolve()))


def test_unterordner():
    """Ein Unterordner ist erlaubt"""
    assert str(sicherer_pfad(_BASIS, "2026/rotach.docx")).endswith(_os.path.join("2026", "rotach.docx"))


def test_punkt_punkt():
    """«../» aus dem Ordner hinaus wird abgelehnt"""
    assert _abgelehnt("../konfig.php"), "../konfig.php wurde durchgelassen."


def test_tief_verschachtelt():
    """Auch «2026/../../» wird abgelehnt"""
    assert _abgelehnt("2026/../../konfig.php")


def test_absoluter_pfad():
    """Ein absoluter Pfad wird abgelehnt"""
    assert _abgelehnt("/etc/passwd"), "Path(basis) / '/etc/passwd' ergibt '/etc/passwd'. Genau deshalb prüfen."


def test_innen_hin_und_zurueck():
    """«2026/../a.txt» bleibt im Ordner und ist erlaubt"""
    assert not _abgelehnt("2026/../a.txt")


def test_aehnlicher_ordnername():
    """Ein Nachbarordner mit gleichem Anfang wird abgelehnt"""
    # /tmp/interviews-abc und /tmp/interviews-abc-geheim: Ein Vergleich mit
    # startswith() auf Text würde den zweiten durchlassen.
    nachbar = Path(_BASIS).name + "-geheim"
    assert _abgelehnt("../" + nachbar + "/x.txt"), "Ein Textvergleich mit startswith() reicht nicht."
