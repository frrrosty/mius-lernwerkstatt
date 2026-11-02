# Ein kleines Bedrohungsmodell als Daten.
#
# Jede Bedrohung ist ein Wörterbuch:
#   {"name": "Fremde QR-Karte", "art": "S", "wahrscheinlichkeit": 3, "schaden": 2}
# art ist ein Buchstabe aus STRIDE: S, T, R, I, D oder E.
#
# 1. risiko(b) gibt wahrscheinlichkeit × schaden zurück.
#    Liegt einer der beiden Werte nicht zwischen 1 und 5, wirf einen ValueError.
#
# 2. wichtigste(bedrohungen, n) gibt die Namen der n Bedrohungen mit dem
#    höchsten Risiko zurück, das höchste zuerst. Bei gleichem Risiko zählt der
#    höhere Schaden. (Ein grosser Schaden wiegt schwerer als eine hohe
#    Wahrscheinlichkeit, findest du nicht?)
#
# 3. luecken(bedrohungen) gibt die STRIDE-Buchstaben zurück, zu denen noch keine
#    Bedrohung erfasst ist, in der Reihenfolge S, T, R, I, D, E.

STRIDE = "STRIDE"


def risiko(b: dict) -> int:
    raise NotImplementedError


def wichtigste(bedrohungen: list[dict], n: int) -> list[str]:
    raise NotImplementedError


def luecken(bedrohungen: list[dict]) -> list[str]:
    raise NotImplementedError
