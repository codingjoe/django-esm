from django.conf import settings

__all__ = ["get_settings"]


def get_settings():
    return type(
        "Settings",
        (),
        {
            "PACKAGE_DIR": "",
            "STATIC_DIR": "",
            "STATIC_PREFIX": "",
            **getattr(settings, "ESM", {}),
        },
    )
