# Ein Prüfer für GitHub-Workflows: Sind alle Actions auf einen Commit festgelegt?
#
# pruefe_workflow(text) liest einen Workflow (YAML als Text) Zeile für Zeile
# und gibt eine Liste von Wörterbüchern zurück, eines pro «uses:»-Zeile:
#   {"zeile": 12, "aktion": "actions/checkout", "ref": "v4", "fest": False}
#
# - zeile: Zeilennummer ab 1
# - aktion: alles vor dem @
# - ref: alles nach dem @, ohne Kommentar (# ...) und ohne Leerzeichen
# - fest: True, wenn ref genau 40 Hexadezimalzeichen sind (0-9, a-f)
#
# «uses:» kann eingerückt sein und mit «- » beginnen.
# Lokale Actions («uses: ./eigene-aktion») und Docker («uses: docker://...»)
# lässt du weg, die haben kein @ im üblichen Sinn.
#
# riskant(text) gibt nur die Namen der Actions zurück, die nicht fest sind,
# ohne Doppelte, in der Reihenfolge ihres ersten Auftretens.

import re


def pruefe_workflow(text: str) -> list[dict]:
    raise NotImplementedError


def riskant(text: str) -> list[str]:
    raise NotImplementedError
