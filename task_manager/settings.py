"""
Django settings for task_manager project.
"""

import os
import sys
from datetime import timedelta
from pathlib import Path

import dj_database_url
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# Core Security
# ============================================================

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-only-secret-key-change-this",
)


DEBUG = (
    os.environ.get(
        "DJANGO_DEBUG",
        "False",
    ).lower()
    == "true"
)


ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1",
).split(",")


# Railway fallback
ALLOWED_HOSTS += [
    "web-production-e9601c.up.railway.app",
]


# ============================================================
# Applications
# ============================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "crispy_forms",
    "crispy_bootstrap5",
    "accounts",
    "tasks",
    "rest_framework",
    "drf_spectacular",
    "api",
]


# ============================================================
# Middleware
# ============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "task_manager.urls"


# ============================================================
# Templates
# ============================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "builtins": [
                "django.templatetags.i18n",
                "django.templatetags.static",
            ],
        },
    },
]


WSGI_APPLICATION = "task_manager.wsgi.application"


# ============================================================
# Database
# ============================================================

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}


# ============================================================
# Password Validation
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ============================================================
# Localization
# ============================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Tehran"

USE_I18N = True

USE_TZ = True


LANGUAGES = [
    ("en", _("English")),
    ("fa", _("Persian")),
]


LOCALE_PATHS = [
    BASE_DIR / "locale",
]


# ============================================================
# Static Files
# ============================================================

STATIC_URL = "/"

STATIC_ROOT = BASE_DIR / "staticfiles"


STATICFILES_DIRS = [
    BASE_DIR / "static",
]


STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# ============================================================
# Crispy Forms
# ============================================================

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"


# ============================================================
# Default
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


LOGIN_REDIRECT_URL = "tasks:task_list"

LOGOUT_REDIRECT_URL = "accounts:login"

LOGIN_URL = "accounts:login"


# ============================================================
# Django REST Framework
# ============================================================

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}


# ============================================================
# Swagger / OpenAPI
# ============================================================

SPECTACULAR_SETTINGS = {
    "TITLE": "Django Task Manager API",
    "DESCRIPTION": "REST API for Django Task Manager",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
}


# ============================================================
# JWT
# ============================================================

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,
}


# ============================================================
# Production Security
# ============================================================


RUNNING_TESTS = (
    "PYTEST_CURRENT_TEST" in os.environ
    or "pytest" in os.path.basename(sys.argv[0]).lower()
    or "test" in sys.argv
)


if not DEBUG and not RUNNING_TESTS:

    SECURE_SSL_REDIRECT = (
        os.getenv(
            "DJANGO_SECURE_SSL_REDIRECT",
            "False",
        ).lower()
        == "true"
    )

    SESSION_COOKIE_SECURE = (
        os.getenv(
            "DJANGO_SESSION_COOKIE_SECURE",
            "True",
        ).lower()
        == "true"
    )

    CSRF_COOKIE_SECURE = (
        os.getenv(
            "DJANGO_CSRF_COOKIE_SECURE",
            "True",
        ).lower()
        == "true"
    )

    SECURE_HSTS_SECONDS = int(
        os.getenv(
            "DJANGO_SECURE_HSTS_SECONDS",
            "31536000",
        )
    )

    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SECURE_HSTS_PRELOAD = True


# Railway Proxy Support

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)


USE_X_FORWARDED_HOST = True
