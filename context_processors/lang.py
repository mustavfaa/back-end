from django.template.defaultfilters import stringfilter
from django import template

register = template.Library()


@register.inclusion_tag('includes/header.html')
def get_lang(request):
    context = {}
    context['lang'] = request.path[4:]
    return context
