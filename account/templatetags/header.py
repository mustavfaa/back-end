from django import template
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

register = template.Library()


@login_required
@register.inclusion_tag('includes/account_header.html')
def header(user):
    context = {'error': 0}
    try:
        user = User.objects.get(id=user.id)
    except User.DoesNotExist:
        context['error'] = 1
        return context
    context['list_groups'] = [x for x in user.groups.values_list('id', flat=True)]
    return context


@login_required
@register.inclusion_tag('account/dashboard_menu.html')
def simple_header(user):
    context = {'error': 0}
    try:
        user = User.objects.get(id=user.id)
    except User.DoesNotExist:
        context['error'] = 1
        return context

    context['list_groups'] = [x for x in user.groups.values_list('id', flat=True)]
    return context
