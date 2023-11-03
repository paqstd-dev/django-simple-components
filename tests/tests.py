from django.template.loader import render_to_string
from django.test import TestCase

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
            'dict': {'a': {'b': {'c': 123}}},
        }

        template = render_to_string('context.html', context)
        expected = """
            <p>['apple', 'banana', 'tomato'], banana</p>
            <p>django, g</p>
            <p>{'a': {'b': {'c': 123}}}, 123</p>
        """

        self.assertHTMLEqual(expected, template)

    def test_children(self):
        template = render_to_string('children.html')
        expected = """
           <div class="card">
                <h3>Test passed!</h3>
                <p>Description as children</p>
           </div>
        """

        self.assertHTMLEqual(expected, template)

    def test_slot(self):
        template = render_to_string('slot.html')
        expected = """
           <div class="card">
                <div class="card-body">
                    <p>Simple slot</p>
                </div>
           </div>
        """

        self.assertHTMLEqual(expected, template)

    def test_slots(self):
        template = render_to_string('slots.html')
        expected = """
           <div class="card">
                <div class="card-header">
                    <div class="d-flex">
                        <h3>Title</h3>
                    </div>
                </div>
                <div class="card-body">
                    <p>Simple slot</p>
                </div>
           </div>
        """

        self.assertHTMLEqual(expected, template)

    def test_slot_fallback(self):
        template = render_to_string('slot_fallback.html')
        expected = """
           <div class="card">
                <div class="card-header">
                    <h3>Default fallback title</h3>
                </div>
                <div class="card-body">
                    <p>Simple slot</p>
                </div>
           </div>
        """

        self.assertHTMLEqual(expected, template)

    def test_raise_tag_name_required(self):
        with self.assertRaises(exceptions.TagNameRequiredError):
            render_to_string('raise_set_component_name_required.html')
            render_to_string('raise_component_name_required.html')
            render_to_string('raise_slot_name_required.html')

    def test_raise_component_not_found(self):
        with self.assertRaises(exceptions.ComponentNotFoundError):
            render_to_string('raise_component_not_found.html')

    def test_raise_component_props(self):
        with self.assertRaises(exceptions.TagPropsArgumentError):
            render_to_string('raise_component_props.html')

    def test_raise_component_props_children(self):
        with self.assertRaises(exceptions.TagPropsChildrenError):
            render_to_string('raise_component_props_children.html')

    def test_raise_slot_not_found(self):
        with self.assertRaises(exceptions.SlotNotFoundError):
            render_to_string('raise_slot_not_found.html')
