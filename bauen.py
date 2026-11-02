#!/usr/bin/env python3
"""Baut die Lernwerkstatt als statische Seite nach dist/.

  python bauen.py                  alles, inklusive Python für den Browser
  python bauen.py --ohne-python    ohne Pyodide (schneller, für Tests der Seite)

Was passiert:
1. Jeder Schritt unter inhalte/sicherheit/ wird zu einer HTML-Seite:
   Text aus schritt.md, Übung aus aufgabe.py, tests.py und loesung.py.
2. Die Weboberfläche aus web/ wird kopiert.
3. Pyodide (Python als WebAssembly) wird aus npm geholt und gegen die
   veröffentlichte SHA-512-Prüfsumme geprüft. Stimmt sie nicht, bricht der Bau ab.
   So läuft Python von unserem eigenen Server, nicht von einem fremden CDN.
"""
import argparse
import base64
import hashlib
import html
import io
import json
import re
import shutil
import sys
import tarfile
import urllib.request
from pathlib import Path

import markdown

WURZEL = Path(__file__).resolve().parent
INHALTE = WURZEL / "inhalte" / "sicherheit"
WEB = WURZEL / "web"
ZIEL = WURZEL / "dist"
ZWISCHENSPEICHER = WURZEL / ".cache"

# Pyodide: Version und Prüfsumme aus «npm view pyodide@0.26.4 dist.integrity».
# Bei einem Update beide Werte zusammen ändern, nie nur die Version.
PYODIDE_VERSION = "0.26.4"
PYODIDE_URL = f"https://registry.npmjs.org/pyodide/-/pyodide-{PYODIDE_VERSION}.tgz"
PYODIDE_SHA512 = "z2CHsjVlhhJi5tYBF0AYAfNEPo3zq/z+xOpFtk1tweJkRaTqU4UK/7pLvo8DBU2VDPH31vB3pSI+8fnoqrVrFg=="
PYODIDE_DATEIEN = ["pyodide.js", "pyodide.asm.js", "pyodide.asm.wasm", "python_stdlib.zip", "pyodide-lock.json"]

ABSCHNITTE = ("Karten", "Prompt", "Literatur")


# ---------------------------------------------------------------- Inhalte lesen

def kopf_lesen(text: str) -> tuple[dict, str]:
    """Liest den Kopf zwischen den beiden «---» (einfaches «schluessel: wert»)."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise SystemExit("schritt.md braucht einen Kopf zwischen --- und ---")
    kopf = {}
    for zeile in m.group(1).splitlines():
        k, _, v = zeile.partition(":")
        kopf[k.strip()] = v.strip()
    return kopf, text[m.end():]


def abschnitte(text: str) -> dict[str, str]:
    """Trennt den Lerntext von den Abschnitten Karten, Prompt, Literatur."""
    teile = re.split(r"^## (" + "|".join(ABSCHNITTE) + r")\s*$", text, flags=re.M)
    ergebnis = {"Text": teile[0]}
    for i in range(1, len(teile), 2):
        ergebnis[teile[i]] = teile[i + 1].strip()
    return ergebnis


def karten_lesen(text: str) -> list[dict]:
    karten = []
    for block in re.split(r"\n\s*\n", text.strip()):
        f = re.search(r"^F:\s*(.+)$", block, re.M)
        a = re.search(r"^A:\s*(.+)$", block, re.M | re.S)
        if f and a:
            karten.append({"f": md_zeile(f.group(1).strip()), "a": md_zeile(a.group(1).strip())})
    return karten


def md(text: str) -> str:
    return markdown.markdown(text, extensions=["fenced_code", "tables"])


def md_zeile(text: str) -> str:
    """Markdown für eine Zeile (Code, Fett), ohne umschliessendes <p>."""
    h = md(text)
    return h[3:-4] if h.startswith("<p>") and h.endswith("</p>") else h


def schritte_lesen() -> list[dict]:
    schritte = []
    for ordner in sorted(p for p in INHALTE.iterdir() if (p / "schritt.md").exists()):
        kopf, rumpf = kopf_lesen((ordner / "schritt.md").read_text(encoding="utf-8"))
        teile = abschnitte(rumpf)
        prompt = re.search(r"```\n?(.*?)```", teile.get("Prompt", ""), re.S)
        einleitung_prompt = teile.get("Prompt", "").split("```")[0].strip()
        schritte.append({
            "id": ordner.name,
            "nr": ordner.name[:2],
            "titel": kopf["titel"], "kurz": kopf["kurz"], "dauer": kopf["dauer"], "projekt": kopf["projekt"],
            "text": md(teile["Text"]),
            "karten": [dict(k, id=f"{ordner.name}-{i}") for i, k in enumerate(karten_lesen(teile.get("Karten", "")))],
            "prompt_einleitung": einleitung_prompt,
            "prompt": prompt.group(1).strip() if prompt else "",
            "literatur": md(teile.get("Literatur", "")),
            "aufgabe": (ordner / "aufgabe.py").read_text(encoding="utf-8"),
            "tests": (ordner / "tests.py").read_text(encoding="utf-8"),
            "loesung": (ordner / "loesung.py").read_text(encoding="utf-8"),
        })
    return schritte


# ---------------------------------------------------------------- Seiten

def seite(titel: str, inhalt: str, tiefe: int, aktiv: str = "") -> str:
    p = "../" * tiefe
    aktuell = ' aria-current="page"'
    nav = "".join(
        f'<a href="{p}{href}"{aktuell if aktiv == key else ""}>{name}</a>'
        for key, href, name in [("start", "index.html", "Lernpfad"), ("karten", "karten.html", "Karten")])
    return f"""<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>{html.escape(titel)} · Lernwerkstatt</title>
