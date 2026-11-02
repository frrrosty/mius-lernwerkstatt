# Passwörter speichern und prüfen, mit PBKDF2.
# (Argon2 bräuchte ein Zusatzpaket; das Prinzip ist dasselbe.)
#
# 1. passwort_speichern(passwort) gibt einen Text zurück, der alles enthält,
#    was man später zum Prüfen braucht, getrennt durch «$»:
#       "pbkdf2$<runden>$<salz als hex>$<hash als hex>"
#    - Das Salz: 16 zufällige Bytes, mit secrets.token_bytes(16)
#    - Der Hash: pbkdf2_sha256(passwort als Bytes, salz, RUNDEN), siehe unten
#    - Text in Bytes: passwort.encode("utf-8")
#    - Bytes in hex: .hex()   hex in Bytes: bytes.fromhex(text)
#
# 2. passwort_pruefen(passwort, gespeichert) gibt True oder False zurück.
#    Lies Runden und Salz aus dem gespeicherten Text, rechne neu und vergleiche
#    mit hmac.compare_digest, nicht mit ==.
#
# Warum stehen die Runden im gespeicherten Text? Überleg es dir, bevor du
# den Hinweis in der Lösung liest.

import hashlib
import hmac
import secrets

RUNDEN = 1_000   # Für die Übung tief, weil reines Python langsam ist. OWASP empfiehlt 600 000.

def pbkdf2_sha256(passwort: bytes, salz: bytes, runden: int) -> bytes:
    """PBKDF2 nach RFC 8018 mit HMAC-SHA256, 32 Bytes Ergebnis.

    Fertig, du musst hier nichts ändern. Lies sie aber: Das ist alles, was
    «absichtlich langsam» heisst. Ein HMAC, dann runden-1 weitere, jedes Mal
    mit dem vorigen Ergebnis, und alle per XOR übereinandergelegt.
    (hashlib.pbkdf2_hmac macht dasselbe in C, fehlt aber im Browser-Python.)
    """
    u = hmac.new(passwort, salz + b"\x00\x00\x00\x01", hashlib.sha256).digest()
    ergebnis = int.from_bytes(u, "big")
    for _ in range(runden - 1):
        u = hmac.new(passwort, u, hashlib.sha256).digest()
        ergebnis ^= int.from_bytes(u, "big")
    return ergebnis.to_bytes(32, "big")



def passwort_speichern(passwort: str) -> str:
    raise NotImplementedError


def passwort_pruefen(passwort: str, gespeichert: str) -> bool:
    raise NotImplementedError
