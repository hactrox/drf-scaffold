import logging
from rest_framework.request import Request


log = logging.getLogger(__name__)


def extract_request_info(request):
    if not isinstance(request, Request):
        log.error("Type of argument 'request' must be 'Request', but actually got [%s]", type(request))
        return None

    info = {
        'path': request.path,
        'method': request.method,
    }

    if request.data:
        info['data'] = request.data
    if request.auth:
        info['user'] = request.user

    return info

def extract_exception_info(exc, context):
    request = context['request']
    info = {
        'exception': exc,
        'view': context['view'].__class__.__name__,
        'path': request.path,
        'method': request.method,
    }

    if request.data:
        info['data'] = request.data
    if request.auth:
        info['user'] = request.user

    return info
