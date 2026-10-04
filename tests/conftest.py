import json
import subprocess
from pathlib import Path

import pytest
from django_esm import importmap
from django_esm.conf import get_settings
from django_esm.templatetags import esm

TEST_DIR = Path(__file__).parent


@pytest.fixture
def importmap_file(settings, tmp_path, monkeypatch):
    """Write an import map to a temporary static directory and reset the caches."""
    (tmp_path / "importmap.json").write_text(
        json.dumps(
            {
                "imports": {
                    "remote": "https://cdn.example.com/module.js",
                    "local": "./local.js",
                },
                "integrity": {
                    "https://cdn.example.com/module.js": "sha256-remote",
                    "./local.js": "sha256-local",
                },
            }
        )
    )
    settings.ESM = {"STATIC_DIR": tmp_path}
    monkeypatch.setattr(importmap, "resolved_importmap", {})
    monkeypatch.setattr(esm, "importmap_json", "")


@pytest.fixture(scope="session")
def package_json():
    subprocess.check_call(["npm", "install", "--omit=dev"], cwd=TEST_DIR)
    with (TEST_DIR / "package.json").open() as f:
        return json.load(f)


@pytest.fixture(scope="session")
def _django_db_helper():
    # we do not need a database for this CI suite
    pass


@pytest.fixture(scope="session")
def built_module_url():
    """URL of a real built entry point, read from the generated import map."""
    esm_settings = get_settings()
    importmap = json.loads((esm_settings.STATIC_DIR / "importmap.json").read_text())
    relative_url = next(
        value for value in importmap["imports"].values() if value.startswith("./")
    )
    return f"/{esm_settings.STATIC_PREFIX}/{relative_url[2:]}"
