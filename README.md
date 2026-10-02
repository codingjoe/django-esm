# Django ESM

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github.com/codingjoe/django-esm/raw/main/images/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://github.com/codingjoe/django-esm/raw/main/images/logo-light.svg">
    <img alt="Django ESM: NextGen JavaScript ESM module support for Django" src="https://github.com/codingjoe/django-esm/raw/main/images/logo-light.svg">
  </picture>
</p>

NextGen JavaScript ESM module support for Django.

[![PyPi Version](https://img.shields.io/pypi/v/django-esm.svg)](https://pypi.python.org/pypi/django-esm/)
[![Test Coverage](https://codecov.io/gh/codingjoe/django-esm/branch/main/graph/badge.svg)](https://codecov.io/gh/codingjoe/django-esm)
[![GitHub License](https://img.shields.io/github/license/codingjoe/django-esm)](https://raw.githubusercontent.com/codingjoe/django-esm/master/LICENSE)

## Sponsors

[![Sponsors](https://django.the-box.sh/sponsors/codingjoe/django-esm.svg)](https://github.com/sponsors/codingjoe)

## Highlights

- 😌 easy transition
- ⚡️ smart cache busting
- 📦 no more bundling
- ☕️ native ESM support
- 📍 local vendoring with npm

## Setup

Install the package:

```bash
pip install django-esm[servestatic]
```

`django-esm[whitenoise]` still works as a deprecated alias for `django-esm[servestatic]`.

First, add `django_esm` to your `INSTALLED_APPS` settings:

```python
# settings.py
INSTALLED_APPS = [
    # …
    "django_esm",  # add django_esm before staticfiles
    "django.contrib.staticfiles",
]
```

Wrap your WSGI or ASGI application to serve the built output at `/esm/` and
pass every other request to the wrapped application:

```python
import os

from django.core.wsgi import get_wsgi_application

from django_esm.wsgi import ESM

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

application = ESM(get_wsgi_application())
```

For ASGI, swap in `django.core.asgi.get_asgi_application` and
`django_esm.asgi.ESM`.

`manage.py runserver` loads `WSGI_APPLICATION`, so even an ASGI-deployed project
is served by the WSGI wrapper in development. For ASGI, point uvicorn or daphne
at the wrapped application object, for example `uvicorn myproject.asgi:application`.

Finally, add the import map to your base template:

```html
<!-- base.html -->
<!DOCTYPE html>
{% load esm %}
<html lang="en">
<head>
  <script type="importmap">{% importmap %}</script>
  <title>Django ESM is awesome!</title>
</head>
</html>
```

That's it!

### Development

Rebuild `STATIC_DIR` on every change:

```bash
python manage.py esm --watch
```

Run the development server in another terminal:

```bash
python manage.py runserver
```

### Treeshaking

By default, every package [entry point](https://nodejs.org/api/packages.html#package-entry-points)
ends up in the import map.
Pass `--treeshake` to drop entry points that are not reachable from your
project's own entry points, keeping only the outputs actually imported:

```bash
python manage.py esm --watch --treeshake
```

## Usage

You can now import JavaScript modules in your Django templates:

```html
<!-- index.html -->
{% block content %}
  <script type="module">
    import "lit"
  </script>
{% endblock %}
```

### Form.media

To use your importmap in Django forms, you can use the `Form.media` attribute:

```python
# forms.py
from django import forms
from django_esm.forms import ImportESModule


class MyForm(forms.Form):
    name = forms.CharField()

    class Media:
        js = [ImportESModule("@sentry/browser")]
```

Now `{{ form.media.js }}` will render to like this:

```html
<script type="module">import '@sentry/browser'</script>
```

### Private modules

You can also import private modules from your Django app:

```html
<!-- index.html -->
{% block content %}
  <script type="module">
    import "#myapp/js/my-module.js"
  </script>
{% endblock %}
```

To import a private module, prefix the module name with `#`.
You need to define your private modules in your `package.json` file:

```json
{
  "imports": {
    "#myapp/script": "./myapp/static/js/script.js",
    // You may use trailing stars to import all files in a directory.
    "#myapp/*": "./myapp/static/js/*"
  }
}
```

## How it works

Django ESM works via native JavaScript module support in modern browsers.
It uses the [import map](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script/type/importmap)
to map module names to their location on the server.

Here is an example import map. Entries resolve under `/esm/` and use
content-hashed names:

```json
{
  "imports": {
    "htmx.org": "/esm/node_modules/htmx.org/dist/htmx.min-<hash>.js"
  }
}
```
