import json
import pathlib
import re

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

from .. import conf

register = template.Library()

importmap_json = {}


def _resolve_importmap_urls(raw_importmap):
    full_importmap = {
        "imports": {},
        "integrity": {},
    }
    for entry_pointy, filename in raw_importmap["imports"].items():
        if re.match("^https?://", filename):
            static_url = filename
        else:
            static_url = str(
                pathlib.Path("/") / conf.get_settings().STATIC_PREFIX / filename
            )
        full_importmap["imports"][entry_pointy] = static_url
        full_importmap["integrity"][static_url] = raw_importmap["integrity"][filename]
    return json.dumps(
        full_importmap,
        indent=2 if settings.DEBUG else None,
        separators=None if settings.DEBUG else (",", ":"),
    )


@register.simple_tag
def importmap():
    global importmap_json
    print(not importmap_json or settings.DEBUG)
    if not importmap_json or settings.DEBUG:
        with (
            pathlib.Path(conf.get_settings().STATIC_DIR) / "importmap.json"
        ).open() as f:
            raw_importmap = json.load(f)
            importmap_json = _resolve_importmap_urls(raw_importmap)
        print(importmap_json)
    return mark_safe(importmap_json)  # nosec
