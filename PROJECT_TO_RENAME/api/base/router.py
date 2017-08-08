from django.conf.urls import url
from rest_framework import routers
from . import views


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'test', views.TestViewSet)


api_urlpatterns = [
    url(r'^user/reg$', views.UserCreateView.as_view()),
]


api_urlpatterns += router.urls
