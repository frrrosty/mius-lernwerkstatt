def zaehle(antworten: list[str]) -> dict[str, int]:
    anzahl: dict[str, int] = {}
    for a in antworten:
        anzahl[a] = anzahl.get(a, 0) + 1
    return anzahl
    # Kürzer, mit der Standardbibliothek: return dict(collections.Counter(antworten))


def haeufigste(antworten: list[str]) -> str | None:
    anzahl = zaehle(antworten)
    if not anzahl:
        return None
    return max(anzahl, key=anzahl.get)
