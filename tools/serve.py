#!/usr/bin/env python3
"""Local preview server.

Serves the site with directory-style URLs (/practice-areas/dui-defense/) and
sends no-store, so a changed stylesheet is actually picked up on reload rather
than silently served from cache.

    python3 tools/serve.py [port]

This is for local development only. Cloudflare Pages serves the real site;
caching in production is set by _headers.
"""
import http.server
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def log_message(self, fmt, *args):
        if "404" in (fmt % args):
            super().log_message(fmt, *args)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8788
    http.server.ThreadingHTTPServer(("", port), Handler).serve_forever()
