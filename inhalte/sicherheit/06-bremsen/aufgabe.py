# Eine Bremse mit gleitendem Zeitfenster, wie Mius\gedrosselt() auf mius.ch.
#
# Bremse(hoechstens, sekunden) erlaubt pro Kennung höchstens «hoechstens»
# Ereignisse in den letzten «sekunden» Sekunden.
#
# erlaubt(kennung, jetzt) gibt True zurück und merkt sich den Zeitpunkt,
# wenn noch Platz ist. Sonst False, und der Versuch zählt NICHT mit.
# jetzt ist eine Zahl in Sekunden. (Wir übergeben die Zeit, statt time.time()
# zu lesen. So lässt sich die Bremse testen, ohne zu warten.)
#
# Ein Ereignis genau «sekunden» Sekunden in der Vergangenheit zählt nicht mehr.
#
# Tipp: ein Wörterbuch Kennung -> Liste von Zeitpunkten.


class Bremse:
    def __init__(self, hoechstens: int, sekunden: float):
        self.hoechstens = hoechstens
        self.sekunden = sekunden

    def erlaubt(self, kennung: str, jetzt: float) -> bool:
        raise NotImplementedError
