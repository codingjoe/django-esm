from django_esm import utils


def test_parse_package_json(package_json):
    assert dict(utils.parse_package_json(package_json.parent)) == {
        "htmx.org": "/static/htmx.org/dist/htmx.min.js",
        "lit": "/static/lit/index.js",
        "@lit/reactive-element": "/static/%40lit/reactive-element/reactive-element.js",
        "@lit-labs/ssr-dom-shim": "/static/%40lit-labs/ssr-dom-shim/index.js",
        "lit-element": "/static/lit-element/index.js",
        "lit-html": "/static/lit-html/lit-html.js",
    }
