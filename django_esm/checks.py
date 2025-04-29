import pathlib

from django.core.checks import Error, Tags, Warning, register

from . import conf

__all__ = ["check_esm_settings"]


@register(Tags.staticfiles)
def check_esm_settings(app_configs, **kwargs):
    errors = []
    if not conf.get_settings().PACKAGE_DIR:
        errors.append(
            Error(
                'Setting ESM["PACKAGE_DIR"] is not configured.',
                hint=(
                    'ESM["PACKAGE_DIR"] must be an absolute path or pathlib.Path object.'
                ),
                id="esm.E001",
            )
        )

    if not pathlib.Path(conf.get_settings().PACKAGE_DIR).is_absolute():
        errors.append(
            Error(
                'ESM["PACKAGE_DIR"] is a relative path.',
                hint=(
                    'ESM["PACKAGE_DIR"] must be an absolute path or pathlib.Path object.'
                ),
                id="esm.E002",
            )
        )

    if not conf.get_settings().STATIC_DIR:
        errors.append(
            Error(
                'Setting ESM["STATIC_DIR"] is not configured.',
                hint=(
                    'ESM["STATIC_DIR"] must be an absolute path or pathlib.Path object.'
                ),
                id="esm.E003",
            )
        )

    if not pathlib.Path(conf.get_settings().STATIC_DIR).is_absolute():
        errors.append(
            Error(
                'ESM["STATIC_DIR"] is a relative path.',
                hint=(
                    'ESM["STATIC_DIR"] must be an absolute path or pathlib.Path object.'
                ),
                id="esm.E004",
            )
        )

    if not conf.get_settings().STATIC_PREFIX:
        errors.append(
            Error(
                'Setting ESM["STATIC_PREFIX"] is not configured.',
                hint=(
                    'ESM["STATIC_PREFIX"] must be an absolute path or pathlib.Path object.'
                ),
                id="esm.E005",
            )
        )

    if not (pathlib.Path(conf.get_settings().PACKAGE_DIR) / "package.json").exists():
        errors.append(
            Error(
                f"package.json file not found in: {conf.get_settings().PACKAGE_DIR}",
                hint='Make sure check your ESM["PACKAGE_DIR"] setting.',
                id="esm.E006",
            )
        )

    if not (pathlib.Path(conf.get_settings().STATIC_DIR) / "importmap.json").exists():
        errors.append(
            Warning(
                f"importmap.json file not found in: {conf.get_settings().STATIC_DIR}",
                hint=(
                    'Make sure check your ESM["STATIC_DIR"] setting and to run the "esm" management command to generate the importmap.json file.'
                ),
                id="esm.W001",
            )
        )

    return errors


@register(Tags.staticfiles, deploy=True)
def check_deployment(app_configs, **kwargs):
    errors = []

    if not (pathlib.Path(conf.get_settings().STATIC_DIR) / "importmap.json").exists():
        errors.append(
            Error(
                f"importmap.json file not found in: {conf.get_settings().STATIC_DIR}",
                hint=(
                    'Make sure check your ESM["STATIC_DIR"] setting and to run the "esm" management command to generate the importmap.json file.'
                ),
                id="esm.E007",
            )
        )

    return errors
