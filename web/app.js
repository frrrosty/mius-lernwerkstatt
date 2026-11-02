/* Lernwerkstatt: Verhalten der Seiten.
   Fortschritt, Code und Notizen liegen im Prototyp im Browser (localStorage).
   Später übernimmt das ein Server, damit Handy und Laptop denselben Stand haben. */
(function () {
  "use strict";
  var $ = function (s, w) { return (w || document).querySelector(s); };
  var $$ = function (s, w) { return Array.prototype.slice.call((w || document).querySelectorAll(s)); };
  var wurzel = document.body.dataset.wurzel || "";

  /* ---------- Speicher (darf fehlen, zum Beispiel im privaten Modus) ---------- */
  function lies(k, ersatz) { try { var v = localStorage.getItem("lw:" + k); return v === null ? ersatz : JSON.parse(v); } catch (e) { return ersatz; } }
  function merke(k, v) { try { localStorage.setItem("lw:" + k, JSON.stringify(v)); } catch (e) {} }
  function esc(t) { return String(t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }

  function statusText(id) {
    var s = lies("status:" + id, null);
    return s === "geloest" ? ["gelöst", "geloest"] : s === "begonnen" ? ["begonnen", "begonnen"] : ["offen", ""];
  }

  /* ---------- Startseite: Fortschritt ---------- */
  var pfad = $$(".pfad-schritt");
  if (pfad.length) {
    var geloest = 0;
    pfad.forEach(function (a) {
      var st = statusText(a.dataset.schritt), el = $("[data-status]", a);
      el.textContent = st[0]; if (st[1]) el.classList.add(st[1]);
      if (st[1] === "geloest") geloest++;
    });
    $("[data-fortschritt]").textContent = geloest + " von " + pfad.length + " Übungen gelöst";
    $("[data-balken]").style.width = (geloest / pfad.length * 100) + "%";
  }

  /* ---------- Schritt ---------- */
  var datenEl = $("#schritt-daten");
  if (datenEl) schritt(JSON.parse(datenEl.textContent));

  function schritt(D) {
    var editor = $("#code"), knopf = $("[data-pruefen]"), ergebnis = $("[data-ergebnis]");
    var statusEl = $(".uebung [data-status]");
    editor.value = lies("code:" + D.id, D.aufgabe);
    zeigeStatus();

    function zeigeStatus() { var st = statusText(D.id); statusEl.textContent = st[0]; statusEl.className = "status " + st[1]; }

    var uhr;
    editor.addEventListener("input", function () { clearTimeout(uhr); uhr = setTimeout(function () { merke("code:" + D.id, editor.value); }, 400); });
    editor.addEventListener("keydown", function (e) {
      if (e.key === "Tab" && !e.shiftKey) {
        // Tab rückt ein, statt den Fokus zu verlassen. Mit Esc, dann Tab, kommst du heraus.
        if (editor.dataset.esc === "1") { editor.dataset.esc = ""; return; }
        e.preventDefault();
        var a = editor.selectionStart, b = editor.selectionEnd;
        editor.setRangeText("    ", a, b, "end");
        editor.dispatchEvent(new Event("input"));
      } else if (e.key === "Escape") {
        editor.dataset.esc = "1";
      } else if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
        e.preventDefault(); pruefen();
      } else if (e.key === "Enter") {
        // Einrückung der aktuellen Zeile übernehmen, nach einem Doppelpunkt vier mehr
        var pos = editor.selectionStart, anfang = editor.value.lastIndexOf("\n", pos - 1) + 1;
        var zeile = editor.value.slice(anfang, pos), einzug = zeile.match(/^\s*/)[0];
        if (/:\s*$/.test(zeile)) einzug += "    ";
        e.preventDefault();
        editor.setRangeText("\n" + einzug, pos, editor.selectionEnd, "end");
        editor.dispatchEvent(new Event("input"));
      }
    });

    $("[data-zurueck]").addEventListener("click", function () {
      if (editor.value !== D.aufgabe && !knopfBestaetigt(this)) return;
      editor.value = D.aufgabe; merke("code:" + D.id, D.aufgabe); ergebnis.innerHTML = "";
    });
    function knopfBestaetigt(k) {
      // Statt confirm(): ein zweiter Klick bestätigt
      if (k.dataset.sicher === "1") { k.dataset.sicher = ""; k.textContent = "Vorlage wiederherstellen"; return true; }
      k.dataset.sicher = "1"; k.textContent = "Wirklich? Dein Code geht verloren";
      setTimeout(function () { k.dataset.sicher = ""; k.textContent = "Vorlage wiederherstellen"; }, 4000);
      return false;
    }

    umschalter("[data-tests-zeigen]", "[data-tests]", function (el) { el.textContent = D.tests; }, "Tests ansehen", "Tests ausblenden");
    umschalter("[data-loesung-zeigen]", "[data-loesung]", function (el) { $("pre", el).textContent = D.loesung; }, "Musterlösung", "Musterlösung ausblenden");
    if (lies("versucht:" + D.id, false)) $("[data-loesung-zeigen]").hidden = false;

    knopf.addEventListener("click", pruefen);

    function pruefen() {
      knopf.disabled = true;
      merke("code:" + D.id, editor.value);
      ergebnis.innerHTML = '<div class="meldung">' + (rechner.bereit ? "Prüfe …" : "Python wird geladen. Beim ersten Mal dauert das einige Sekunden (rund 13 MB, danach im Speicher).") + "</div>";
      rechner.ausfuehren(editor.value, D.tests).then(zeigen, function (f) {
        ergebnis.innerHTML = '<div class="meldung fehler">' + esc(f) + "</div>";
      }).then(function () { knopf.disabled = false; });
    }

    function zeigen(r) {
      merke("versucht:" + D.id, true);
      $("[data-loesung-zeigen]").hidden = false;
      var h = "";
      if (r.ausgabe) h += '<div class="meldung"><strong>Ausgabe deines Codes</strong><pre>' + esc(r.ausgabe) + "</pre></div>";
      if (r.fehler) {
        h += '<div class="meldung fehler"><strong>Dein Code startet nicht.</strong><pre>' + esc(r.fehler) + "</pre></div>";
        ergebnis.innerHTML = h;
        if (lies("status:" + D.id, null) !== "geloest") merke("status:" + D.id, "begonnen");
        zeigeStatus();
        return;
      }
      var ok = 0;
      r.tests.forEach(function (t) {
        if (t[1]) ok++;
        h += '<div class="zeile ' + (t[1] ? "ok" : "nein") + '"><span class="zeichen">' + (t[1] ? "✓" : "✗") + "</span><span>" + esc(t[0]) + (t[1] ? "" : "<small>" + esc(t[2]) + "</small>") + "</span></div>";
      });
      var alle = ok === r.tests.length;
      h += '<div class="summe">' + ok + " von " + r.tests.length + " bestanden" + (alle ? ". Gelöst." : "") + "</div>";
      ergebnis.innerHTML = h;
      if (alle) merke("status:" + D.id, "geloest");
      else if (lies("status:" + D.id, null) !== "geloest") merke("status:" + D.id, "begonnen");
      zeigeStatus();
    }

    /* Eigene Worte */
    var worte = $("#worte");
    worte.value = lies("worte:" + D.id, "");
    var wu;
    worte.addEventListener("input", function () { clearTimeout(wu); wu = setTimeout(function () { merke("worte:" + D.id, worte.value); }, 400); });

    /* Karten aufklappen */
    $$(".karte-f").forEach(function (b) {
      b.addEventListener("click", function () {
        var a = b.nextElementSibling, auf = b.getAttribute("aria-expanded") !== "true";
        b.setAttribute("aria-expanded", auf); a.hidden = !auf;
      });
    });

    /* Prompt kopieren */
    var kopieren = $("[data-kopieren]");
    kopieren.addEventListener("click", function () {
      var text = $(".prompt").textContent;
      var fertig = function () { kopieren.textContent = "Kopiert"; setTimeout(function () { kopieren.textContent = "Kopieren"; }, 1800); };
      if (navigator.clipboard) navigator.clipboard.writeText(text).then(fertig, markieren); else markieren();
      function markieren() { var r = document.createRange(); r.selectNodeContents($(".prompt")); var s = getSelection(); s.removeAllRanges(); s.addRange(r); kopieren.textContent = "Markiert, jetzt kopieren"; }
    });
  }

  function umschalter(knopfSel, zielSel, fuellen, zu, auf) {
    var k = $(knopfSel), z = $(zielSel);
    k.addEventListener("click", function () {
      var offen = z.hidden;
      if (offen && !z.dataset.gefuellt) { fuellen(z); z.dataset.gefuellt = "1"; }
      z.hidden = !offen; k.setAttribute("aria-expanded", offen); k.textContent = offen ? auf : zu;
    });
  }

  /* ---------- Rechner: Python im Worker, mit Zeitlimit ---------- */
  var rechner = {
    bereit: false, worker: null, wartend: null, nr: 0,
    starten: function () {
      var self = this;
      this.worker = new Worker(wurzel + "rechner.js");
      this.laden = new Promise(function (ok, nein) {
        self.worker.onmessage = function (e) {
          var m = e.data;
          if (m.art === "bereit") { self.bereit = true; ok(); return; }
          if (!self.wartend || m.id !== self.wartend.id) return;
          var w = self.wartend; self.wartend = null; clearTimeout(w.uhr);
          if (m.art === "ergebnis") w.ok(m.ergebnis); else w.nein("Panne im Rechner: " + m.meldung);
        };
        self.worker.onerror = function (e) { nein("Python liess sich nicht laden (" + (e.message || "unbekannt") + "). Bist du offline und warst noch nie hier?"); };
      });
      this.worker.postMessage({ art: "laden" });
    },
    ausfuehren: function (code, tests) {
      var self = this;
      if (!this.worker) this.starten();
      return this.laden.then(function () {
        return new Promise(function (ok, nein) {
          var id = ++self.nr;
          self.wartend = { id: id, ok: ok, nein: nein, uhr: setTimeout(function () {
            // Endlosschleife? Worker beenden, beim nächsten Prüfen neu starten.
            self.worker.terminate(); self.worker = null; self.bereit = false; self.wartend = null;
            nein("Dein Code lief länger als zehn Sekunden und wurde abgebrochen. Gibt es eine Schleife, die nie endet?");
          }, 10000) };
          self.worker.postMessage({ art: "pruefen", id: id, code: code, tests: tests });
        });
      });
    }
  };

  /* ---------- Kartentraining (Leitner, fünf Fächer) ---------- */
  var kartenEl = $("#karten-daten");
  if (kartenEl) training(JSON.parse(kartenEl.textContent));

  function training(alle) {
    var ABSTAND = [0, 1, 3, 7, 16];   // Tage bis zur nächsten Wiederholung je Fach
    var stand = lies("leitner", {});  // id -> {fach, faellig}
    var heute = Math.floor(Date.now() / 864e5);
    var jetzt = null;

    function faellige() { return alle.filter(function (k) { var s = stand[k.id]; return !s || s.faellig <= heute; }); }
    function faecher() {
      var n = [0, 0, 0, 0, 0];
      alle.forEach(function (k) { n[(stand[k.id] || { fach: 0 }).fach]++; });
      $("[data-faecher]").innerHTML = n.map(function (z, i) { return '<div class="fach"><b>' + z + "</b><small>Fach " + (i + 1) + "</small></div>"; }).join("");
    }
    function naechste() {
      faecher();
      var f = faellige();
      if (!f.length) { $("[data-karte]").hidden = true; $("[data-leer]").hidden = false; return; }
      jetzt = f[Math.floor(Math.random() * f.length)];
      $("[data-leer]").hidden = true; $("[data-karte]").hidden = false;
      $("[data-herkunft]").textContent = jetzt.schritt + " · noch " + f.length + " fällig";
      // f und a sind HTML, das bauen.py aus den eigenen Inhalten erzeugt hat, keine Eingabe von aussen
      $("[data-frage]").innerHTML = jetzt.f;
      var a = $("[data-antwort]"); a.innerHTML = jetzt.a; a.hidden = true;
      $("[data-zeigen]").hidden = false; $("[data-ja]").hidden = true; $("[data-nein]").hidden = true;
      $("[data-zeigen]").focus();
    }
    function werten(gewusst) {
      var s = stand[jetzt.id] || { fach: 0 };
      s.fach = gewusst ? Math.min(4, s.fach + 1) : 0;
      // Gewusst: je nach Fach später wieder. Nicht gewusst: morgen wieder, nicht sofort im Kreis.
      s.faellig = heute + (gewusst ? ABSTAND[s.fach] : 1);
      stand[jetzt.id] = s; merke("leitner", stand);
      naechste();
    }
    $("[data-zeigen]").addEventListener("click", function () {
      $("[data-antwort]").hidden = false; this.hidden = true;
      $("[data-ja]").hidden = false; $("[data-nein]").hidden = false; $("[data-ja]").focus();
    });
    $("[data-ja]").addEventListener("click", function () { werten(true); });
    $("[data-nein]").addEventListener("click", function () { werten(false); });
    naechste();
  }

  /* ---------- Offline ---------- */
  if ("serviceWorker" in navigator && location.protocol === "https:") {
    navigator.serviceWorker.register(wurzel + "sw.js").catch(function () {});
  }
})();
