import json
from unittest.mock import Mock

import pytest
from django_esm.exceptions import ModuleNotFound
from django_esm.templatetags import esm


def test_importmap_resolves_local_and_remote_urls(importmap_file):
    resolved = json.loads(str(esm.importmap()))

    assert resolved["imports"] == {
        "remote": "https://cdn.example.com/module.js",
        "local": "/esm/local.js",
    }
    assert resolved["integrity"] == {
        "https://cdn.example.com/module.js": "sha256-remote",
        "/esm/local.js": "sha256-local",
    }


def test_importmap_is_cached_when_debug_is_off(settings, tmp_path, importmap_file):
    settings.DEBUG = False

    first = str(esm.importmap())
    (tmp_path / "importmap.json").write_text(
        json.dumps(
            {"imports": {"late": "./late.js"}, "integrity": {"./late.js": "sha"}}
        )
    )

    assert str(esm.importmap()) == first
    assert '"late"' not in first


def test_importmap_is_reread_when_debug_is_on(settings, tmp_path, importmap_file):
    settings.DEBUG = True
    assert '"late"' not in str(esm.importmap())

    (tmp_path / "importmap.json").write_text(
        json.dumps(
            {"imports": {"late": "./late.js"}, "integrity": {"./late.js": "sha"}}
        )
    )

    assert '"late"' in str(esm.importmap())


def test_importmap_serializes_once_when_debug_is_off(
    settings, importmap_file, monkeypatch
):
    settings.DEBUG = False
    dumps = Mock(wraps=json.dumps)
    monkeypatch.setattr(json, "dumps", dumps)

    esm.importmap()
    esm.importmap()

    assert dumps.call_count == 1


def test_esm__ok(importmap_file):
    assert str(esm.esm("local")) == (
        '<script type="module" src="/esm/local.js" integrity="sha256-local"></script>'
    )


def test_esm__remote_url(importmap_file):
    assert str(esm.esm("remote")) == (
        '<script type="module" src="https://cdn.example.com/module.js"'
        ' integrity="sha256-remote"></script>'
    )


def test_esm__module_absent(importmap_file):
    with pytest.raises(ModuleNotFound, match="unknown") as error:
        esm.esm("unknown")

    assert error.value.module_name == "unknown"
