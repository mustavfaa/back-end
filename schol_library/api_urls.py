from django.urls import path
from .views import HeadOfScienceView, HeadLibrarianView, HeadEditLibrarianView, InvoiceView, PaperInvoiceView, \
    Invoices, RequestEditionView, ActWriteOffView, InitialBalanceView, BooksOrderView
from .api import number_books_list, number_books_delete, add_number_books, school_titul_list, \
    add_school_titul, school_titul_delete, editions_list, demo_add_number_books
from schol_library import api, views, librian_views, h_librarian_views, hl_api
from .utils import all_editions
from django.views.generic.base import TemplateView
from account.api import NewGetSchool, LoginView
from . import api_views

app_name = 'schol_library'
urlpatterns = [
    path('superuser/change_editions_by_id/', views.change_editon_set),
    # API FOR NEW FRONT
    path('my_schools/', api_views.LibraryCurrentWorkTimeLinesViewAPI.as_view(), ),

    path('goto_webinar/', api_views.goto_webinar, ),
    path('has_webinar/', api_views.has_webinar, ),
    path('initial_balance/', api_views.InitialBalanceViewAPI.as_view(), ),
    path('income_invoices/', api_views.PaperInvoiceViewAPI.as_view(), ),
    path('act_write_off/', api_views.ActWriteOffViewAPI.as_view(), ),
    path('books_order/', api_views.BooksOrderViewAPI.as_view(), ),
    path('school_titul/', api_views.SchoolTitulAPI.as_view(), ),
    path('school_titul_planned/', api_views.SchoolTitulPlannedAPI.as_view(), ),
    path('school_titul_planned/build/', api_views.school_titul_planned_build, ),
    path('school_titul/list/', api_views.SchoolTitullList.as_view(), ),
    path('school_titul_list/', api_views.school_titul_list, ),
    path('school_titul_planned_list/', api_views.school_titul_planned_list, ),
    path('users_by_school/', api_views.users_by_school, ),
    path('brief_case/', api_views.BriefcaseAPI.as_view(), ),
    path('books_order_global/', api_views.BookOrdersGlobalList.as_view(), ),
    path('get_schools/', api_views.GetSchool.as_view(), ),
    path('school_list/', api_views.NewGetSchool.as_view(), ),
    path('books_recall/', api_views.BooksRecallView.as_view(), ),
    path('edition_list/', views.EditionListView.as_view()),
    path('act_write_off/get_ost/', views.get_ost),
    path('all_ost/', views.get_all_ost, ),
    path('get_demand/', views.get_demand, ),
    # path('kontingent/', views.KontingentView.as_view(), ),
    path('login/', LoginView.as_view()),


    path('pagination/article/', api_views.GetNewInitialBalanceView.as_view()),


    path('import_editions/', api_views.ImportBooksList.as_view()),
    path('import_ost/', api_views.ImportOst.as_view()),
    path('admin_books_moving/', api_views.AdminBooksMoving.as_view()),
    path('books_moving/', api_views.BooksMoving.as_view()),
    path('cat_ver/', api_views.cat_ver),
    path('when_ready/', api_views.when_ready),

]
