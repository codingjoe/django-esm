import json
from pathlib import Path

from django.contrib.staticfiles.storage import staticfiles_storage

# There is a long history how ESM is supported in Node.js
# So we implement some fallbacks, see also: https://nodejs.org/api/packages.html#exports
ESM_KEYS = ["exports", "module", "main"]


def parse_package_json(path: Path = None, node_modules: Path = None):
    """Parse a project main package.json and return a dict of importmap entries."""
    if node_modules is None:
        node_modules = path / "node_modules"
    with (path / "package.json").open() as f:
        package_json = json.load(f)
    name = package_json["name"]
    dependencies = package_json.get("dependencies", {})
    for key in ESM_KEYS:
        export = package_json.get(key, None)
        if export:
            try:
                for module_name, module in export.items():
                    yield str(Path(name) / module_name), staticfiles_storage.url(
                        str((path / module["default"]).relative_to(node_modules))
                    )
            except AttributeError:
                yield name, staticfiles_storage.url(
                    str((path / export).relative_to(node_modules))
                )
    for dep_name, dep_version in dependencies.items():
        yield from parse_package_json(node_modules / dep_name, node_modules)
