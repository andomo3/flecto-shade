"""The Vercel Python entry point. One function, every /api route.

The handler does three things and no more: read the request, hand it to the router, and
write the response. Every rule, every query, and every conversion lives in `flecto/`,
so the same code runs under `python software/api/local_server.py` with no network and
under a Vercel Function with no change.

`vercel.json` rewrites `/api/(.*)` here, so this file is the whole API surface.
"""

import json
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))

from flecto.app import Request, dispatch  # noqa: E402

MAX_BODY_BYTES = 256 * 1024


class handler(BaseHTTPRequestHandler):  # noqa: N801 - Vercel looks for this name
    server_version = "flecto-api"

    def do_GET(self):
        self.respond("GET")

    def do_POST(self):
        self.respond("POST")

    def do_PATCH(self):
        self.respond("PATCH")

    def do_PUT(self):
        self.respond("PUT")

    def do_OPTIONS(self):
        self.send_response(204)
        for key, value in self.cors().items():
            self.send_header(key, value)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

    def cors(self):
        import os
        origin = os.environ.get("ALLOWED_ORIGIN", "")
        if not origin:
            return {}
        return {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Methods": "GET, POST, PATCH, PUT, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Idempotency-Key",
        }

    def read_body(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return b""
        if length > MAX_BODY_BYTES:
            return None
        return self.rfile.read(length)

    def respond(self, method):
        parsed = urlparse(self.path)
        body = self.read_body()
        if body is None:
            self.write(413, {"error": {
                "code": "body_too_large",
                "message": "The request body is larger than this service accepts.",
            }}, {"Cache-Control": "no-store"})
            return

        request = Request(
            method=method,
            path=parsed.path,
            query={key: values[0] for key, values in parse_qs(parsed.query).items()},
            body=body,
            headers=dict(self.headers),
        )
        response = dispatch(request)
        self.write(response.status, response.body, response.headers)

    def write(self, status, body, headers):
        payload = json.dumps(body, sort_keys=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        for key, value in {**headers, **self.cors()}.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *_args):
        """Quiet by default: a request line can carry a grower's zone identifiers."""
        return
