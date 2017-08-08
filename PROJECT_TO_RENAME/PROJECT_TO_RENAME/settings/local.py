import copy
from .base import *  # pylint: disable=W0614, W0401

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'MYSQL_NAME',
        'HOST': 'localhost',
        'PORT': '13306',
        'USER': 'MYSQL_USER',
        'PASSWORD': 'MYSQL_PASSWORD'
    }
}

CACHES = {
    "default": {
        "LOCATION": "redis://127.0.0.1:16379/0",
        "BACKEND": "django_redis.cache.RedisCache",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            "PASSWORD": "PASSWORD_TO_CHANGE",
        }
    }
}

# Default configuration for global logger
global_logger_conf = {  # pylint: disable=C0103
    'handlers': ['console'],
    'level': 'DEBUG',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        app: copy.deepcopy(global_logger_conf) for app in LOCAL_APPS
    }
}
