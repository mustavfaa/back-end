from django import template

register = template.Library()


@register.filter(name='class_len')
def class_len(value):
    return value.name[:7]


@register.simple_tag
def calculation(val1, val2):
    a = round(((val2 - val1) / val1) * 100, 2)
    return a