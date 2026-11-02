from aufgabe import *

# Schein-Geheimnisse werden hier zusammengesetzt, damit dieses Repo selbst
# keinen Treffer für GitHub Secret Scanning enthält.
_GHP = "gh" + "p_"
_BEGIN = "-----BEGIN " + "OPENSSH PRIVATE KEY-----"
_END = "-----END " + "OPENSSH PRIVATE KEY-----"

KONFIG = '''# Beispielkonfiguration
DB_HOST = "localhost"
DB_PASS = os.environ["DB_PASS"]
password = ""
api_key: "sk-3f9a8b7c6d5e4f3a"
SECRET = 'kurz'
'''


def test_privater_schluessel():
    """Ein privater Schlüssel wird erkannt"""
    text = "x\n" + _BEGIN + "\nAAAAschein\n" + _END + "\n"
    assert finde_geheimnisse(text) == [(2, "privater-schluessel")]


def test_github_token():
    """Ein GitHub-Token wird erkannt"""
    assert finde_geheimnisse("token = " + _GHP + "a1B2c3D4e5" * 4) == [(1, "github-token")]


def test_kurzes_ghp_ist_kein_token():
    """«ghp_» mit zu wenigen Zeichen ist kein Token"""
    assert finde_geheimnisse("# siehe " + _GHP + "abc") == []


def test_zuweisungen():
    """Zuweisungen mit echtem Wert werden erkannt, leere, kurze und Umgebungsvariablen nicht"""
    assert finde_geheimnisse(KONFIG) == [(5, "zuweisung")]


def test_gross_klein():
    """Gross- und Kleinschreibung spielt keine Rolle"""
    assert finde_geheimnisse('PassWort = "Untersee2026"') == [(1, "zuweisung")]


def test_ein_fund_pro_zeile():
    """Pro Zeile höchstens ein Fund"""
    zeile = 'api_key = "' + _GHP + "x" * 40 + '"'
    assert len(finde_geheimnisse(zeile)) == 1


def test_sauberer_text():
    """Ein Text ohne Geheimnisse ergibt eine leere Liste"""
    assert finde_geheimnisse("def anmelden(passwort):\n    return pruefen(passwort)\n") == []