<link rel="manifest" href="{p}manifest.webmanifest">
<link rel="icon" href="{p}icon.svg" type="image/svg+xml">
<meta name="theme-color" content="#16212B">
<link rel="stylesheet" href="{p}app.css">
</head>
<body data-wurzel="{p}">
<header class="leiste">
  <a class="marke" href="{p}index.html"><span aria-hidden="true">⌘</span> Lernwerkstatt</a>
  <nav aria-label="Hauptnavigation">{nav}</nav>
</header>
<main>
{inhalt}
</main>
<script src="{p}app.js" defer></script>
</body>
</html>
"""


def schritt_seite(s: dict, vorher: dict | None, nachher: dict | None) -> str:
    daten = json.dumps({k: s[k] for k in ("id", "aufgabe", "tests", "loesung", "karten")}, ensure_ascii=False).replace("</", "<\\/")
    karten = "".join(
        f'<li class="karte" data-karte="{k["id"]}"><button type="button" class="karte-f" aria-expanded="false">{k["f"]}</button>'
        f'<div class="karte-a" hidden><p>{k["a"]}</p></div></li>' for k in s["karten"])
    weiter = ""
    if vorher:
        weiter += f'<a class="weiter-l" href="{vorher["id"]}.html"><small>← Schritt {vorher["nr"]}</small>{html.escape(vorher["titel"])}</a>'
    if nachher:
        weiter += f'<a class="weiter-r" href="{nachher["id"]}.html"><small>Schritt {nachher["nr"]} →</small>{html.escape(nachher["titel"])}</a>'
    inhalt = f"""
