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
You can define a base component that can be reused later. For example:
```html
{% load simple_components %}

{% #set_component "card" %}
    <div class="card">
        <h3>{{ title }}</h3>
        <p>{{ description }}</p>
    </div>
{% /set_component %}

<div class="card-list">
    {% component "card" title="Post 1" description="..." %}
    {% component "card" title="Post 2" description="..." %}
    {% component "card" title="Post 3" description="..." %}
</div>
```

You can also use named slots to change the contents of a component as quickly as possible:
```html
{% load simple_components %}

{% #set_component "profile" %}
    <div class="profile">
        <div class="avatar">
            {% @set_slot "avatar" %}
                <!-- fallback username as bdage -->
                <span class="badge">{{ username.0 }}</span>
            {% /set_slot %}
        </div>
        <div class="info">
            {{ username }}
        </div>
    </div>
{% /set_component %}

{% #set_component "card" %}
    <div class="card">
        {% set_slot "image" %}

        <h3>{{ title }}</h3>
        <p>{{ description }}</p>
    </div>
{% /set_component %}

<div class="page">
    {% component "profile" username="Default" %}

    <div class="card-list">
        {% #component "card" title="Post 1" description="..." %}
            {% @slot "image" %}
                <img src="..." alt="slot image" />
            {% /slot %}
        {% /component %}
    </div>
</div>
```
### 3. Hooray! Everything is ready to use it.

## Template syntax
### Create component
To define a component you need to use the Django tag `{# set_component name %}` where name is the name of the component,
listed in quotes. This is a paired tag, which means it needs to be closed:
```html
{% #set_component "card" %}
    <p>{{ title }}</p>
{% /set_component %}
```

### Use component
In the example above, we defined the "card" component and specified a variable that will be used during rendering later.
Now, to use this component, you just need to write:
```html
{% component "card" title="Post" %}
```

Components can also render children - anything specified between the opening and closing `component` tags:
```html
{% #set_component "card" %}
    <div class="c1 c2 c3 c4 c5">
        <p>{{ title }}</p>
        {{ children }}
    </div>
{% /set_component %}

{% #component "card" title="Post" %}
    <p>Simple</p>
    <p>Content</p>
{% /component %}
```

### Create slots
Slots are a powerful opportunity to upgrade your components! Slots can accept any content.
Each slot has a name, and is specified inside the set_component tag:
```html
{% #set_component "card" %}
    <div class="card">
        <div class="card-header">
            <h3>{{ title }}</h3>
        </div>
        <div class="card-body">
            {% set_slot "body" %}
        </div>
    </div>
{% /set_component %}
```

Any slot can have a fallback template, which will be displayed if this slot was not passed to the component.
Otherwise, a `SlotNotFoundError` will be raised:
```html
{% @set_slot "custom" %}
    fallback
{% /set_slot %}
```

### Use slots
To use slots in components, you need to pass the slot when rendering where it is needed:
```html
{% #set_component "card" %}
    <div class="card">
        ...
        <div class="card-body">
            {% set_slot "body" %}
        </div>
    </div>
{% /set_component %}

{% #component "card" %}
    {% @slot "body" %}
        render slot inside card-body class
    {% /slot %}
{% /component %}
```

### Summarize
All paired tags in simple components close with `%{ /tag %}`, where `tag` can be `set_component`, `set_slot`, `component`.

There are `{% component %}` and `{% set_slot %}` which can be defined on the same line. For the component,
this means that it cannot use slots and children. For `set_slot` this means that the fallback template is not specified:
```html
{% component "card" title="Post" description="..." %}
```
```html
{% set_slot "avatar" %}
```

To define a component or use it, you can specify `#` at the beginning of the tag (only for closable tags):
```html
{% #set_component name="simple" %}
    {{ children }}
{% /set_component %}
```
```html
{% #component name="simple" %}
    component with children content
{% /component %}
```

To define a slot or use it, you can specify `@` at the beginning of the tag (only for closable tags):
```html
{% @set_slot "custom" %}
    fallback
{% /set_slot %}
```
```html
{% @slot "custom" %}
    render slot
{% /slot %}
```

## Contributing
If you would like to suggest a new feature, you can create an issue on the GitHub repository for this project.
Also you can fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.
