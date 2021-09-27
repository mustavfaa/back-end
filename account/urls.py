from django.urls import path
from .views import dashboard, delete_caches, access_edit_create, create_library, get_school
from account import api, views
from schol_library import hl_api

app_name = 'account'
urlpatterns = [
    path('api/login/', api.LoginView.as_view()),
    path('api/touch_user/', views.touch_user),
    path('api/get_schools/', api.GetSchool.as_view()),
    path('', dashboard, name='dashboard'),
    path('cash/delete/my/', delete_caches),
    path('access_edit_create/admin/', access_edit_create),
    path('create_library/', create_library),
    path('api/close/page/', api.ClosePage.as_view()),
    path('get_brif_100/', hl_api.get_brif_100),
    path('get_school/', get_school, name="get_school"),
]
