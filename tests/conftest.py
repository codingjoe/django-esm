import json
import subprocess
from pathlib import Path

import pytest

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
