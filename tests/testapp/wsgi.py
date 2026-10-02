import os

from django.core.wsgi import get_wsgi_application
from django_esm.wsgi import ESM

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.testapp.settings")

application = ESM(get_wsgi_application())
