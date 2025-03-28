import sys
import urllib
from unittest.mock import patch

import httpx
import requests
import urllib3


def requote_uri(uri):
    return uri


if __name__ == "__main__":
    with (
        patch.object(requests.sessions, "requote_uri", requote_uri),
        patch.object(requests.models, "requote_uri", requote_uri),
    ):
        print("Wrapping requests", file=sys.stderr)
        requests.get(sys.argv[1], headers={"User-Agent": "requests-patched"})
        print("Unwrapping requests", file=sys.stderr)
    requests.get(sys.argv[1])
    urllib.request.urlopen(sys.argv[1])
    urllib3.request("GET", sys.argv[1])
    httpx.get(sys.argv[1], follow_redirects=True)
