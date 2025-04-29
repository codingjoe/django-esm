def test_importmap(client, live_server):
    response = client.get(live_server.url)
    assert b"""<script type="importmap">{"imports":{""" in response.content
