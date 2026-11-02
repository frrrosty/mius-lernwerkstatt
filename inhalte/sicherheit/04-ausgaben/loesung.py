ERSETZEN = [("&", "&amp;"), ("<", "&lt;"), (">", "&gt;"), ('"', "&quot;"), ("'", "&#39;")]


def maskiere(text: str) -> str:
    for zeichen, ersatz in ERSETZEN:   # & steht vorn in der Liste
        text = text.replace(zeichen, ersatz)
    return text


def karte(titel: str, link: str) -> str:
    # Erlaubnisliste statt Verbotsliste: nur https und Pfade auf der eigenen Seite.
    # «javascript:», «data:» und Schreibweisen mit Leerzeichen oder Grossbuchstaben fallen so alle raus.
    if not (link.startswith("https://") or link.startswith("/")):
        link = "#"
    return f'<a class="karte" href="{maskiere(link)}">{maskiere(titel)}</a>'
