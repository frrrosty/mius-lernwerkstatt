# Maskieren für HTML, wie esc() in faden.js auf mius.ch.
#
# 1. maskiere(text) ersetzt
#       &  durch  &amp;
#       <  durch  &lt;
#       >  durch  &gt;
#       "  durch  &quot;
#       '  durch  &#39;
#    Achte auf die Reihenfolge.
#
# 2. karte(titel, link) baut daraus ein Stück HTML:
#       <a class="karte" href="LINK">TITEL</a>
#    Titel und Link werden maskiert.
#    Zusätzlich: Ein Link, der nicht mit «https://» oder «/» beginnt, wird durch
#    «#» ersetzt. Warum? Probier «javascript:alert(1)» als Link.

def maskiere(text: str) -> str:
    raise NotImplementedError


def karte(titel: str, link: str) -> str:
    raise NotImplementedError
