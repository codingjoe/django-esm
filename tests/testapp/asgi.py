import os

from django.core.asgi import get_asgi_application
from django_esm.asgi import ESM

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.testapp.settings")

application = ESM(get_asgi_application())
