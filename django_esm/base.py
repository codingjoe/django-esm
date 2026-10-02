from django.conf import settings

from django_esm.conf import get_settings


class ServeESM:
    def immutable_file_test(self, path, url):
        return True

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **{
                "root": get_settings().STATIC_DIR,
                "prefix": get_settings().STATIC_PREFIX,
                "autorefresh": settings.DEBUG,
            }
            | kwargs,
        )
