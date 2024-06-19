import os

import environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env.local"), overwrite=False)

DEBUG = env.bool("DEBUG", default=False)

SECRET_KEY = env.str("SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

ROOT_URLCONF = "photoroom.urls"
APPEND_SLASH = True

USE_TZ = True
USE_I18N = True
TIME_ZONE = "UTC"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    "django.contrib.admin",
    "django.contrib.sessions",
    "photoroom",
    "rest_framework",
    "rest_framework.authtoken",
    "colorfield",
]

DATABASES = {
    "default": {
        "OPTIONS": {
            "application_name": "django",
        },
        **env.db("DATABASE_URL", default="postgres:///photoroom"),
        # Ensure all views are wrapped in a transaction
        "ATOMIC_REQUESTS": True,
        # Use long-lived connections to avoid paying the cost
        # of re-establishing it frequently.
        "CONN_MAX_AGE": None,
        # Disable server-side cursors to ensure compatibility
        # with transaction-level connection pooling
        "DISABLE_SERVER_SIDE_CURSORS": True,
        "TEST": {
            "name": "photoroom-test",
        },
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    },
]

STATIC_URL = "static/"
STATICFILES_DIRS: list[str] = []
STATIC_ROOT = os.path.join(BASE_DIR, "public")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

REST_FRAMEWORK = {
    "DEFAULT_VERSION": "1.0",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny"
        # "rest_framework.permissions.DjangoModelPermissions"
    ],
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.AcceptHeaderVersioning",
    "DEFAULT_RENDERER_CLASSES": [
        "photoroom.renderers.VendoredJSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
}
