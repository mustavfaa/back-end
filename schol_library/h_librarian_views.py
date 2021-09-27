from account.models import AccessToEdit
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .valid_view import head_librarian
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from .models import PlannedTitle, Year
from portfoli.models_core import DateObjects


# Формирование планового титула школы
@method_decorator(user_passes_test(head_librarian, login_url='home:index'), name='dispatch')
class PlannedTitleCreateView(TemplateView):
    template_name = 'schol_library/head_librarian/planned_title_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = list(set(PlannedTitle.objects.filter(school=self.request.user.libraryuser.school).values_list('year', flat=True)))
        context['years'] = DateObjects.objects.filter(pk__in=year)
        context['len'] = len(year)
        return context


# плановый титул школы
@method_decorator(user_passes_test(head_librarian, login_url='home:index'), name='dispatch')
class PlannedTitleListView(ListView):
    template_name = 'schol_library/head_librarian/planned_title_list.html'
    model = PlannedTitle
    context_object_name = 'tituls'

    def get_queryset(self):
        if self.kwargs.get('pk'):
            qs = self.model.objects.filter(year_id=self.kwargs['pk'], school=self.request.user.libraryuser.school)
            return qs
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = list(set(
            PlannedTitle.objects.filter(school=self.request.user.libraryuser.school).values_list('year', flat=True)))
        context['years'] = DateObjects.objects.filter(pk__in=year)
        context['year'] = DateObjects.objects.get(pk=self.kwargs.get('pk'))
        context['len'] = len(year)
        return context


# Портфель
@method_decorator(user_passes_test(head_librarian, login_url='home:index'), name='dispatch')
class BriefcaseView(TemplateView):
    template_name = 'schol_library/head_librarian/briefcase.html'


# Реестр потребностей
@method_decorator(user_passes_test(head_librarian, login_url='home:index'), name='dispatch')
class ConsolidatedRegistryView(TemplateView):
    template_name = 'schol_library/head_librarian/need_consolidate.html'

