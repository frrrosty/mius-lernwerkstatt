#!/usr/bin/env python3
"""Lokale Vorschau von dist/ mit denselben Sicherheits-Headern wie auf dem Server.

  python werkzeug/vorschau.py        dann http://localhost:8710

Warum nicht einfach «python -m http.server»? Der liefert keine
Content-Security-Policy. Ob Python im Browser mit der strengen Regel vom
Server läuft, sähe man dann erst nach dem Hochladen.
"""
import http.server
import re
from functools import partial
from pathlib import Path

DIST = Path(__file__).resolve().parent.parent / "dist"
HTACCESS = (Path(__file__).resolve().parent.parent / "web" / ".htaccess").read_text(encoding="utf-8")
CSP = re.search(r'Content-Security-Policy "([^"]+)"', HTACCESS).group(1)


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, ".wasm": "application/wasm", ".webmanifest": "application/manifest+json"}

    def end_headers(self):
        self.send_header("Content-Security-Policy", CSP)
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()


if __name__ == "__main__":
    print("Vorschau auf http://localhost:8710 (Strg+C beendet)")
    http.server.ThreadingHTTPServer(("127.0.0.1", 8710), partial(Handler, directory=str(DIST))).serve_forever()
