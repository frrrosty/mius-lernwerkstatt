import re

# ^\s*        beliebig eingerückt
# (?:-\s*)?   optional ein Listenstrich
# uses:\s*    das Schlüsselwort
# ([^@\s]+)   die Aktion: alles bis zum @
# @([^\s#]+)  der Ref: alles bis zum Leerzeichen oder Kommentar
USES = re.compile(r"^\s*(?:-\s*)?uses:\s*([^@\s]+)@([^\s#]+)")
HASH = re.compile(r"[0-9a-f]{40}")


def pruefe_workflow(text: str) -> list[dict]:
    ergebnis = []
    for nr, zeile in enumerate(text.splitlines(), start=1):
        m = USES.match(zeile)
        if not m:
            continue
        aktion, ref = m.group(1), m.group(2)
        if aktion.startswith(("./", "docker://")):
            continue
        ergebnis.append({"zeile": nr, "aktion": aktion, "ref": ref, "fest": bool(HASH.fullmatch(ref))})
    return ergebnis


def riskant(text: str) -> list[str]:
    namen: list[str] = []
    for r in pruefe_workflow(text):
        if not r["fest"] and r["aktion"] not in namen:
            namen.append(r["aktion"])
    return namen

# Hinweis: docker://alpine:3.20@sha256:... wäre die festgelegte Form für Container.
# Die Regel oben lässt Docker bewusst weg; ein echter Prüfer würde sie auch ansehen.
