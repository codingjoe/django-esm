import functools
import json

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

from .. import utils

register = template.Library()


@register.simple_tag
@functools.lru_cache
def importmap():
    with (settings.BASE_DIR / "package.json").open() as f:
        package_json = json.load(f)
    return mark_safe(  # nosec
        json.dumps(
            {"imports": dict(utils.parse_root_package(package_json))},
            indent=2 if settings.DEBUG else None,
            separators=None if settings.DEBUG else (",", ":"),
        )
    )
