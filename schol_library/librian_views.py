from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from .valid_view import librarian, llibrarian_or_head


@method_decorator(user_passes_test(llibrarian_or_head, login_url='home:index'), name='dispatch')
class LibrarianView(TemplateView):
    template_name = 'schol_library/librarian/librarian.html'


@method_decorator(user_passes_test(llibrarian_or_head, login_url='home:index'), name='dispatch')
class ClassListView(TemplateView):
    template_name = 'schol_library/librarian/class_list.html'
