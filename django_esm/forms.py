import warnings

from django.forms import Script

from .importmap import resolve_module

__all__ = ["ESM", "ImportESModule"]


class ESM(Script):
    """
    Import an ES module from the import map as a script tag with its integrity hash.

    Usage:
        class MyForm(forms.Form):
            class Media:
                js = [ESM("@sentry/browser")]
    """

    # https://code.djangoproject.com/ticket/36353
    element_template = '<script type="module" src="{path}"{attributes}></script>'

    def __init__(self, src, **attributes):
        source_url, integrity = resolve_module(src)
        super().__init__(source_url, **attributes | {"integrity": integrity})


class ImportESModule(ESM):
    """Provide a deprecated alias for ESM."""

    def __init__(self, *args, **kwargs):
        warnings.warn(
            "ImportESModule is deprecated, use django_esm.forms.ESM instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)
