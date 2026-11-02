from pathlib import Path


def sicherer_pfad(basis: str, name: str) -> Path:
    wurzel = Path(basis).resolve()
    ziel = (wurzel / name).resolve()
    # is_relative_to vergleicht Pfadteile, nicht Text: /a/b-geheim liegt nicht in /a/b.
    if not ziel.is_relative_to(wurzel):
        raise ValueError(f"{name!r} liegt ausserhalb des erlaubten Ordners.")
    return ziel
