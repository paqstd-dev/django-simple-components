# Django Simple Components

Django Simple Components is a small package to easily create components inside your templates without saving them in the templates folder.

## Quick start

0. Install package from pypi:
```bash
pip install django-simple-components
```

1. Add `simple_components` to your INSTALLED_APPS setting like this:
```python
INSTALLED_APPS = [
    ...,
    "simple_components",
]
```

2. Add `simple_components` to your template like this:
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

3. Hooray! Everything is ready to use it.

## Contributing
If you would like to suggest a new feature, you can create an issue on the GitHub repository for this project. 
If you'd like to contribute code, you can fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.