<article class="schritt" data-schritt="{s['id']}">
  <header class="schritt-kopf">
    <p class="kennung">Lernpfad Sicherheit · Schritt {s['nr']} · {html.escape(s['dauer'])}</p>
    <h1>{html.escape(s['titel'])}</h1>
    <p class="vorspann">{html.escape(s['kurz'])}</p>
    <p class="projekt">Aus deinen Projekten: {html.escape(s['projekt'])}</p>
  </header>

  <section class="text">{s['text']}</section>

  <section class="uebung" aria-labelledby="ue-titel">
    <div class="ue-kopf">
      <h2 id="ue-titel">Übung</h2>
      <span class="status" data-status>offen</span>
    </div>
    <p class="ue-hinweis">Schreib deinen Code ins Feld. «Prüfen» führt ihn mit Python aus, hier auf deinem Gerät. Auf dem Rechner: <code>python pruefen.py {s['nr']}</code>.</p>
    <label class="sr" for="code">Dein Python-Code</label>
    <textarea id="code" class="editor" spellcheck="false" autocapitalize="off" autocomplete="off" wrap="off"></textarea>
    <div class="ue-knoepfe">
      <button type="button" class="knopf voll" data-pruefen>Prüfen <kbd>Strg ↵</kbd></button>
      <button type="button" class="knopf" data-zurueck>Vorlage wiederherstellen</button>
      <button type="button" class="knopf leise" data-tests-zeigen aria-expanded="false">Tests ansehen</button>
      <button type="button" class="knopf leise" data-loesung-zeigen aria-expanded="false" hidden>Musterlösung</button>
    </div>
    <div class="ergebnis" data-ergebnis aria-live="polite"></div>
    <pre class="quelltext" data-tests hidden></pre>
    <div class="loesung" data-loesung hidden><p>Vergleich mit deiner Lösung. Es gibt meist mehrere richtige Wege.</p><pre class="quelltext"></pre></div>
  </section>

  <section class="eigene-worte">
    <h2>In eigenen Worten</h2>
    <p>Erklär die wichtigste Idee dieses Schritts so, wie du sie einer Kollegin erklären würdest. Drei, vier Sätze reichen. Wird nur auf diesem Gerät gespeichert.</p>
    <label class="sr" for="worte">Deine Erklärung</label>
    <textarea id="worte" class="notiz" rows="5"></textarea>
  </section>

  <section class="karten-block">
    <h2>Karten</h2>
    <p>Tippe auf eine Frage, um die Antwort zu sehen. Unter «Karten» oben übst du alle mit Wiederholung.</p>
    <ul class="karten">{karten}</ul>
  </section>

  <section class="prompt-block">
    <h2>Prompt für Claude</h2>
    <p>{html.escape(s['prompt_einleitung'])}</p>
    <pre class="prompt">{html.escape(s['prompt'])}</pre>
    <button type="button" class="knopf" data-kopieren>Kopieren</button>
  </section>

  <section class="literatur"><h2>Literatur</h2>{s['literatur']}</section>

  <nav class="weiter" aria-label="Weitere Schritte">{weiter}</nav>
</article>
<script type="application/json" id="schritt-daten">{daten}</script>
"""
    return seite(s["titel"], inhalt, 1)


def startseite(schritte: list[dict]) -> str:
    liste = "".join(f"""
    <li><a class="pfad-schritt" href="schritt/{s['id']}.html" data-schritt="{s['id']}">
      <span class="nr">{s['nr']}</span>
      <span class="pfad-text"><strong>{html.escape(s['titel'])}</strong><small>{html.escape(s['kurz'])}</small></span>
      <span class="pfad-meta"><span class="dauer">{html.escape(s['dauer'])}</span><span class="status" data-status>offen</span></span>
    </a></li>""" for s in schritte)
    inhalt = f"""
<section class="start">
  <p class="kennung">Prototyp · Etappe 1</p>
  <h1>Sicherheit von Grund auf</h1>
  <p class="vorspann">Acht Schritte, jeder mit Text, einer Python-Übung, Karten und einem Prompt, mit dem du Claude gezielt prüfen lassen kannst. Die Beispiele stammen aus deinen eigenen Projekten.</p>
  <div class="fortschritt"><div class="balken"><i data-balken></i></div><span data-fortschritt>0 von {len(schritte)} Übungen gelöst</span></div>
</section>
<ol class="pfad">{liste}</ol>
<section class="wie">
  <h2>Wie du hier lernst</h2>
  <div class="wie-raster">
    <div><h3>Drei Minuten</h3><p>Auf dem Handy: Karten üben. Was du weisst, kommt seltener wieder, was nicht, bald.</p></div>
    <div><h3>Eine Stunde</h3><p>Am Laptop: einen Schritt lesen, die Übung lösen, in eigenen Worten erklären.</p></div>
    <div><h3>Mit Claude</h3><p>Jeder Schritt endet mit einem Prompt. Damit prüfst du deine echten Projekte, statt nur «ist das sicher?» zu fragen.</p></div>
  </div>
</section>
"""
    return seite("Sicherheit von Grund auf", inhalt, 0, "start")


def kartenseite(schritte: list[dict]) -> str:
    alle = [dict(k, schritt=s["titel"]) for s in schritte for k in s["karten"]]
    daten = json.dumps(alle, ensure_ascii=False).replace("</", "<\\/")
    inhalt = f"""
