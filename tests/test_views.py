import os


def test_importmap(page, live_server):
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    page.goto(live_server.url)
    assert (
        """<script type="importmap">{
  "imports": {
    "htmx.org": "/static/htmx.org/dist/htmx.min.js",
    "lit": "/static/lit/index.js",
    "@lit/reactive-element": "/static/%40lit/reactive-element/reactive-element.js",
    "@lit-labs/ssr-dom-shim": "/static/%40lit-labs/ssr-dom-shim/index.js",
    "lit-element": "/static/lit-element/index.js",
    "lit-html": "/static/lit-html/lit-html.js"
  }
}</script>"""
        in page.content()
    )
