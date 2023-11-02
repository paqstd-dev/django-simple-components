import re

from django import template

from ..exceptions import (
    ComponentArgsError,
    ComponentNameError,
    ComponentNotDefined,
    SetComponentNameError,
)

# allow line breaks inside tags
template.base.tag_re = re.compile(template.base.tag_re.pattern, re.DOTALL)

register = template.Library()


@register.tag
def set_component(parser, token):
    nodelist = parser.parse(('end_set_component',))
    parser.delete_first_token()

    bits = token.split_contents()
    if len(bits) < 2:
        raise SetComponentNameError(
            '\'%s\' takes at least one argument (name of component)' % bits[0]
        )

    component_name = str(parser.compile_filter(bits[1]))

    return SetComponentNode(component_name, nodelist)


class SetComponentNode(template.Node):
    def __init__(self, component_name, nodelist):
        self.component_name = component_name
        self.nodelist = nodelist

    def render(self, context):
        if 'components' not in context:
            context['components'] = {}
        context['components'][self.component_name] = self.nodelist

        return ''


@register.tag
def component(parser, token):
    bits = token.split_contents()
    if len(bits) < 2 or "=" in bits[1]:
        example = '{% component "name" ' + ' '.join(bits[1:]) + ' %}'
        raise ComponentNameError(
            'Component takes at least one required argument (name of component):\n%s'
            % example
        )

    component_name = str(parser.compile_filter(bits[1]))

    kwargs = {}
    bits = bits[2:]
    for bit in bits:
        match = re.compile(r'(?:(\w+)=)?(.+)').match(bit)

        name, value = match.groups()
        if name:
            kwargs[name] = parser.compile_filter(value)
        else:
            example = (
                '{% component "' + component_name + '" param1=%s' % bit + ' ... %}'
            )
            raise ComponentArgsError(
                'Argument %s must be takes as kwargs:\n%s' % (bit, example)
            )

    return ComponentNode(component_name, kwargs)


class ComponentNode(template.Node):
    def __init__(self, component_name, kwargs=None):
        self.component_name = component_name
        self.kwargs = kwargs

    def render(self, context):
        try:
            nodelist = context['components'][self.component_name]
        except KeyError:
            raise ComponentNotDefined(
                'The component \'%s\' has not been previously defined. '
                'Check that the component is named correctly.' % self.component_name
            )

        if self.kwargs is not None:
            for key, value in self.kwargs.items():
                context[key] = value.resolve(context)
        return nodelist.render(context)
