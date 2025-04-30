import subprocess  # nosec
import sys

from django.contrib.staticfiles.management.commands import collectstatic

from django_esm.conf import get_settings


class Command(collectstatic.Command):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--no-esm",
            "--noesm",
            action="store_true",
            help="Do not collect ES modules before collecting static files.",
        )

    def handle(self, **options):
        if not options["no_esm"]:
            subprocess.check_call(  # nosec
                [
                    "npx",
                    "--yes",
                    "esimport",
                    get_settings().PACKAGE_DIR,
                    get_settings().STATIC_DIR,
                ],
                stdout=sys.stdout,
                stderr=sys.stderr,
            )
            try:
                import whitenoise  # noqa
            except ImportError:
                pass
            else:
                subprocess.check_call(  # nosec
                    [
                        "python3",
                        "-m",
                        "whitenoise.compress",
                        get_settings().STATIC_DIR,
                    ],
                    stdout=sys.stdout,
                    stderr=sys.stderr,
                )
        super().handle(**options)
