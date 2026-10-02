import json

from django_esm.templatetags import esm


def test_importmap_resolves_local_and_remote_urls(settings, tmp_path, monkeypatch):
    importmap = {
        "imports": {
            "remote": "https://cdn.example.com/module.js",
            "local": "./local.js",
        },
        "integrity": {
            "https://cdn.example.com/module.js": "sha256-remote",
            "./local.js": "sha256-local",
        },
    }
    (tmp_path / "importmap.json").write_text(json.dumps(importmap))
    settings.ESM = {"STATIC_DIR": tmp_path}
    monkeypatch.setattr(esm, "importmap_json", {})

    resolved = json.loads(str(esm.importmap()))

    assert resolved["imports"] == {
        "remote": "https://cdn.example.com/module.js",
        "local": "/esm/local.js",
    }
    assert resolved["integrity"] == {
        "https://cdn.example.com/module.js": "sha256-remote",
        "/esm/local.js": "sha256-local",
    }


def test_importmap_is_cached_when_debug_is_off(settings, tmp_path, monkeypatch):
    settings.DEBUG = False
    importmap_file = tmp_path / "importmap.json"
    importmap_file.write_text(json.dumps({"imports": {}, "integrity": {}}))
    settings.ESM = {"STATIC_DIR": tmp_path}
    monkeypatch.setattr(esm, "importmap_json", {})

    first = str(esm.importmap())
    importmap_file.write_text(
        json.dumps(
            {"imports": {"late": "./late.js"}, "integrity": {"./late.js": "sha"}}
        )
    )

    assert str(esm.importmap()) == first
    assert json.loads(first) == {"imports": {}, "integrity": {}}
