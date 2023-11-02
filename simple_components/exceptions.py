from django import template


class SetComponentNameError(template.TemplateSyntaxError):
    pass


class ComponentNameError(template.TemplateSyntaxError):
    pass


class ComponentArgsError(template.TemplateSyntaxError):
    pass


class ComponentNotDefined(template.TemplateSyntaxError):
    pass
