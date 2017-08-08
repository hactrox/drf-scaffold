from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken
from . import errors
from .exceptions import Error
from .utils import get_client_ip


def jwt_response_payload_handler(token, user=None, request=None):
    ip_addr = get_client_ip(request)
    now = datetime.now()
    user.update_last_login_info(now, ip_addr)

    return {
        'token': token
    }


class CustomObtainJSONWebToken(ObtainJSONWebToken):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        error_code = errors.VALIDATION_ERROR
        error = 'Unable to log in with provided credentials.'
        msg = '用户名或密码不正确'
        status_code = status.HTTP_400_BAD_REQUEST
        raise Error(error_code, error, msg, status_code)

custom_obtain_jwt_token = CustomObtainJSONWebToken.as_view()