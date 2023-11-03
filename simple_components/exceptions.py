from django import template


class TagNameRequiredError(template.TemplateSyntaxError):
    def __init__(self, tag_name, example):
        self.message = '\'%s\' takes at least one required argument "name":\n%s' % (
            tag_name,
            example,
        )
        super().__init__(self.message)


class TagPropsArgumentError(template.TemplateSyntaxError):
    def __init__(self, bit, example):
        self.message = 'Argument %s must be takes as params:\n%s' % (bit, example)
        super().__init__(self.message)


class TagPropsChildrenError(template.TemplateSyntaxError):
    def __init__(self, name):
        self.message = (
            'The parameter \'%s\' cannot be specified in props because it is built-in '
            'and cannot be overridden in this way.' % name
        )
        super().__init__(self.message)


class ComponentNotFoundError(template.TemplateSyntaxError):
    def __init__(self, name):
        self.message = (
            'The component \'%s\' has not been previously defined. '
            'Check that the component is named correctly.' % name
        )
        super().__init__(self.message)


class SlotNotFoundError(template.TemplateSyntaxError):
    def __init__(self, name, *args):
        self.message = 'Expected slot with name \'%s\'!' % name
        super().__init__(self.message)
