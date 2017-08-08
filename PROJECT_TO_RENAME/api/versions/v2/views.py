from ...base import views as base_view
from . import serializers as v2_serializers
from ...base.views import *


class TestViewSet(base_view.TestViewSet):
    serializer_class = v2_serializers.TestListSerializer
