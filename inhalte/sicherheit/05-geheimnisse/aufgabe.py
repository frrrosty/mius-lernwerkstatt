# Ein einfacher Geheimnis-Scanner, wie GitHub Secret Scanning im Kleinen.
#
# finde_geheimnisse(text) gibt eine Liste von (zeilennummer, art) zurück,
# Zeilen gezählt ab 1, in der Reihenfolge des Textes. Höchstens ein Fund pro Zeile.
#
# Erkennen sollst du diese Arten (art):
#   "privater-schluessel"  eine Zeile mit «-----BEGIN» und «PRIVATE KEY-----»
#   "github-token"         «ghp_» gefolgt von mindestens 36 Buchstaben oder Ziffern
#   "zuweisung"            password, passwort, secret oder api_key (gross/klein egal),
#                          dann = oder :, dann ein Wert in Anführungszeichen,
#                          der mindestens 8 Zeichen lang ist
#
# Keine Fehlalarme bei:
#   password = ""               (leer)
#   password = os.environ["DB_PASS"]   (aus der Umgebung gelesen, gut so)
#
# Werkzeug: das Modul re (reguläre Ausdrücke). re.search(muster, zeile, re.IGNORECASE)

import re


def finde_geheimnisse(text: str) -> list[tuple[int, str]]:
    raise NotImplementedError
