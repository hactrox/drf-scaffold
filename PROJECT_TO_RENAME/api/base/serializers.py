import re
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.settings import settings
from ..models import Test, User


class UserListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'nickname', 'register_time')


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

    def validate_username(self, value):
        if not re.compile('^[a-zA-Z0-9_]{3,20}$').match(value):
            raise ValidationError("用户名格式不正确")

        # TODO: Check if the username is in blocklist

        return value

    def validate_password(self, value):
        if settings.DEBUG:
            return value

        if len(value) < 8:
            raise ValidationError("密码长度不能小于 8 位数")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        user = User.objects.create_user(username, password)
        return user

    def update(self, instance, validated_data):
        error_code = METHOD_NOT_ALLOWED
        error = "Action 'update' on this serializer is not allowed"
        msg = "系统开了个小差"
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise Error(error_code, error, msg, status_code)

class TestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('id', 'field_for_v1')
