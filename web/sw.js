/* Service Worker: macht die Lernwerkstatt offline lesbar.

   Er liegt zwischen der Seite und dem Netz. Beim Installieren legt er die
   Seiten in einen Zwischenspeicher; danach antwortet er zuerst aus dem Netz
   und, wenn das nicht geht, aus dem Speicher («network first»). So siehst du
   immer den neuesten Stand, aber im Zug geht es trotzdem.

   Python (rund 13 MB) wird erst beim ersten «Prüfen» geholt und dann
   ebenfalls gespeichert. Die Version ändert sich bei jedem Bau, alte
   Speicher werden dann gelöscht. */
const VERSION = "__VERSION__";
const DATEIEN = __DATEIEN__;
const SPEICHER = "lernwerkstatt-" + VERSION;

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(SPEICHER).then((c) => c.addAll(DATEIEN)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((namen) => Promise.all(namen.filter((n) => n !== SPEICHER && n.startsWith("lernwerkstatt-")).map((n) => caches.delete(n))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET" || new URL(e.request.url).origin !== location.origin) return;
  const istPython = e.request.url.includes("/pyodide/");
  e.respondWith(
    istPython
      // Python ändert sich nur mit der Version: erst Speicher, dann Netz
      ? caches.match(e.request).then((t) => t || fetch(e.request).then((r) => merken(e.request, r)))
      : fetch(e.request).then((r) => merken(e.request, r)).catch(() => caches.match(e.request))
  );
});

function merken(anfrage, antwort) {
  if (antwort.ok) {
    const kopie = antwort.clone();
    caches.open(SPEICHER).then((c) => c.put(anfrage, kopie));
  }
  return antwort;
}
