import threading
import urllib.error
import urllib.request
from wsgiref.simple_server import WSGIRequestHandler, make_server

import pytest
from django.contrib.staticfiles.handlers import StaticFilesHandler

pytest.importorskip("servestatic")
from tests.testapp.wsgi import application  # noqa: E402


class _QuietRequestHandler(WSGIRequestHandler):
    def log_request(self, code="-", size="-"):
        pass


def _get(url):
    request = urllib.request.Request(url, headers={"Host": "testserver"})
    try:
        response = urllib.request.urlopen(request, timeout=10)
    except urllib.error.HTTPError as error:
        return error.code, error.headers, error.read()
    with response:
        return response.status, response.headers, response.read()


@pytest.fixture(scope="session")
def base_url():
    """Serve the runserver shape: StaticFilesHandler around the ESM-wrapped WSGI app."""
    server = make_server(
        "127.0.0.1",
        0,
        StaticFilesHandler(application),
        handler_class=_QuietRequestHandler,
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        thread.join(timeout=5)


def test_serves_built_module_with_immutable_caching(base_url, built_module_url):
    status, headers, body = _get(base_url + built_module_url)

    assert status == 200
    assert headers["Content-Type"].startswith("text/javascript")
    assert "immutable" in headers["Cache-Control"]
    assert headers["Access-Control-Allow-Origin"] == "*"
    assert body


def test_delegates_other_requests_to_django(base_url):
    status, _, body = _get(base_url + "/")

    assert status == 200
    assert b"Test App" in body


def test_unknown_esm_module_is_not_served(base_url):
    status, _, _ = _get(base_url + "/esm/nope.js")

    assert status == 404
