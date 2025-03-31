import json
import subprocess
import sys
from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from django.core.files.storage import FileSystemStorage

from . import utils

basedir = Path(__file__).parent.parent

root_storage = FileSystemStorage(
    location=settings.BASE_DIR, base_url=settings.STATIC_URL
)


class ESMBundleStorage(ManifestStaticFilesStorage):
    """Bundle dependencies as single file ESM modules."""

    prefix = "esm/"

    def url(self, name, force=False):
        """Return the URL to the file with the given name."""
        if name.startswith(self.prefix):
            p = Path(name)
            if p.suffix == ".mjs":
                name = str(p.with_suffix(".js"))
        return super().url(name, force=force)

    def path(self, name):
        """Return the absolute path to the file with the given name."""
        if name.startswith(self.prefix):
            p = Path(name)
            if p.suffix == ".mjs":
                name = str(p.with_suffix(".js"))
        return super().path(name)

    def post_process(self, paths, **options):
        with (settings.BASE_DIR / "package.json").open() as f:
            package_json = json.load(f)

        subprocess.check_call(
            [
                "node",
                "--experimental-import-meta-resolve",
                (basedir / "bundle.mjs").resolve(),
                str(settings.STATIC_ROOT.absolute()),
            ],
            cwd=settings.BASE_DIR,
            stderr=sys.stderr,
            stdout=sys.stdout,
        )

        imports = list(dict(utils.parse_root_package(package_json)).values())
        imports += [
            f"esm/{k}"
            for k, v in utils.parse_dependencies(package_json)
        ]

        for path in imports:
            paths[path] = self, path
        yield from super().post_process(paths, **options)
