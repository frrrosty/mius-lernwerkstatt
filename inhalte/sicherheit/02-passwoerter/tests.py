from aufgabe import *
import hmac as _hmac


def test_format():
    """passwort_speichern() liefert «pbkdf2$runden$salz$hash»"""
    teile = passwort_speichern("Untersee-2026").split("$")
    assert len(teile) == 4 and teile[0] == "pbkdf2", f"Erwartet vier Teile mit «pbkdf2» vorn, erhalten: {teile[:2]}"
    assert int(teile[1]) >= 1_000, "Zu wenige Runden."
    assert len(bytes.fromhex(teile[2])) == 16, "Das Salz soll 16 Bytes lang sein."
    assert len(bytes.fromhex(teile[3])) == 32, "SHA-256 ergibt 32 Bytes."


def test_passwort_nicht_im_klartext():
    """Das Passwort steht nirgends im gespeicherten Text"""
    assert "Untersee" not in passwort_speichern("Untersee-2026")


def test_salz_ist_zufaellig():
    """Gleiches Passwort, zweimal gespeichert, ergibt verschiedene Texte"""
    assert passwort_speichern("gleich") != passwort_speichern("gleich"), "Ohne zufälliges Salz sind gleiche Passwörter erkennbar."


def test_richtiges_passwort():
    """passwort_pruefen() erkennt das richtige Passwort"""
    assert passwort_pruefen("Blaue Stunde", passwort_speichern("Blaue Stunde")) is True


def test_falsches_passwort():
    """passwort_pruefen() weist ein falsches Passwort ab"""
    assert passwort_pruefen("blaue stunde", passwort_speichern("Blaue Stunde")) is False


def test_liest_runden_aus_dem_text():
    """passwort_pruefen() nutzt die Runden aus dem gespeicherten Text, nicht die Konstante"""
    salz = bytes(16)
    alt = "pbkdf2$500$" + salz.hex() + "$" + pbkdf2_sha256(b"alt", salz, 500).hex()
    assert passwort_pruefen("alt", alt) is True, "Ein älterer Hash mit 500 Runden muss weiterhin prüfbar sein."


def test_hilfsfunktion_unveraendert():
    """pbkdf2_sha256 liefert den Wert aus dem Standard (RFC 7914, Testvektor)"""
    # Testvektor aus RFC 7914, Abschnitt 11: PBKDF2-HMAC-SHA256, 1 Runde
    erwartet = "55ac046e56e3089fec1691c22544b605f94185216dde0465e68b9d57c20dacbc"
    assert pbkdf2_sha256(b"passwd", b"salt", 1).hex() == erwartet, "Die Hilfsfunktion wurde verändert."


def test_vergleich_in_konstanter_zeit():
    """passwort_pruefen() vergleicht mit hmac.compare_digest"""
    aufgerufen = []
    original = _hmac.compare_digest

    def spion(a, b):
        aufgerufen.append(True)
        return original(a, b)

    _hmac.compare_digest = spion
    try:
        passwort_pruefen("x", passwort_speichern("x"))
    finally:
        _hmac.compare_digest = original
    assert aufgerufen, "hmac.compare_digest wurde nicht verwendet."
