from pathlib import Path

import pytest

from django_esm import utils

FIXTURE_DIR = Path(__file__).parent


def test_parse_root_package(package_json):
    import_map = dict(utils.parse_root_package(package_json))
    assert import_map["htmx.org"] == "/static/htmx.org/dist/htmx.min.js"
    assert import_map["lit"] == "/static/lit/index.js"
    assert (
        import_map["@lit/reactive-element"]
        == "/static/%40lit/reactive-element/reactive-element.js"
    )
    assert import_map["lit-html"] == "/static/lit-html/lit-html.js"
    assert import_map["#index"] == "/static/js/index.js"
    assert import_map["#components/index.js"] == "/static/js/components/index.js"
    assert import_map["#htmx"] == "https://unpkg.com/htmx.org@1.9.10"


def test_parse_root_package__bad_imports(package_json):
    package_json["imports"] = "foo"
    with pytest.raises(ValueError) as e:
        dict(utils.parse_root_package(package_json))
    assert "must be an object" in str(e.value)

    package_json["imports"] = ["foo"]
    with pytest.raises(ValueError) as e:
        dict(utils.parse_root_package(package_json))
    assert "must be an object" in str(e.value)


def test_parse_root_package__bad_keys(package_json):
    package_json["imports"] = {"foo": "/bar"}
    with pytest.raises(ValueError) as e:
        dict(utils.parse_root_package(package_json))
    assert "must start with #" in str(e.value)


def test_cast_exports():
    assert utils.cast_exports({"exports": {"foo": "bar"}}) == {"foo": "bar"}
    assert utils.cast_exports({"exports": "foo"}) == {".": "foo"}
    assert utils.cast_exports({"exports": ["foo"]}) == {"foo": "foo"}


def test_get_static_from_abs_path():
    assert not list(utils.get_static_from_abs_path("#some-module", Path("/foo/bar")))
