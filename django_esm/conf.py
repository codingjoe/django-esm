from pathlib import Path

from django.conf import settings

__all__ = ["get_settings"]


def get_settings():
    return type(
        "Settings",
        (),
        {
            "PACKAGE_DIR": Path(getattr(settings, "BASE_DIR", "")),
            "STATIC_DIR": Path(getattr(settings, "STATIC_ROOT")) / "esm",
            "STATIC_PREFIX": "esm",
            **getattr(settings, "ESM", {}),
        },
    )
