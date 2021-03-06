"""
Django settings for musicavis project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from pathlib import Path
import mimetypes
from dotenv import load_dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT = Path(__file__).resolve().parent.parent

BASE_TEMPLATES_DIR = f"{ROOT}/app/frontend/templates/app"

load_dotenv(f"{ROOT}/.env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "you-will-never-guess")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "0.0.0.0",
    "localhost",
    "127.0.0.1",
    "192.168.0.117",
    "www.musicavis.ca",
    "musicavis.ca",
]

CSRF_COOKIE_SECURE = not DEBUG

SECURE_HSTS_SECONDS = False

# Application definition

INSTALLED_APPS = [
    "app.apps.AppConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "webpack_loader",
    "channels",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "musicavis.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_TEMPLATES_DIR,],
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

WSGI_APPLICATION = "musicavis.wsgi.application"

ASGI_APPLICATION = "musicavis.routing.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "OPTIONS": {"read_default_file": f"{ROOT}/db.conf"},
        "TEST": {"NAME": "musicavis_test"},
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
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

STATIC_ROOT = f"{ROOT}/static/"

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    f"{ROOT}/app/frontend/static/app/",
    f"{ROOT}/app/frontend/static/app/assets",
]

EXPORTS_DIR = f"{STATIC_ROOT}/exports"

# Session
#

SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # One month

SESSION_COOKIE_SECURE = False  # if DEBUG else True

SESSION_SAVE_EVERY_REQUEST = True

SESSION_COOKIE_NAME = "musicavis-session"

# Webpack
#

WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "BUNDLE_DIR_NAME": "bundles/",
        "STATS_FILE": os.path.join(BASE_DIR, "webpack-stats.json"),
        "POLL_INTERVAL": 0.1,
        "TIMEOUT": None,
        "IGNORE": [r".+\.hot-update.js", r".+\.map"],
        "LOADER_CLASS": "webpack_loader.loader.WebpackLoader",
    }
}

LOGIN_URL = "/login/"

LOGIN_REDIRECT_URL = "/"

# MimeTypes
#

MIMETYPES = mimetypes.MimeTypes()
MIMETYPES.add_type(
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document", ".docx"
)
MIMETYPES.add_type(
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", ".xlsx"
)
MIMETYPES.add_type("application/vnd.oasis.opendocument.text", ".odt")
MIMETYPES.add_type("application/vnd.oasis.opendocument.spreadsheet", ".ods")

# Celery
#

BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE

CELERY_EMAIL_TASK_CONFIG = {
    "queue": "email",
    "rate_limit": "50/m",
    "name": "djcelery_email_send",
    "ignore_result": True,
}

# Email
#

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("MAIL_SERVER", "smtp.googlemail.com")
EMAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
EMAIL_HOST_USER = os.environ.get("MAIL_USERNAME")
EMAIL_HOST_PASSWORD = os.environ.get("MAIL_PASSWORD")
EMAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", True)

MUSICAVIS_ADMIN = os.environ.get("MUSICAVIS_ADMIN", "macpoule@gmail.com")
MUSICAVIS_MAIL_SUBJECT_PREFIX = "[Musicavis]"
MUSICAVIS_MAIL_SENDER = f"Musicavis Admin <{MUSICAVIS_ADMIN}>"

if DEBUG:
    BASE_URL = "http://127.0.0.1:8000"
else:
    BASE_URL = "https://www.musicavis.ca"

# Channels
#

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [("127.0.0.1", 6379)],},
    },
}
