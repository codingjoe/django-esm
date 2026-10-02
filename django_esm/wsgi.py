from servestatic import ServeStatic

from django_esm.base import ServeESM


class ESM(ServeESM, ServeStatic):
    """Lightweight WSGI ES module loader."""
