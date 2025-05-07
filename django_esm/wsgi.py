from whitenoise import WhiteNoise


class ESM(WhiteNoise):
    """Lightweight WSGI ES module loader based on whitenoise."""

    def immutable_file_test(self, path, url):
        return True

    def __init__(self, *args, **kwargs):
        from django.conf import settings  # noqa: F401

        super().__init__(
            *args,
            **{
                "root": settings.BASE_DIR / "staticfiles" / "esm",
                "prefix": "esm",
                "autorefresh": settings.DEBUG,
            }
            | kwargs,
        )
