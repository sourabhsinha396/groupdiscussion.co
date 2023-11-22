from django import template

register = template.Library()

@register.filter(name='space_to_code')
def space_to_code(value):
    return value.replace(' ', '%20')