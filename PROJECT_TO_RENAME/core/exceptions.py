import logging
from rest_framework import status
from rest_framework import exceptions
from rest_framework.compat import set_rollback
from django.http import JsonResponse
from . import errors


log = logging.getLogger(__name__)


def custom404(request):

    error_code = errors.NOT_FOUND
    error = {
        'request_path': request.path
    }
    msg = '资源不存在'
    status_code = status.HTTP_404_NOT_FOUND

    log.info('request path does not exist: %s', request.path)

    return error_response(error_code, error, msg, status_code)


def custom500(request):  # pylint: disable=W0613
    error_code = errors.SYSTEM_ERROR
    error = 'Internal Server Error'
    msg = '系统繁忙'
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return error_response(error_code, error, msg, status_code)


class Error(Exception):
    def __init__(self, error_code, err_message, message, status_code, headers=None):
        super(Error, self).__init__()
        self.error_code = error_code
        self.err_message = err_message
        self.message = message
        self.status_code = status_code
        self.headers = headers

    def __str__(self):
        return u'[Error] %d: %s(%d)' % (self.error_code, self.err_message, self.status_code)

    def get_response(self):
        return error_response(self.error_code, self.err_message, self.message, self.status_code, self.headers)


def error_response(error_code, err_message, message, status_code, headers=None):
    err = {
        'error_code': error_code,
        'error': err_message,
        'message': message,
    }
    response = JsonResponse(err, status=status_code)

    if headers:
        for header, value in headers.items():
            response[header] = value

    return response


def get_error_detail(error_obj):
    if isinstance(error_obj, list):
        return error_obj[0]
    elif isinstance(error_obj, dict):
        return next(iter(error_obj.values()))[0]
    else:
        return '出现错误'


def custom_exception_handler(exc, context):  # pylint: disable=W0613

    if isinstance(exc, Error):
        set_rollback()
        error_code = exc.error_code
        error = exc.err_message
        msg = exc.message
        status_code = exc.status_code
        return error_response(error_code, error, msg, status_code)

    if isinstance(exc, exceptions.PermissionDenied):
        set_rollback()
        error_code = errors.PERMISSION_DENIED
        error = exc.detail
        msg = '您没有对应的权限'
        status_code = status.HTTP_403_FORBIDDEN
        return error_response(error_code, error, msg, status_code)

    if isinstance(exc, exceptions.NotAuthenticated):
        set_rollback()
        error_code = errors.NOT_AUTHENTICATED
        error = exc.detail
        msg = '登录信息已失效'
        status_code = status.HTTP_401_UNAUTHORIZED
        return error_response(error_code, error, msg, status_code)

    if isinstance(exc, exceptions.MethodNotAllowed):
        set_rollback()
        error_code = errors.METHOD_NOT_ALLOWED
        error = exc.detail
        msg = '不允许的指令'
        status_code = status.HTTP_405_METHOD_NOT_ALLOWED
        return error_response(error_code, error, msg, status_code)

    if isinstance(exc, exceptions.ValidationError):
        set_rollback()
        error_code = errors.VALIDATION_ERROR
        error = exc.detail
        msg = get_error_detail(exc.detail)
        status_code = status.HTTP_400_BAD_REQUEST
        return error_response(error_code, error, msg, status_code)

    if isinstance(exc, exceptions.AuthenticationFailed):
        set_rollback()
        error_code = errors.AUTHENTICATION_FAILED
        error = exc.detail
        msg = '用户名或密码不正确'
        status_code = status.HTTP_401_UNAUTHORIZED
        return error_response(error_code, error, msg, status_code)

    log.exception(exc)
