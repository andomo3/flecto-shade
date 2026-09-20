"""Serve the console and the API from one origin, locally, with no network.

    python software/api/local_server.py --port 8000

The static page is served from `software/page/`, and anything under `/api/` goes to the
same router a Vercel Function runs. Nothing here is used in deployment.
"""

import argparse
import json
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from flecto.app import Request, dispatch  # noqa: E402

PAGE = HERE.parent / "page"


class Console(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PAGE), **kwargs)

    def do_GET(self):
        if self.path.startswith("/api/"):
            return self.api("GET")
        return super().do_GET()

    def do_POST(self):
        return self.api("POST")

    def do_PATCH(self):
        return self.api("PATCH")

    def do_PUT(self):
        return self.api("PUT")

    def api(self, method):
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else b""
        request = Request(
            method=method,
            path=parsed.path,
            query={key: values[0] for key, values in parse_qs(parsed.query).items()},
            body=body,
            headers=dict(self.headers),
        )
        response = dispatch(request)
        payload = json.dumps(response.body).encode("utf-8")
        self.send_response(response.status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        for key, value in response.headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(payload)

    def end_headers(self):
        if not self.path.startswith("/api/"):
            self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *_args):
        return


def main():
    parser = argparse.ArgumentParser(description="The console and the API, on one port.")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Console)
    print(f"watering http://127.0.0.1:{args.port}/")
    print(f"console  http://127.0.0.1:{args.port}/console.html")
    print(f"api      http://127.0.0.1:{args.port}/api/health")
    server.serve_forever()


if __name__ == "__main__":
    main()
