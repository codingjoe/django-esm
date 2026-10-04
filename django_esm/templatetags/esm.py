import json

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

from ..forms import ESM
from ..importmap import get_importmap

register = template.Library()


@register.simple_tag
def importmap():
    """Render the import map for an importmap script tag."""
    return mark_safe(  # noqa: S308
        json.dumps(
            get_importmap(),
            indent=2 if settings.DEBUG else None,
            separators=None if settings.DEBUG else (",", ":"),
        )
    )


@register.simple_tag
def esm(module_name):
    """Load a module from the import map as a script tag with its integrity hash."""
    return ESM(module_name)
