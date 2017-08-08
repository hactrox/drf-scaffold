import datetime
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password
from core.models import LastLoginInfoModel


class UserManager(BaseUserManager):
    def create_user(self, username, password):
        if username is None:
            raise ValueError('必须输入用户名')
        if password is None:
            raise ValueError('必须输入密码')

        user = self.model(username=username)
        user.password = make_password(password)
        user.last_login_time = datetime.datetime.now()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username=username, password=password)
        user.save(using=self._db)


class User(LastLoginInfoModel):
    username = models.CharField(max_length=20, unique=True, error_messages={
        'unique': '用户名已存在'
    })
    password = models.CharField(max_length=255)
    nickname = models.CharField(max_length=20)
    register_time = models.DateTimeField(auto_now_add=True)
    # Used for jwt authentication
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'
    is_anonymous = False
    is_authenticated = True

    class Meta:
        db_table = 'user'

    def __str__(self):
        return "%s" % self.username


class Test(models.Model):
    field_for_v1 = models.CharField(max_length=100)
    field_for_v2 = models.CharField(max_length=80)

    class Meta:
        db_table = 'test'
