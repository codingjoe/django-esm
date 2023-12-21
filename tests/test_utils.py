from django_esm import utils


def test_parse_package_json(package_json):
    import_map = dict(utils.parse_package_json(package_json.parent))
    assert import_map["htmx.org"] == "/static/htmx.org/dist/htmx.min.js"
    assert import_map["lit"] == "/static/lit/index.js"
    assert (
        import_map["@lit/reactive-element"]
        == "/static/%40lit/reactive-element/reactive-element.js"
    )
    assert import_map["lit-html"] == "/static/lit-html/lit-html.js"
