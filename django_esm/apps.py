from django.apps import AppConfig


class ESMConfig(AppConfig):
    name = "django_esm"
    verbose_name = "ESM"

    def ready(self):
        from . import checks  # noqa
