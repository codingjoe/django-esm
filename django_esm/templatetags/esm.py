import functools
import json

from django import template
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils.safestring import mark_safe

from .. import utils

register = template.Library()


@register.simple_tag
@functools.lru_cache()
def importmap():
    with (settings.BASE_DIR / "package.json").open() as f:
        package_json = json.load(f)

    imports = dict(utils.parse_root_package(package_json)) | dict(
        utils.parse_dependencies(package_json)
    )

    return mark_safe(  # nosec
        json.dumps(
            {"imports": {k: staticfiles_storage.url(v) for k, v in imports.items()}},
            indent=2 if settings.DEBUG else None,
            separators=None if settings.DEBUG else (",", ":"),
        )
    )
