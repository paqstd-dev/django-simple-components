import re
from django import template

# allow line breaks inside tags
template.base.tag_re = re.compile(template.base.tag_re.pattern, re.DOTALL)

register = template.Library()


@register.tag
def set_component(parser, token):
    nodelist = parser.parse(('end_set_component',))
    parser.delete_first_token()

    bits = token.split_contents()
    if len(bits) < 2:
        raise template.TemplateSyntaxError(
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
    if len(bits) < 2:
        raise template.TemplateSyntaxError(
            '\'%s\' takes at least one argument (name of component)' % bits[0]
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
            raise template.TemplateSyntaxError(
                '\'%s\' must be takes as kwargs' % bit
            )

    return ComponentNode(component_name, kwargs)


class ComponentNode(template.Node):
    def __init__(self, component_name=None, kwargs=None):
        if component_name is None:
            raise template.TemplateSyntaxError(
                'Component template nodes must be given a name to return.'
            )

        self.component_name = component_name

        if kwargs is None:
            kwargs = {}

        self.kwargs = kwargs

    def render(self, context):
        try:
            nodelist = context['components'][self.component_name]
        except KeyError:
            raise template.TemplateSyntaxError(
                'The component \'%s\' has not been previously defined.Check that the component is named correctly.'
                % self.component_name
            )

        for key, value in self.kwargs.items():
            context[key] = value.resolve(context)
        return nodelist.render(context)
