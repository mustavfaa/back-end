from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Count
from django.http import HttpResponse
from django.utils import translation
from .models import AccessToEdit, LibraryUser
from portfoli import models as p_models
from django.shortcuts import redirect
from schol_library.models import NumberBooks, Edition
from django.http import JsonResponse
from . import serializers


def get_school(request):
    is_admin = request.user.groups.filter(id=6).exists()
    if is_admin or request.user.is_superuser:
        u = LibraryUser.objects.get(user=request.user)
        if request.GET.get('pk'):
            u.create_school_id = int(request.GET.get('pk'))
            u.save()
        else:
            u.create_school = None
            u.save()
    return redirect('account:dashboard')


# Список школ
def get_right_school_menu(request, context):
    school_menu = cache.get('left_school_menu_' + translation.get_language())
    school_menu = None
    if school_menu == None:
        school_types_for_render = p_models.SchoolType.objects.filter(show_at_site=True, deleted=False).order_by('sort')
        for item in school_types_for_render:
            item.my_schools = item.get_my_schools()
            item.my_schools_len = item.my_schools.__len__()
            item.teacher_len = 0
            for sch in item.my_schools:
                sch.teacher_len = 0
                wtls = sch.portfolioworktimeline_set.filter(current=True,
                                                            portfolio__deleted=False,
                                                            checked=True,
                                                            uvolen=False,
                                                            deleted=False).values(
                    'portfolio').annotate(kount=Count('portfolio', distinct=True))

                for wtl in wtls:
                    sch.teacher_len = sch.teacher_len + wtl['kount']
                    item.teacher_len = item.teacher_len + wtl['kount']

        groups = []
        for item in school_types_for_render:
            group = item.group
            if item.group is None:
                groups.append({
                    'group': False,
                    'data': item
                })
            else:
                ind = None
                for i in range(0, groups.__len__()):
                    if groups[i]['group'] and groups[i]['data'] == item.group:
                        ind = i
                        break
                if ind is None:
                    groups.append({
                        'group': True,
                        'data': item.group,
                        'list': [item],
                        'my_schools_len': item.my_schools_len,
                        'teacher_len': item.teacher_len
                    })
                else:
                    groups[ind]['list'].append(item)
                    groups[ind]['my_schools_len'] = groups[ind]['my_schools_len'] + item.my_schools_len
                    groups[ind]['teacher_len'] = groups[ind]['teacher_len'] + item.teacher_len

        context['groups'] = groups
        school_menu = render(request, 'account/school_left_menu.html', context).content
        cache.set('left_school_menui_' + translation.get_language(), school_menu)
    context['school_menu'] = school_menu.decode('utf-8')
    return context


@login_required
def dashboard(request):
    context = {}
    context['section'] = 'dashboard'
    context['is_admin'] = request.user.groups.filter(id=6).exists()
    if request.user.groups.filter(id=6).exists():
        context = get_right_school_menu(request, context)
    else:
        context
    return render(request, 'account/dashboard.html', context)


@login_required
def delete_caches(request):
    if request.user.is_superuser:
        cache.delete('Editedsru')
        cache.delete('Editedskk')
        cache.delete('edsru')
        cache.delete('edskk')
        cache.delete('titulru')
        cache.delete('titulkk')
        cache.delete('briefcases')
        return HttpResponse('<h1>Кэш очищен!</h1>')
    else:
        return HttpResponse('<h1>НЕТ Доступа!</h1>')


@login_required
def access_edit_create(request):
    if request.user.is_superuser:
        schools = list(set(p_models.AlmaMater.objects.all().values_list('id', flat=True)))
        for i in schools:
            item = AccessToEdit.objects.filter(school__id=i).first()
            if item:
                item.edit_status = 1
                item.save()
            else:
                school = p_models.AlmaMater.objects.get(id=i)
                create_item = AccessToEdit.objects.create(school=school, edit_status=1)
                create_item.save()
        return HttpResponse('<h1>Всем школам добавлен возможность редактировать, а у кого не было создана модель!</h1>')
    else:
        return HttpResponse('<h1>НЕТ Доступа!</h1>')


@login_required
def create_library(request):
    if request.user.is_superuser:
        recs = p_models.PortfolioWorkTimeLine.objects.filter(deleted=False,
                                                             current=True,
                                                             uvolen=False,
                                                             checked=True,
                                                             positions__in=[152, 107],
                                                             school__nash=True)

        for rec in recs:
            items = LibraryUser.objects.filter(school=rec.school, user=rec.portfolio.user)
            if items.__len__() == 0:
                item = LibraryUser()
                item.school = rec.school
                item.user = rec.portfolio.user
                item.save()

        return HttpResponse('<h1>Метод сработал!</h1>')
    else:
        return HttpResponse('<h1>НЕТ Доступа!</h1>')


def touch_user(request):
    user = request.user
    if user.is_authenticated:
        if user.is_superuser or request.user.groups.filter(id=6).exists():
            user.is_admin = True
        return JsonResponse(serializers.UserSerializers(user).data)
    return HttpResponse(status=401)