<section class="training">
  <p class="kennung">Karten · {len(alle)} insgesamt</p>
  <h1>Üben mit Wiederholung</h1>
  <p class="vorspann">Fünf Fächer. Gewusst: ein Fach weiter, die Karte kommt später wieder. Nicht gewusst: zurück ins erste Fach.</p>
  <div class="faecher" data-faecher></div>
  <div class="trainer" data-trainer>
    <p class="trainer-leer" data-leer hidden>Für heute ist alles geübt. Komm morgen wieder.</p>
    <div class="trainer-karte" data-karte hidden>
      <p class="kennung" data-herkunft></p>
      <p class="frage" data-frage></p>
      <div class="antwort" data-antwort hidden></div>
      <div class="trainer-knoepfe">
        <button type="button" class="knopf voll" data-zeigen>Antwort zeigen</button>
        <button type="button" class="knopf" data-nein hidden>Noch nicht</button>
        <button type="button" class="knopf voll" data-ja hidden>Gewusst</button>
      </div>
    </div>
  </div>
</section>
<script type="application/json" id="karten-daten">{daten}</script>
"""
    return seite("Karten", inhalt, 0, "karten")


# ---------------------------------------------------------------- Pyodide

def pyodide_holen() -> None:
    """Lädt Pyodide aus npm, prüft die Prüfsumme und packt die nötigen Dateien aus."""
    ZWISCHENSPEICHER.mkdir(exist_ok=True)
    paket = ZWISCHENSPEICHER / f"pyodide-{PYODIDE_VERSION}.tgz"
    if not paket.exists():
        print(f"Lade {PYODIDE_URL}")
        with urllib.request.urlopen(PYODIDE_URL, timeout=120) as antwort:
            paket.write_bytes(antwort.read())
    ist = base64.b64encode(hashlib.sha512(paket.read_bytes()).digest()).decode()
    if ist != PYODIDE_SHA512:
        paket.unlink()
        raise SystemExit(f"Prüfsumme von Pyodide stimmt nicht.\n  erwartet {PYODIDE_SHA512}\n  erhalten {ist}\nAbbruch.")
    ziel = ZIEL / "pyodide"
    ziel.mkdir(parents=True, exist_ok=True)
    with tarfile.open(paket) as tar:
        for name in PYODIDE_DATEIEN:
            mitglied = tar.getmember("package/" + name)
            with tar.extractfile(mitglied) as quelle:
                (ziel / name).write_bytes(quelle.read())
    print(f"Pyodide {PYODIDE_VERSION}: Prüfsumme stimmt, {len(PYODIDE_DATEIEN)} Dateien ausgepackt")


# ---------------------------------------------------------------- Hauptteil

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ohne-python", action="store_true")
    args = ap.parse_args()

    schritte = schritte_lesen()
    if ZIEL.exists():
        for kind in ZIEL.iterdir():
            if kind.name == "pyodide" and args.ohne_python:
                continue
            shutil.rmtree(kind) if kind.is_dir() else kind.unlink()
    (ZIEL / "schritt").mkdir(parents=True, exist_ok=True)

    for datei in WEB.iterdir():
        if datei.is_file():
            shutil.copy2(datei, ZIEL / datei.name)
    shutil.copy2(WURZEL / "werkzeug" / "runner.py", ZIEL / "runner.py")

    (ZIEL / "index.html").write_text(startseite(schritte), encoding="utf-8")
    (ZIEL / "karten.html").write_text(kartenseite(schritte), encoding="utf-8")
    for i, s in enumerate(schritte):
        vorher = schritte[i - 1] if i > 0 else None
        nachher = schritte[i + 1] if i + 1 < len(schritte) else None
        (ZIEL / "schritt" / f"{s['id']}.html").write_text(schritt_seite(s, vorher, nachher), encoding="utf-8")

    # Service Worker: Versionsnummer aus dem Inhalt, damit neue Fassungen ankommen
    seiten = ["index.html", "karten.html"] + [f"schritt/{s['id']}.html" for s in schritte]
    statisch = ["app.css", "app.js", "rechner.js", "runner.py", "icon.svg", "manifest.webmanifest"]
    fingerabdruck = hashlib.sha256()
    for name in seiten + statisch:
        fingerabdruck.update((ZIEL / name).read_bytes())
    sw = (WEB / "sw.js").read_text(encoding="utf-8")
    sw = sw.replace("__VERSION__", fingerabdruck.hexdigest()[:12]).replace("__DATEIEN__", json.dumps(seiten + statisch))
    (ZIEL / "sw.js").write_text(sw, encoding="utf-8")

    if not args.ohne_python:
        pyodide_holen()
    print(f"{len(schritte)} Schritte, {sum(len(s['karten']) for s in schritte)} Karten → {ZIEL}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
