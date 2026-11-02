import hashlib
import hmac
import secrets

RUNDEN = 1_000


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
    salz = secrets.token_bytes(16)
    h = pbkdf2_sha256(passwort.encode("utf-8"), salz, RUNDEN)
    return f"pbkdf2${RUNDEN}${salz.hex()}${h.hex()}"


def passwort_pruefen(passwort: str, gespeichert: str) -> bool:
    try:
        art, runden, salz_hex, hash_hex = gespeichert.split("$")
    except ValueError:
        return False
    if art != "pbkdf2":
        return False
    neu = pbkdf2_sha256(passwort.encode("utf-8"), bytes.fromhex(salz_hex), int(runden))
    return hmac.compare_digest(neu, bytes.fromhex(hash_hex))

# Warum die Runden im Text stehen: Rechner werden schneller, also erhöht man die
# Runden mit der Zeit. Alte Hashes müssen aber prüfbar bleiben. Beim nächsten
# erfolgreichen Login kann man sie mit den neuen Runden neu speichern
# («Rehashing»). PHPs password_hash() und Argon2 machen es genauso: Verfahren
# und Parameter stehen vorn im gespeicherten Text.
