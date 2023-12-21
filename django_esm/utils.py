import json
from pathlib import Path

from django.contrib.staticfiles.storage import staticfiles_storage


def parse_package_json(path: Path = None, node_modules: Path = None):
    """Parse a project main package.json and return a dict of importmap entries."""
    if node_modules is None:
        node_modules = path / "node_modules"
    with (path / "package.json").open() as f:
        package_json = json.load(f)
    name = package_json["name"]
    dependencies = package_json.get("dependencies", {})
    main = package_json.get("main", None)
    if main:
        yield name, staticfiles_storage.url(
            str((path / main).relative_to(node_modules))
        )
    for dep_name, dep_version in dependencies.items():
        yield from parse_package_json(node_modules / dep_name, node_modules)
