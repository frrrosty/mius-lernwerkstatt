import re

# Reihenfolge = Vorrang: der spezifischste Befund zuerst
MUSTER = [
    ("privater-schluessel", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("github-token", re.compile(r"ghp_[A-Za-z0-9]{36,}")),
    # (?:...) gruppiert ohne zu merken; ["'] ist ein Anführungszeichen;
    # [^"']{8,} sind mindestens 8 Zeichen, die kein Anführungszeichen sind.
    ("zuweisung", re.compile(r"(password|passwort|secret|api_key)\s*[=:]\s*[\"'][^\"']{8,}[\"']", re.IGNORECASE)),
]


def finde_geheimnisse(text: str) -> list[tuple[int, str]]:
    funde = []
    for nr, zeile in enumerate(text.splitlines(), start=1):
        for art, muster in MUSTER:
            if muster.search(zeile):
                funde.append((nr, art))
                break   # ein Fund pro Zeile
    return funde
