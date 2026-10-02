import asyncio

import pytest
from asgiref.testing import ApplicationCommunicator

pytest.importorskip("servestatic")
from tests.testapp.asgi import application  # noqa: E402


def _scope(path):
    return {
        "type": "http",
        "asgi": {"version": "3.0", "spec_version": "2.1"},
        "http_version": "1.1",
        "method": "GET",
        "scheme": "http",
        "path": path,
        "raw_path": path.encode(),
        "query_string": b"",
        "root_path": "",
        "headers": [(b"host", b"localhost")],
        "client": ("127.0.0.1", 12345),
        "server": ("127.0.0.1", 80),
    }


async def _request(path):
    communicator = ApplicationCommunicator(application, _scope(path))
    await communicator.send_input(
        {"type": "http.request", "body": b"", "more_body": False}
    )
    start = await communicator.receive_output(timeout=5)
    body = bytearray()
    while True:
        message = await communicator.receive_output(timeout=5)
        if message["type"] == "http.response.body":
            body.extend(message.get("body", b""))
            if not message.get("more_body", False):
                break
    await communicator.wait(timeout=5)
    return start["status"], dict(start["headers"]), bytes(body)


def test_serves_built_module_with_immutable_caching(built_module_url):
    status, headers, body = asyncio.run(_request(built_module_url))

    assert status == 200
    assert headers[b"content-type"].startswith(b"text/javascript")
    assert b"immutable" in headers[b"cache-control"]
    assert headers[b"access-control-allow-origin"] == b"*"
    assert body


def test_delegates_other_requests_to_django():
    status, _, body = asyncio.run(_request("/"))

    assert status == 200
    assert b"Test App" in body


def test_unknown_esm_module_is_not_served():
    status, _, _ = asyncio.run(_request("/esm/nope.js"))

    assert status == 404
