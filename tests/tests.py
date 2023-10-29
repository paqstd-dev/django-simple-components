from django.test import TestCase
from django.template.loader import render_to_string


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
