/* Der Rechner: Python im Hintergrund.

   Läuft als Web Worker, also in einem eigenen Thread. Zwei Gründe:
   - Die Seite bleibt bedienbar, während Python rechnet.
   - Hängt dein Code in einer Endlosschleife, beendet app.js den Worker
     nach zehn Sekunden. Im Hauptthread ginge das nicht, die Seite fröre ein.

   Python (Pyodide) und runner.py kommen vom eigenen Server. Dein Code
   verlässt das Gerät nie. */
"use strict";

importScripts("pyodide/pyodide.js");

let py = null;

async function laden() {
  if (py) return py;
  py = await loadPyodide({ indexURL: "pyodide/" });
  const runner = await (await fetch("runner.py")).text();
  py.FS.writeFile("runner.py", runner);
  py.runPython("import sys; sys.path.insert(0, '.')");
  return py;
}

self.onmessage = async (e) => {
  const { art, id, code, tests } = e.data;
  try {
    const p = await laden();
    if (art === "laden") { self.postMessage({ art: "bereit" }); return; }
    p.globals.set("_code", code);
    p.globals.set("_tests", tests);
    const roh = p.runPython("import json, runner; json.dumps(runner.ausfuehren(_code, _tests))");
    self.postMessage({ art: "ergebnis", id, ergebnis: JSON.parse(roh) });
  } catch (err) {
    self.postMessage({ art: "panne", id, meldung: String(err && err.message || err) });
  }
};
