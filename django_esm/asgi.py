from servestatic import ServeStaticASGI

from django_esm.base import ServeESM


class ESM(ServeESM, ServeStaticASGI):
    """Lightweight ASGI ES module loader."""
