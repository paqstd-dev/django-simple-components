import re

from django import template
from django.template.base import Node, NodeList

from ..exceptions import (
    ComponentNotFoundError,
    SlotNotFoundError,
    TagNameRequiredError,
    TagPropsArgumentError,
    TagPropsChildrenError,
)

# allow line breaks inside tags
template.base.tag_re = re.compile(template.base.tag_re.pattern, re.DOTALL)

register = template.Library()


def _get_params(parser, bits, builtin_tag_name, tag_name):
    params = {}
    for bit in bits:
        match = re.compile(r'(?:(\w+)=)?(.+)').match(bit)

        name, value = match.groups()
        if name:
            # check built-in parameter
            if name == 'children':
                raise TagPropsChildrenError(name)
            params[name] = parser.compile_filter(value)
        else:
            # fmt: off
            example = (
                '{% ' + builtin_tag_name + ' "' + tag_name +
                '" param1=%s' % bit + ' ... %}'
            )
            # fmt: on
            raise TagPropsArgumentError(bit, example)

    return params


class _CreateTag:
    def __init__(
        self, name: str, inline: bool = False, closable: bool = False, prefix: str = ''
    ):
        self.tag_name = name
        self._prefix = prefix
        self._inline = inline
        self._closable = closable

    def __call__(self, function):
        def create_tag(parser, token):
            tag_name, *bits = token.split_contents()

            if self._closable and tag_name[0] == self._prefix:
                # Block components start with `#` or '@'
                # Expect a closing tag
                nodelist = parser.parse((f"/{tag_name[1:]}",))
                parser.delete_first_token()
            else:
                # Inline component
                nodelist = NodeList()

            if len(bits) < 1 or '=' in bits[0]:
                example = '{% ' + tag_name + ' "custom_name" %}'
                raise TagNameRequiredError(tag_name, example)

            element_name = bits[0]
            params = _get_params(parser, bits[1:], self.tag_name, tag_name)

            class SimpleNode(Node):
                def __init__(self, element_name: str, nodelist: NodeList, params: dict):
                    self.element_name = element_name
                    self.nodelist = nodelist
                    self.params = params

                def render(self, context):
                    return function(self, context)

            return SimpleNode(element_name, nodelist, params)

        if self._inline:
            register.tag(self.tag_name, create_tag)
        if self._closable:
            register.tag(self._prefix + self.tag_name, create_tag)


create_tag = _CreateTag


@create_tag('set_component', prefix="#", closable=True)
def set_component_closable(cls, context):
    # setup component nodelist for render later
    if 'components' not in context:
        context['components'] = {}
    context['components'][cls.element_name] = cls.nodelist

    return ''


@create_tag('component', prefix="#", inline=True, closable=True)
def component_closable(cls, context):
    try:
        nodelist = context['components'][cls.element_name]
    except KeyError:
        raise ComponentNotFoundError(cls.element_name)

    if cls.params is not None:
        for key, value in cls.params.items():
            context[key] = value.resolve(context)

    # setup children if exist
    if cls.nodelist:
        context['children'] = cls.nodelist.render(context)

    return nodelist.render(context)


@create_tag('set_slot', prefix='@', inline=True, closable=True)
def set_slot_closable(cls, context):
    children = None

    try:
        children = context['slots'][cls.element_name]
    except KeyError:
        if not cls.nodelist:
            raise SlotNotFoundError(cls.element_name)

    if children is not None:
        return children.render(context)
    return cls.nodelist.render(context)


@create_tag('slot', prefix='@', closable=True)
def slot_closable(cls, context):
    if 'slots' not in context:
        context['slots'] = {}
    context['slots'][cls.element_name] = cls.nodelist

    return ''
