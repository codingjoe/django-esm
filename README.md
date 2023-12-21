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
pip install django-esm
```

```python
# settings.py
INSTALLED_APPS = [
    # …
    'django_esm',
]
```

Next, add the `node_modules` directory to your staticfiles directories:

```python
# settings.py
STATICFILES_DIRS = [
    BASE_DIR / "node_modules",
]
```

Finally, add the import map to your base template:

```html
<!-- base.html -->
<!DOCTYPE html>
{% load esm %}
<html lang="en">
<head>
  <script type="importmap">{% importmap %}</script>
</head>
</html>
```

That's it!
Don't forget to run `npm install` and `python manage.py collectstatic`.

## Usage

You can now import JavaScript modules in your Django templates:

```html
<!-- index.html -->
{% block content %}
  <script type="module">
    import "htmx.org"
    htmx.logAll()
  </script>
{% endblock %}
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
