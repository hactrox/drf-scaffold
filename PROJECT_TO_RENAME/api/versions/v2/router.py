from rest_framework import routers
from . import views


router = routers.DefaultRouter(trailing_slash=False) # pylint: disable=C0103

router.register(r'test', views.TestViewSet)

api_urlpatterns = router.urls # pylint: disable=C0103
