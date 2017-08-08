"""PROJECT_TO_RENAME URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500  # pylint: disable=W0611
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_swagger.views import get_swagger_view
from api.base.router import api_urlpatterns as api_v1
from api.versions.v2.router import api_urlpatterns as api_v2
from core.jwt import custom_obtain_jwt_token
from core.exceptions import custom404, custom500
from .settings import base as base_settings


handler404 = custom404  # pylint: disable=C0103
handler500 = custom500  # pylint: disable=C0103


schema_view = get_swagger_view(title='PROJECT_TO_RENAME API')  # pylint: disable=C0103


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^token$', custom_obtain_jwt_token),
    url(r'refresh-token$', refresh_jwt_token),
    url(r'^v1/', include(api_v1, namespace='v1')),
    url(r'^v2/', include(api_v2, namespace='v2')),
    url(r'^$', schema_view),
]

urlpatterns += static(base_settings.MEDIA_URL, document_root=base_settings.MEDIA_ROOT)
