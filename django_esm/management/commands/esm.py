import subprocess  # nosec
import sys

from django.core.management import BaseCommand

from django_esm.conf import get_settings


class Command(BaseCommand):
    """Collect ES modules from the package directory and generate importmap."""

    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument(
            "-w",
            "--watch",
            action="store_true",
            help="Watch for changes in the package directory and re-run collect files.",
        )
        parser.add_argument(
            "-s",
            "--serve",
            action="store_true",
            help="Serve the files using esimport.",
        )

    def handle(self, *args, **options):
        subprocess.check_call(  # nosec
            (
                [
                    "npx",
                    "--yes",
                    "esimport",
                    get_settings().PACKAGE_DIR,
                    get_settings().STATIC_DIR,
                ]
                + (["--watch"] if options["watch"] else [])
                + (["--serve"] if options["serve"] else [])
                + (["--verbose"] if options["verbosity"] > 1 else [])
            ),
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
