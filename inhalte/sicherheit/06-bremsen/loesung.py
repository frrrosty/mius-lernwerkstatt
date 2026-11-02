class Bremse:
    def __init__(self, hoechstens: int, sekunden: float):
        self.hoechstens = hoechstens
        self.sekunden = sekunden
        self.zeiten: dict[str, list[float]] = {}

    def erlaubt(self, kennung: str, jetzt: float) -> bool:
        grenze = jetzt - self.sekunden
        # Nur behalten, was noch im Fenster liegt. Das räumt nebenbei auf,
        # sonst wüchse die Liste mit jeder Kennung unbegrenzt (Speicher!).
        frisch = [t for t in self.zeiten.get(kennung, []) if t > grenze]
        if len(frisch) >= self.hoechstens:
            self.zeiten[kennung] = frisch
            return False
        frisch.append(jetzt)
        self.zeiten[kennung] = frisch
        return True

# Auf einem Server läuft jede Anfrage in einem eigenen PHP-Prozess. Ein
# Wörterbuch im Speicher wäre nach jeder Anfrage weg. Darum speichert
# Mius\gedrosselt() die Zeitpunkte in SQLite. Gleiche Idee, anderer Ort.
