import functools
import json

from django.conf import settings
from django.contrib.staticfiles.finders import BaseFinder
from django.contrib.staticfiles.utils import matches_patterns
from django.core.checks import Error

from . import storages, utils


class ESMFinder(BaseFinder):
    def __init__(self, apps=None, *args, **kwargs):
        self.apps = apps or []
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        return [*self._check_package_json()]

    def _check_package_json(self):
        if not (settings.BASE_DIR / "package.json").exists():
            return [
                Error(
                    "package.json not found",
                    hint="Run `npm init` to create a package.json file.",
                    obj=self,
                    id="django_esm.E001",
                )
            ]
        return []

    def find(self, path, all=False):
        if path in self.all:
            return [path] if all else path
        return []  # this method has a strange return type

    def list(self, ignore_patterns):
        with (settings.BASE_DIR / "package.json").open() as f:
            package_json = json.load(f)
        for mod, path in utils.parse_root_package(package_json):
            if not matches_patterns(path, ignore_patterns):
                yield path, storages.root_storage
                map_path = settings.BASE_DIR / path
                map_path = map_path.with_suffix(map_path.suffix + ".map")
                if map_path.exists():
                    yield str(
                        map_path.relative_to(settings.BASE_DIR)
                    ), storages.root_storage

    @functools.cached_property
    def all(self):
        return [path for path, storage in self.list([])]
