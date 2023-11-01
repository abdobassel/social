import os
from datetime import timedelta
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    ALLOWED_HOSTS=(list, []),
    INTERNAL_IPS=(list, []),
    DEBUG=(bool, False),
    DEBUG_TOOLBAR=(bool, False),
    EMAIL_BACKEND=(str, "django.core.mail.backends.console.EmailBackend"),
)
environ.Env.read_env(BASE_DIR / ".env")
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
DEBUG_TOOLBAR = env("DEBUG_TOOLBAR")
ALLOWED_HOSTS: list[str] = env("ALLOWED_HOSTS")
INTERNAL_IPS: list[str] = env("INTERNAL_IPS")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    #     3rd party libraries
    "rest_framework",
    "djoser",
    "django_extensions",
    "django_filters",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_countries",
    #     Local applications
    "social.users",
    "social.profiles",
    "social.posts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "project.urls"

# Enable the debug toolbar only in DEBUG mode.
if DEBUG and DEBUG_TOOLBAR:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = ["127.0.0.1"]

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
                "django.template.context_processors.request",
            ],
        },
    },
]

# As of Django 4.1, the cached loader is used in development mode.
# Runserver works around this in some manner, but Gunicorn does not.
# Override the loaders to get non-cached behavior.
if DEBUG:
    # app_dirs isn't allowed to be True when the loader key is present.
    TEMPLATES[0]["APP_DIRS"] = False
    TEMPLATES[0]["OPTIONS"]["loaders"] = [
        "django.template.loaders.filesystem.Loader",
        "django.template.loaders.app_directories.Loader",
    ]
WSGI_APPLICATION = "project.wsgi.application"

# Database https://docs.djangoproject.com/en/4.2/ref/settings/#databases django.db.backends.postgresql
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
    }
}
# Password validation https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images) https://docs.djangoproject.com/en/4.2/howto/static-files/
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
STATIC_ROOT = os.path.join(BASE_DIR / "static")
STATIC_URL = "/static/"
# STATICFILES_DIRS = [BASE_DIR / "staticfiles"]
MEDIA_ROOT = os.path.join(BASE_DIR / "media")
MEDIA_URL = "/media/"

# Default primary key field type https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# django-allauth
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
AUTH_USER_MODEL = "users.User"
# LOGIN_REDIRECT_URL = "/"
SIDE_ID = 1
# Authentication cookies and JWT
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "JWT_ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "JWT_REFRESH_TOKEN_LIFETIME": timedelta(days=14),
}
AUTH_COOKIE = "access"
AUTH_COOKIE_MAX_AGE = 60 * 60 * 24 * 14  # 14 days
AUTH_COOKIE_SECURE = env("AUTH_COOKIE_SECURE")
AUTH_COOKIE_HTTP_ONLY = env("AUTH_COOKIE_HTTP_ONLY")
AUTH_COOKIE_PATH = "/"
AUTH_COOKIE_SAMESITE = "None"  # Strict if we have the same domain

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "social.users.authentications.CustomJWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),  # IsAuthenticated
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": ("rest_framework.parsers.JSONParser",),
}
DJOSER = {
    "PASSWORD_RESET_CONFIRM_URL": "password-reset/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": True,
    "ACTIVATION_URL": "activation/{uid}/{token}",
    "USER_CREATE_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "TOKEN_MODEL": None,
}
# django-extensions
GRAPH_MODELS = {
    "app_labels": ["users", "profiles", "posts"],
    "rankdir": "BT",
    "output": "models.png",
}
