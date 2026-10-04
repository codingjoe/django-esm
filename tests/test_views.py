def test_importmap(client, live_server):
    response = client.get(live_server.url)
    assert b"""<script type="importmap">{"imports":{""" in response.content


def test_esm_tag(client, live_server):
    response = client.get(live_server.url)
    assert (
        b'<script type="module" src="/esm/node_modules/htmx.org/dist/htmx.min-'
        in response.content
    )
    assert b'" integrity="sha256-' in response.content
