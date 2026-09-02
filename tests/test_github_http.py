from __future__ import annotations

import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from fixbundle.github import GitHubAPI


def test_bearer_token_is_not_forwarded_to_redirect_target():
    seen: dict[str, str | None] = {}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            if self.path == "/redirect":
                seen["api"] = self.headers.get("Authorization")
                self.send_response(302)
                self.send_header("Location", f"http://127.0.0.1:{self.server.server_port}/blob")
                self.end_headers()
                return
            if self.path == "/blob":
                seen["blob"] = self.headers.get("Authorization")
                body = b"real log payload\n"
                self.send_response(200)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            self.send_response(404)
            self.end_headers()

        def log_message(self, format, *args):  # noqa: A002
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        api = GitHubAPI(token="test-token", api_root=f"http://127.0.0.1:{server.server_port}")
        assert api.text("/redirect") == "real log payload\n"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)

    assert seen["api"] == "Bearer test-token"
    assert seen["blob"] is None
