import pathlib

from django_esm import importmap


def test_resolve_importmap_urls__uses_forward_slashes(monkeypatch):
    """URLs must keep forward slashes, even where pathlib.Path is WindowsPath."""
    monkeypatch.setattr(pathlib, "Path", pathlib.PureWindowsPath)
    raw_importmap = {
        "imports": {
            "remote": "https://cdn.example.com/module.js",
            "local": "./local.js",
        },
        "integrity": {
            "https://cdn.example.com/module.js": "sha256-remote",
            "./local.js": "sha256-local",
        },
    }

    resolved = importmap._resolve_importmap_urls(raw_importmap)

    assert resolved["imports"] == {
        "remote": "https://cdn.example.com/module.js",
        "local": "/esm/local.js",
    }
