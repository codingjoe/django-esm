from servestatic import ServeStaticASGI

from django_esm.base import ServeESM


class ESM(ServeESM, ServeStaticASGI):
    """Lightweight ASGI ES module loader.

    Serves the built modules under ``/esm/`` and delegates every other request
    to the wrapped application.
    """
