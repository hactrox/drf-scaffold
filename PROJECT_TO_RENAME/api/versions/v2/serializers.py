from ...base import serializers as base_serializers
from ...models import Test


class TestListSerializer(base_serializers.TestListSerializer):
    class Meta(base_serializers.TestListSerializer.Meta):
        fields = ('id', 'field_for_v1', 'field_for_v2')
