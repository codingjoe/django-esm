import json
from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles.finders import get_finders
from django.contrib.staticfiles.storage import staticfiles_storage


def parse_root_package(package_json):
    """Parse a project main package.json and return a dict of importmap entries."""
    imports = package_json.get("imports", {})
    if isinstance(imports, (str, list)):
        raise ValueError(f"package.imports must be an object, {type(imports)} given")

    for module_name, module in imports.items():
        if not module_name.startswith("#"):
            raise ValueError(
                f"package.imports keys must start with #, {module_name} given"
            )
        try:
            mod = module["default"]
        except TypeError:
            mod = module
        url = mod
        if mod[0] in [".", "/"]:
            # local file
            url = get_static_from_abs_path(settings.BASE_DIR / mod)
            if mod.endswith("/*"):
                url = url[:-2] + "/"
                module_name = module_name[:-1]
        yield module_name, url

    for dep_name, dep_version in package_json.get("dependencies", {}).items():
        yield from parse_package_json(settings.BASE_DIR / "node_modules" / dep_name)


def get_static_from_abs_path(path: Path):
    for finder in get_finders():
        for storage in finder.storages.values():
            try:
                rel_path = path.relative_to(Path(storage.location))
            except ValueError:
                pass
            else:
                return staticfiles_storage.url(str(rel_path))
    raise ValueError(f"Could not find {path} in staticfiles")


# There is a long history how ESM is supported in Node.js
# So we implement some fallbacks, see also: https://nodejs.org/api/packages.html#exports
ESM_KEYS = ["exports", "module", "main"]


def cast_exports(package_json):
    exports = {}
    for key in ESM_KEYS:
        try:
            exports = package_json[key]
        except KeyError:
            continue
        else:
            break
    if not exports:
        exports = {}
    elif isinstance(exports, str):
        exports = {".": exports}
    elif isinstance(exports, list):
        exports = {i: i for i in exports}
    return exports


def parse_package_json(path: Path = None):
    """Parse a project main package.json and return a dict of importmap entries."""
    with (path / "package.json").open() as f:
        package_json = json.load(f)
    name = package_json["name"]
    dependencies = package_json.get("dependencies", {})
    exports = cast_exports(package_json)

    for module_name, module in exports.items():
        try:
            mod = module["default"]
        except TypeError:
            mod = module

        yield str(Path(name) / module_name), staticfiles_storage.url(
            str((path / mod).relative_to(settings.BASE_DIR / "node_modules"))
        )

    if (path / "node_modules").exists():
        node_modules = path / "node_modules"
    else:
        node_modules = path / "/".join(".." for _ in Path(name).parts)
    for dep_name, dep_version in dependencies.items():
        yield from parse_package_json(node_modules / dep_name)
