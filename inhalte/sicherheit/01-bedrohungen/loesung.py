STRIDE = "STRIDE"


def risiko(b: dict) -> int:
    w, s = b["wahrscheinlichkeit"], b["schaden"]
    if not (1 <= w <= 5 and 1 <= s <= 5):
        raise ValueError("Wahrscheinlichkeit und Schaden liegen zwischen 1 und 5.")
    return w * s


def wichtigste(bedrohungen: list[dict], n: int) -> list[str]:
    # sorted mit einem Tupel als Schlüssel: erst nach Risiko, dann nach Schaden.
    # reverse=True, weil das Höchste zuerst kommen soll.
    sortiert = sorted(bedrohungen, key=lambda b: (risiko(b), b["schaden"]), reverse=True)
    return [b["name"] for b in sortiert[:n]]


def luecken(bedrohungen: list[dict]) -> list[str]:
    vorhanden = {b["art"] for b in bedrohungen}   # eine Menge: jeder Buchstabe einmal
    return [a for a in STRIDE if a not in vorhanden]
