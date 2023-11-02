from django.test import TestCase
from django.template.loader import render_to_string

from simple_components import exceptions


class ComponentTestCase(TestCase):
    def test_setup_component(self):
        template = render_to_string('setup.html')
        expected = ''

        self.assertHTMLEqual(expected, template)

    def test_components_with_string_values(self):
        template = render_to_string('strings.html')
        expected = """
            <p>a, b, c</p>
            <p>1, 2, 3</p>
            <p>'abc',  ?,  </p>
        """

        self.assertHTMLEqual(expected, template)

    def test_components_with_newlines_props(self):
        template = render_to_string('newlines.html')
        expected = """
            <div>
                <h3>Hello</h3>
                <p>World</p>
                ...
            </div>
        """

        self.assertHTMLEqual(expected, template)

    def test_components_with_context(self):
        context = {
            'list': ['apple', 'banana', 'tomato'],
            'string': 'django',
            'dict': {
                'a': {
                    'b': {
                        'c': 123
                    }
                }
            }
        }

        template = render_to_string('context.html', context)
        expected = """
            <p>['apple', 'banana', 'tomato'], banana</p>
            <p>django, g</p>
            <p>{'a': {'b': {'c': 123}}}, 123</p>
        """

        self.assertHTMLEqual(expected, template)

    def test_raise_set_component_name(self):
        with self.assertRaises(exceptions.SetComponentNameError):
            render_to_string('raise_set_component_name.html')

    def test_raise_component_name(self):
        with self.assertRaises(exceptions.ComponentNameError):
            render_to_string('raise_component_name.html')

    def test_raise_component_not_found(self):
        with self.assertRaises(exceptions.ComponentNotDefined):
            render_to_string('raise_component_not_found.html')

    def test_raise_component_args(self):
        with self.assertRaises(exceptions.ComponentArgsError):
            render_to_string('raise_component_args.html')
