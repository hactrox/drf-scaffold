from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class LastLoginInfoModel(models.Model):
    last_login_time = models.DateTimeField()
    last_login_ip = models.GenericIPAddressField(null=True)

    class Meta:
        abstract = True

    def update_last_login_info(self, login_time, login_ip):
        self.last_login_time = login_time
        self.last_login_ip = login_ip
        self.save(update_fields=['last_login_time', 'last_login_ip'])
