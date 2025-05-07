# Django ESM

NextGen JavaScript ESM module support for Django.

[![PyPi Version](https://img.shields.io/pypi/v/django-esm.svg)](https://pypi.python.org/pypi/django-esm/)
[![Test Coverage](https://codecov.io/gh/codingjoe/django-esm/branch/main/graph/badge.svg)](https://codecov.io/gh/codingjoe/django-esm)
[![GitHub License](https://img.shields.io/github/license/codingjoe/django-esm)](https://raw.githubusercontent.com/codingjoe/django-esm/master/LICENSE)

## Highlights

* easy transition
* smart cache busting
* no more bundling
* native ESM support
* local vendoring with npm

## Setup

Install the package and add it to your `INSTALLED_APPS` setting:

```bash
pip install django-esm[whitenoise]
```

First, add `django_esm` to your `INSTALLED_APPS` settings:

```python
# settings.py
INSTALLED_APPS = [
    # …
    "django_esm",  # add django_esm before staticfiles
    "django.contrib.staticfiles",
]
```

Optionally: If you are using whitenoise you will need to modify your WSGI application.

```python
import os
import pathlib

from django.core.wsgi import get_wsgi_application

from django_esm.wsgi import ESM

BASE_DIR = pathlib.Path(__file__).parent.parent

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

application = ESM(get_wsgi_application())
```

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
Remember to run `npm install` and `python manage.py esm --watch`.

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

Here is an example import map:

```json
{
  "imports": {
    "htmx.org": "/static/htmx.org/dist/htmx.min.js"
  }
}
```
