from pathlib import Path

import pytest

from django_esm import utils

FIXTURE_DIR = Path(__file__).parent


def test_parse_root_package(package_json):
    import_map = dict(utils.parse_root_package(package_json))
    assert import_map["htmx.org"].startswith("/static/htmx.org/dist/htmx.min")
    assert import_map["lit"].startswith("/static/lit/index.")
    assert import_map["@lit/reactive-element"].startswith(
        "/static/@lit/reactive-element/reactive-element"
    )
    assert import_map["lit-html"].startswith("/static/lit-html/lit-html")
    assert import_map["#index"] == "/static/js/index.d41d8cd98f00.js"
    assert import_map["#components/"] == "/static/js/components/"
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
    with pytest.raises(ValueError) as e:
        utils.get_static_from_abs_path(Path("/foo/bar"))
    assert "Could not find" in str(e.value)
