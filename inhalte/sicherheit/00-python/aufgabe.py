# Zähle, wie oft jede Antwort vorkommt.
#
# antworten ist eine Liste von Texten, zum Beispiel
#   ["Lehrperson", "ICT", "Lehrperson"]
# Zurück kommt ein Wörterbuch Antwort -> Anzahl:
#   {"Lehrperson": 2, "ICT": 1}
#
# Danach: haeufigste() gibt die Antwort zurück, die am häufigsten vorkommt.
# Bei einer leeren Liste gibt sie None zurück.


def zaehle(antworten: list[str]) -> dict[str, int]:
    raise NotImplementedError


def haeufigste(antworten: list[str]) -> str | None:
    raise NotImplementedError
