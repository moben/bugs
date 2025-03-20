import string
import sys
from collections import defaultdict
from http.server import BaseHTTPRequestHandler, HTTPServer, HTTPStatus
from threading import Thread
from typing import Final
from urllib.parse import quote

ua_paths = defaultdict(set)

# All printable ascii characters correctly quoted if needed
# + a quoted `~` (tilde), to show the difference between requests and other clients
valid_redirect_target: Final = f"/v/%7E__-.~__{quote(string.printable)}__"
# all non-whitespace printable ascii characters, unquoted (except `#`, which breaks most clients)
# + a quoted `~` (tilde), to show the difference between requests and other clients
# + some invalid percent escape sequences
invalid_redirect_target: Final = f"/i/%^1%__%%/%7E__-.~__{string.ascii_letters} {string.digits} {string.punctuation.replace('#', '')}__"


class Handler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        print(self.headers.get("User-Agent"))

    def _redirect(self, target: str) -> None:
        self.send_response(HTTPStatus.FOUND)
        self.send_header("Location", target)
        self.send_header("Content-Length", "0")
        self.end_headers()
        return None

    def _send_close(self, status: HTTPStatus) -> None:
        out = b"""<html><head><title>Close</title></head><body onload="window.close();"></body></html>\n"""

        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)
        return None

    def do_GET(self):
        if not (user_agent := self.headers.get("User-Agent")):
            self.send_response(HTTPStatus.BAD_REQUEST)
            self.end_headers()
            return None

        if self.path == "/favicon.ico":
            self.send_response(HTTPStatus.NOT_FOUND)
            self.end_headers()
            return None

        ua_paths[user_agent].add(self.path)

        if self.path == "/v":
            return self._redirect(valid_redirect_target)
        elif self.path == "/i":
            return self._redirect(invalid_redirect_target)
        elif self.path == valid_redirect_target:
            return self._send_close(HTTPStatus.OK)
        else:
            # In the real world this might be 4xx, but we don't want to deal with
            # errors in clients and just check the redirection anyway
            return self._send_close(HTTPStatus.OK)


def main() -> None:
    print(f"{valid_redirect_target=}")
    print(f"{invalid_redirect_target=}")

    port = int(sys.argv[1])
    httpd = HTTPServer(("", port), Handler)
    try:
        t = Thread(target=httpd.serve_forever)
        t.start()
        input(f"""
Request 'http://localhost:{port}/v' or 'http://localhost:{port}/i', following redirects

Press Enter when done to exit...
""")
    finally:
        httpd.shutdown()
        t.join()

    aus_by_paths = {
        tuple(reqs): {ua for ua, r in ua_paths.items() if r == reqs}
        for reqs in ua_paths.values()
    }
    if aus_by_paths:
        print("The following paths were requested by these User-Agents:")
        for reqs, uas in aus_by_paths.items():
            print()
            print(f"  - {', '.join(sorted(reqs))}")
            for ua in sorted(uas):
                print(f"    - {ua}")


if __name__ == "__main__":
    main()
