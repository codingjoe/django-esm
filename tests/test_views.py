import os


def test_importmap(page, live_server):
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    page.goto(live_server.url)
    assert (
        """<script type="importmap">{
  "imports": {"""
        in page.content()
    )
