from django.forms import Script

__all__ = ["ImportESModule"]


class ImportESModule(Script):
    """
    Import ES module inline via an importmap.

    Usage:
        class MyForm(forms.Form):
            class Media:
                js = [ImportESModule("@sentry/browser")]
    """

    # https://code.djangoproject.com/ticket/36353
    element_template = "<script{attributes}>import '{path}'</script>"

    def __init__(self, src, **attributes):
        super().__init__(src, **attributes | {"type": "module"})

    @property
    def path(self):
        return self._path
