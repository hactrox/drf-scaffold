from django.contrib.auth.hashers import check_password
from api.models import User


class CustomBackend(object):
    def authenticate(self, request, username=None, password=None):
        if username is not None and password is not None:
            try:
                user = User.objects.get(username__exact=username)
                password_valid = check_password(password, user.password)
                if password_valid:
                    return user
            except User.DoesNotExist:
                return None
        return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            return None
