"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

from .envtools import getenv

# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = getenv("SECRET_KEY", default="###SECRET_KEY###")

DEBUG = getenv("DEBUG", default=False, coalesce=bool)

ALLOWED_HOSTS = ["*"]

USE_X_FORWARDED_HOST = False
SESSION_COOKIE_HTTPONLY = True

SERVER_URL = os.getenv("SERVER_URL", default="*")


APPEND_SLASH = False

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_extensions"
]

LOCAL_APPS = [
    "backend_test.utils",
    "backend_test.users.apps.UsersAppConfig",
    "backend_test.menus.apps.MenusAppConfig"
]
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS

MIDDLEWARE = [
    "backend_test.middleware.HealthCheckAwareSessionMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "backend_test.middleware.HeaderNoCacheMiddleware",
]

ROOT_URLCONF = "backend_test.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend_test.wsgi.application"

# Users & Authentication
AUTH_USER_MODEL = 'users.User'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": getenv("POSTGRES_DEFAULT_DB", default="postgres"),
        "USER": getenv("POSTGRES_DEFAULT_USER", default="postgres"),
        "PASSWORD": getenv("POSTGRES_DEFAULT_PASSWORD", default="postgres"),
        "HOST": getenv("POSTGRES_DEFAULT_HOSTNAME", default="postgres"),
        "PORT": 5432,
        "CONN_MAX_AGE": 600,
        "DISABLE_SERVER_SIDE_CURSORS": True,
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}:6379/0".format(
            getenv("REDIS_CACHE_HOSTNAME", default="redis")
        ),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "../collected_static")
STATIC_URL = "/static/"

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ]
}

if getenv("BROWSABLE_API_RENDERER", default=False, coalesce=bool):
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = REST_FRAMEWORK[
        "DEFAULT_RENDERER_CLASSES"
    ] + ["rest_framework.renderers.BrowsableAPIRenderer"]

# APP SPECIFIC SETTINGS

# if getenv("SENTRY_DSN", default=None):
#    sentry_sdk.init(dsn=getenv("SENTRY_DSN"), integrations=[DjangoIntegration()])

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "fluent_formatter": {
            "()": "backend_test.logging_formatter.VerboseFluentRecordFormatter",
            "format": {
                "level": "%(levelname)s",
                "pathname": "%(pathname)s",
                "hostname": "%(hostname)s",
                "logger": "%(name)s",
                "module": "%(module)s",
                "funcname": "%(funcName)s",
                "namespace": os.getenv("KUBERNETES_NAMESPACE", "localhost"),
                "release": os.getenv("GIT_HASH", "local"),
            },
            "encoder_class": "django.core.serializers.json.DjangoJSONEncoder",
            "raise_on_format_error": DEBUG,
        },
        "simple": {
            "format": "[{asctime}] {levelname} {message}",
            "style": "{",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
    },
    "filters": {"require_debug_true": {"()": "django.utils.log.RequireDebugTrue"}},
    "handlers": {
        "sentry": {
            "level": "WARNING",
            "class": "sentry_sdk.integrations.logging.EventHandler",
        },
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "filters": ["require_debug_true"],
        },
        "fluent": {
            "class": "fluent.handler.FluentHandler",
            "host": os.getenv("FLUENT_HOST", "fluentbit"),
            "port": int(os.getenv("FLUENT_PORT", 24224)),
            "tag": os.getenv("FLUENT_TAG", "catalog"),
            "formatter": "fluent_formatter",
            "level": "INFO",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
    },
    "root": {"level": "WARNING", "handlers": ["sentry"]},
    "loggers": {
        "django": {"handlers": ["console"], "propagate": True},
        "django.db": {
            "handlers": ["console"],
            "propagate": False,
            "level": os.getenv("DB_LOGGING_LEVEL", "INFO"),
        },
        "django.server": {"handlers": ["django.server"], "propagate": False},
        "backend_test": {
            "handlers": ["fluent", "console"],
            "level": os.getenv("APP_LOGGING_LEVEL", "INFO"),
            "propagate": True,
        },
    },
}

SLACK = "https://hooks.slack.com/services/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"

# Admin
ADMIN_URL = 'admin/'
ADMINS = [
    ("""Pablo Trinidad""", 'pablotrinidad@ciencias.unam.mx'),
]
MANAGERS = ADMINS
ADMIN_ENABLED = True
