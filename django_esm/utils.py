from __future__ import annotations

import itertools
import json
import re
from pathlib import Path

from django.conf import settings


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
            yield from get_static_from_abs_path(
                module_name, settings.BASE_DIR / mod, settings.BASE_DIR
            )
        else:
            yield module_name, url


def parse_dependencies(package_json):
    for dep_name, dep_version in package_json.get("dependencies", {}).items():
        yield from parse_package_json(settings.BASE_DIR / "node_modules" / dep_name)


def get_static_from_abs_path(mod: str, path: Path, location: Path):
    try:
        rel_path = path.relative_to(location.resolve())
    except ValueError:
        pass
    else:
        if "*" in mod:
            for match in location.glob(str(rel_path).replace("*", "**/*")):
                if match.is_dir():
                    continue
                sp = str(match.relative_to(location.resolve()))
                pattern = re.escape(str(rel_path)).replace(r"\*", r"(.*)")
                bit = re.match(pattern, sp).group(1)
                yield mod.replace("*", bit), sp
        else:
            yield mod, str(rel_path)


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


def find_default_key(module):
    try:
        yield module["default"]
    except TypeError:
        if isinstance(module, list):
            yield from itertools.chain(*(find_default_key(i) for i in module))
        else:
            yield module
    except KeyError:
        yield from find_default_key(module["import"])


def parse_package_json(path: Path = None):
    """Parse a project main package.json and return a dict of importmap entries."""
    with (path / "package.json").open() as f:
        package_json = json.load(f)
    name = package_json["name"]
    dependencies = package_json.get("dependencies", {})
    exports = cast_exports(package_json)

    try:
        module = exports["default"]
        yield from get_static_from_abs_path(
            name,
            path / module,
            settings.BASE_DIR / "node_modules",
        )
    except KeyError:
        try:
            module = exports["import"]
            yield from get_static_from_abs_path(
                name,
                path / module,
                settings.BASE_DIR / "node_modules",
            )
        except KeyError:
            for module_name, module in exports.items():
                module = next(find_default_key(module))

                yield from get_static_from_abs_path(
                    str(Path(name) / module_name),
                    path / module,
                    settings.BASE_DIR / "node_modules",
                )

    for dep_name, dep_version in dependencies.items():
        dep_path = path
        while not (dep_path / "node_modules" / dep_name).exists():
            dep_path /= ".."

        yield from parse_package_json((dep_path / "node_modules" / dep_name).resolve())
