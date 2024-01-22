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

Next, add a new staticfiles finder to your `STATICFILES_FINDERS` setting:

```python
# settings.py
STATICFILES_FINDERS = [
    # Django's default finders
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # django-esm finder
    "django_esm.finders.ESMFinder",
]
```

You will also need to expose your `node_modules` directory to Django's
staticfiles finder. You may run `npm ci --omit=dev` prior to running
`collectstatic` to avoid exposing your `devDependencies` publicly.

```python
# settings.py
from pathlib import Path

# add BASE_DIR (if not already present)
BASE_DIR = Path(__file__).resolve().parent.parent

STATICFILES_DIRS = [
    # …
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

### Testing (with Jest)

You can use the `django_esm` package to test your JavaScript modules with Jest.
Jest v27.4 and upwards will honor `imports` in your `package.json` file.

Before v27.4 that, you can try to use a custom `moduleNameMapper`, like so:

```js
// jest.config.js
module.exports = {
  // …
  moduleNameMapper: {
    '^#(.*)$': '<rootDir>/staticfiles/js/$1' // @todo: remove this with Jest >=29.4
  },
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
