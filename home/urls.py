from django.urls import path
from .views import home
from django.contrib.auth.views import logout_then_login

app_name = 'home'
urlpatterns = [
    path('', home, name='index'),
    path('logout/', logout_then_login, {'login_url': 'home:index'}, name='logout')
]
