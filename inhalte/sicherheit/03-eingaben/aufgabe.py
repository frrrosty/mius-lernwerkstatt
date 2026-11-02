# Pfade prüfen wie im noScribe-Editor.
#
# sicherer_pfad(basis, name) bekommt einen erlaubten Ordner und einen
# Dateinamen aus einer Anfrage. Sie gibt den vollständigen Pfad zurück,
# wenn er innerhalb von basis liegt. Sonst wirft sie einen ValueError.
#
# Hilfreich aus pathlib:
#   Path(basis) / name        setzt Pfade zusammen
#   .resolve()                löst «..» und Verknüpfungen auf, ergibt einen absoluten Pfad
#   p.is_relative_to(b)       ist p innerhalb von b?
#
# Repariere nichts. Entweder der Pfad ist in Ordnung, oder er wird abgelehnt.

from pathlib import Path


def sicherer_pfad(basis: str, name: str) -> Path:
    raise NotImplementedError
