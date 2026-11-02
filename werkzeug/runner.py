"""Führt eine Übung aus: deinen Code als Modul «aufgabe», dann die Tests dazu.

Dieselbe Datei läuft an zwei Orten:
- im Browser, in Pyodide (Python als WebAssembly), über web/rechner.js,
- auf deinem Rechner, über pruefen.py und in der CI über tests/.

Warum kein pytest im Browser? pytest ist gross und braucht Zusatzpakete.
Für unsere Tests reicht das, was pytest im Kern tut: Funktionen, die mit
«test_» beginnen, aufrufen und AssertionError als «nicht bestanden» werten.
"""
import contextlib
import io
import sys
import traceback
import types


def ausfuehren(code: str, tests: str) -> dict:
    """Gibt {"tests": [[beschreibung, bestanden, meldung], ...], "ausgabe": str}
    oder {"fehler": str, "ausgabe": str} zurück, wenn dein Code nicht startet."""
    ausgabe = io.StringIO()
    modul = types.ModuleType("aufgabe")
    try:
        with contextlib.redirect_stdout(ausgabe):
            exec(compile(code, "aufgabe.py", "exec"), modul.__dict__)
    except Exception:
        # Nur die letzte Zeile des Tracebacks: Datei, Zeile, Fehlerart
        return {"fehler": _kurz(traceback.format_exc()), "ausgabe": ausgabe.getvalue()}
    sys.modules["aufgabe"] = modul

    namensraum: dict = {}
    exec(compile(tests, "tests.py", "exec"), namensraum)
    ergebnisse = []
    for name, funktion in list(namensraum.items()):
        if not (name.startswith("test_") and callable(funktion)):
            continue
        beschreibung = (funktion.__doc__ or name).strip()
        try:
            with contextlib.redirect_stdout(ausgabe):
                funktion()
            ergebnisse.append([beschreibung, True, ""])
        except AssertionError as e:
            ergebnisse.append([beschreibung, False, str(e) or "Die Erwartung ist nicht erfüllt."])
        except NotImplementedError:
            ergebnisse.append([beschreibung, False, "Noch nicht umgesetzt."])
        except Exception as e:
            ergebnisse.append([beschreibung, False, f"{type(e).__name__}: {e}"])
    sys.modules.pop("aufgabe", None)
    return {"tests": ergebnisse, "ausgabe": ausgabe.getvalue()}


def _kurz(tb: str) -> str:
    zeilen = [z for z in tb.strip().splitlines() if z.strip()]
    # Zeile im eigenen Code suchen, damit klar ist, wo es klemmt
    ort = next((z.strip() for z in reversed(zeilen) if 'File "aufgabe.py"' in z), "")
    return (ort + "\n" if ort else "") + zeilen[-1]
