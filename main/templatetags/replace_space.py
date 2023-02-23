from django import template

register = template.Library()


@register.filter(name='replace_space')
def replace_space(value):
    return value.replace(' ', '_')
