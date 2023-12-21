import json

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

from .. import utils

register = template.Library()


@register.simple_tag
def importmap():
    return mark_safe(  # nosec
        json.dumps(
            {"imports": dict(utils.parse_package_json(settings.BASE_DIR))},
            indent=2 if settings.DEBUG else None,
            separators=None if settings.DEBUG else (",", ":"),
        )
    )
