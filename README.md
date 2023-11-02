# Django Simple Components
[![PyPI version](https://img.shields.io/pypi/v/django-simple-components)](https://pypi.python.org/pypi/django-simple-components/)
[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/django-simple-components.svg)](https://pypi.python.org/pypi/django-simple-components/)
[![PyPI Supported Django Versions](https://img.shields.io/pypi/djversions/django-simple-components.svg)](https://pypi.python.org/pypi/django-simple-components/)
[![Coverage)](https://codecov.io/github/paqstd-dev/django-simple-components/graph/badge.svg)](https://app.codecov.io/github/paqstd-dev/django-simple-components)

Django Simple Components is a small package to easily create components inside your templates without saving them in the templates folder.

## Quick start

### 1. Install package:
To get started, install the package from [pypi](https://pypi.org/project/django-simple-components/):
```bash
pip install django-simple-components
```

Now you can add `simple_components` to your django project. Change your `INSTALLED_APPS` setting like this:
```python
INSTALLED_APPS = [
    ...,
    "simple_components",
]
```

Optionally, you can specify `simple_components` as builtins and this will be available in any of your templates without additionally specifying `{% load simple_components %}`:
```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "builtins": ["simple_components.templatetags.simple_components"],
        },
    },
]
```
If you choose not use it as a built-in, you will need to add `{% load simple_components %}` to the top of your template whenever you want to use simple components.

### 2. Create component inside your template:
```html
{% load simple_components %}

{% set_component "first_component" %}
    <div class="card">
        <h3>{{ title }}</h3>
        <p>{{ description }}</p>
    </div>
{% end_set_component %}

<div class="card-list">
    {% component "first_component" title="Hello world!" description="Some text..." %}
    {% component "first_component"
        title="Some lines"
        description="Other text..."
    %}

    {% with value="this text will be capitalized later" %}
        {% component "first_component" title=123 description=value|capfirst %}
    {% endwith %}
</div>
```

### 3. Hooray! Everything is ready to use it.

## Contributing
If you would like to suggest a new feature, you can create an issue on the GitHub repository for this project.
Also you can fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.
