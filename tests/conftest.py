import subprocess
from pathlib import Path

import pytest

TEST_DIR = Path(__file__).parent


@pytest.fixture(scope="session")
def package_json():
    subprocess.check_call(["npm", "install"], cwd=TEST_DIR)
    return TEST_DIR / "package.json"


@pytest.fixture(scope="session")
def _django_db_helper():
    # we do not need a database for this CI suite
    pass
