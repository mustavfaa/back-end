from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def avatar(value):
    value = str(value)[6:]
    return value


@register.simple_tag
def in_admin(user):
    context = {}
    if 6 in user.groups.values_list('id', flat=True):
        context['con'] = 'container-fluid'
        context['col'] = 'col-md-9'
        return context
    else:
        context['con'] = 'container'
        context['col'] = 'col-md-12'
        return context