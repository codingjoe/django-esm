import json
import subprocess
from pathlib import Path

import pytest
from django_esm.conf import get_settings

TEST_DIR = Path(__file__).parent


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
