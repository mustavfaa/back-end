"""ekitaphana URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.functional import curry
from django.views.defaults import server_error, page_not_found

from django.conf.urls import url
from home.views import tech_view


from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
# handler404 = curry(page_not_found, template_name='errs/404.html')
# handler500 = curry(server_error, template_name='errs/500.html')

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    # path('api-auth/', include('rest_framework.urls')),
     path('', include('home.urls', namespace='home')),
    # path('cabinet/', include('schol_library.urls', namespace='schol_library')),
     path('account/', include('account.urls', namespace='account')),
    path('e-admin/', admin.site.urls),
    path('api/', include('schol_library.api_urls', namespace='schol_library_api')),

    # path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),

    # prefix_default_language=False,
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

tech = False

if tech:
    urlpatterns = [
        url(r'^', tech_view, ),
    ]
