from django.urls import path
from .views import HeadOfScienceView, HeadLibrarianView, HeadEditLibrarianView, InvoiceView, PaperInvoiceView, \
    Invoices, RequestEditionView, ActWriteOffView, InitialBalanceView, BooksOrderView,GetNewInitialBalanceView
from .api import number_books_list, number_books_delete, add_number_books, school_titul_list, \
    add_school_titul, school_titul_delete, editions_list, demo_add_number_books
from schol_library import api, views, librian_views, h_librarian_views, hl_api
from .utils import all_editions
from django.views.generic.base import TemplateView
from account.api import NewGetSchool

app_name = 'schol_library'
urlpatterns = [
                  path('getexel/', hl_api.getexel, name="getexel"),
                  # Бибилотекарь
                  path('librarian/', api.LibraryBooksAPIList.as_view(), name='librarian'),
                  path('librarian/class_list/', librian_views.ClassListView.as_view(), name='l_class_list'),
                  path('librarian/books_list/', api.LibraryBooksAPIList.as_view(), name='l_books_list'),
              ] + [
                  # Кабинет Зав директора
                  path('head_science/', HeadOfScienceView.as_view(), name='head_science'),
                  path('head_science/school_titul_list/', school_titul_list, name='hc_school_titul_list'),
                  path('head_science/api/school_titul/add/', add_school_titul, name='hc_add_school_titul'),
                  path('head_science/api/delete/<int:pk>', school_titul_delete, name='hc_school_titul_delete'),
              ] + [
                  # Demo Кабинет зав.библиотекоря
                  path('head_librarian/api/books/demo/', number_books_list, name='hl_number_books'),
                  path('head_librarian/api/books/add/demo/', add_number_books, name='hl_add_number_books'),
                  path('head_librarian/api/books/delete/<int:pk>/', number_books_delete, name='hl_number_books_delete'),
                  # number_books_delete удаление и редактирование
              ] + [
                  # кабинет зав.библиотекоря
                  path('head_librarian/', HeadLibrarianView.as_view(), name='head_librarian'),
                  path('head_librarian/edit/', HeadEditLibrarianView.as_view(), name='hl_edit_books'),
                  path('head_librarian/list/', api.BooksAPIList.as_view()),
                  path('head_librarian/editions_list/', editions_list),
                  path('head_librarian/briefcase/', h_librarian_views.BriefcaseView.as_view(), name='hl_briefcase'),
                  path('head_librarian/briefcase/api/', hl_api.BriefcaseAPI.as_view()),

                  # Роли для пользователей
                  path('head_librarian/roles/', views.RoleAssignment.as_view(), name='hl_edit_role'),
                  path('head_librarian/roles/api/', api.RoleAssignmentAPI.as_view(), name='hl_api_edit_role'),
                  path('head_librarian/roles/api/end/', api.RoleEndAPI.as_view(), name='hl_api_edit_role_end'),
                  # Создание планового титула
                  path('head_librarian/planned_title_create/',
                       h_librarian_views.PlannedTitleCreateView.as_view(),
                       name='hl_planned_title_create'),
                  path('head_librarian/planned_title_create/api/', hl_api.PlannedTitleCreateAPI.as_view(),
                       name='hl_planned_title_create_api'),
                  path('head_librarian/planned_title_list/api/list/', hl_api.PlannedTitleListEditAPI.as_view()),
                  path('head_librarian/planned_title_list/<int:pk>', h_librarian_views.PlannedTitleListView.as_view(),
                       name='hl_planned_list'),
                  path('head_librarian/consolidated_registry/', h_librarian_views.ConsolidatedRegistryView.as_view(),
                       name='hl_consolidated_registry'),
                  path('head_librarian/consolidated_registry/api/', hl_api.ConsolidatedRegistry.as_view()),
                  # path('head_librarian/planned_title_create/api/list/', hl_api.ListPlannedTitlesYearAPI.as_view())
                  # INVOICE
                  path('head_librarian/invoices/', Invoices.as_view(), name="hl_invoices"),
                  path('head_librarian/invoice/', InvoiceView.as_view(), name="hl_invoice"),
                  path('head_librarian/paper_invoice/', PaperInvoiceView.as_view(), name="hl_paper_invoice"),
                  path('head_librarian/act_write_off/', ActWriteOffView.as_view(), name='act_write_off_invoice'),
                  path('head_librarian/initial_balance/', InitialBalanceView.as_view(), name='initial_balance'),
                  path('head_librarian/initial_balance/', InitialBalanceView.as_view(), name='initial_balance'),
                  path('head_librarian/books_order/', BooksOrderView.as_view(), name='books_order'),
                  path('head_librarian/request_edition/', RequestEditionView.as_view(), name="request_edition"),
                  path('test/', all_editions),
                  # API
                  path('api/edition_list/', views.EditionListView.as_view()),
                  path('api/school_list/', NewGetSchool.as_view()),
                  path('api/paper_invoice/', views.NewPaperInvoiceView.as_view(), ),
                  path('api/initial_balance/', views.NewInitialBalanceView.as_view(), ),
                  path('api/act_write_off/', views.NewActWriteOffView2.as_view(), ),
                  path('api/books_order/', views.BooksOrderView.as_view(), ),
                  path('api/books_order_global/', views.BookOrdersGlobalList.as_view(), ),
                  path('api/books_recall/', views.BooksRecallView.as_view(), ),
                  path('api/all_ost/', views.get_all_ost, ),
                  path('api/get_demand/', views.get_demand, ),
                  path('api/school_titul/', views.SchoolTitul.as_view(), ),
                  path('head_librarian/act_write_off/get_ost/', views.get_ost),
                  path('superuser/change_editions_by_id', views.change_editon_set),


                  # path('api/frqYhKSfeB/', views.cron_register_number_books, name='cron_register_500_nb'),
                  # path('api/NzhDGWIWJB/', views.clear_register, name='save_all_NB')
                  # path('NYhDGWIWJW/', views.clear_up_nb, name='numberbook_clear')
              ]
