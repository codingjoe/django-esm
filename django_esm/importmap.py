import json
import pathlib
import re

from django.conf import settings

from . import conf
from .exceptions import ModuleNotFound

__all__ = ["get_importmap", "resolve_module"]

resolved_importmap = {}


def _resolve_importmap_urls(raw_importmap):
    full_importmap = {
        "imports": {},
        "integrity": {},
    }
    static_prefix = conf.get_settings().STATIC_PREFIX
    for module_name, filename in raw_importmap["imports"].items():
        if re.match("^https?://", filename):
            static_url = filename
        else:
            static_url = str(pathlib.Path("/") / static_prefix / filename)
        full_importmap["imports"][module_name] = static_url
        full_importmap["integrity"][static_url] = raw_importmap["integrity"][filename]
    return full_importmap


def get_importmap():
    """Return the resolved import map, re-reading it in DEBUG mode."""
    global resolved_importmap
    if not resolved_importmap or settings.DEBUG:
        with (
            pathlib.Path(conf.get_settings().STATIC_DIR) / "importmap.json"
        ).open() as f:
            resolved_importmap = _resolve_importmap_urls(json.load(f))
    return resolved_importmap


def resolve_module(module_name):
    """Return the source URL and integrity hash of a module in the import map.

    Raises:
        ModuleNotFound: If the import map has no entry for the module.
    """
    importmap_data = get_importmap()
    try:
        source_url = importmap_data["imports"][module_name]
    except KeyError as error:
        raise ModuleNotFound(module_name) from error
    return source_url, importmap_data["integrity"][source_url]
