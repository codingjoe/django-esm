import pathlib

import pytest
from django_esm import importmap


@pytest.fixture
def raw_importmap():
    return {
        "imports": {
            "remote": "https://cdn.example.com/module.js",
            "local": "./local.js",
        },
        "integrity": {
            "https://cdn.example.com/module.js": "sha256-remote",
            "./local.js": "sha256-local",
        },
    }


def test_resolve_importmap_urls(raw_importmap):
    assert importmap._resolve_importmap_urls(raw_importmap) == {
        "imports": {
            "remote": "https://cdn.example.com/module.js",
            "local": "/esm/local.js",
        },
        "integrity": {
            "https://cdn.example.com/module.js": "sha256-remote",
            "/esm/local.js": "sha256-local",
        },
    }


def test_resolve_importmap_urls__uses_forward_slashes(raw_importmap, monkeypatch):
    """URLs must keep forward slashes, even where pathlib.Path is WindowsPath."""
    monkeypatch.setattr(pathlib, "Path", pathlib.PureWindowsPath)

    resolved = importmap._resolve_importmap_urls(raw_importmap)

    assert resolved["imports"]["local"] == "/esm/local.js"
