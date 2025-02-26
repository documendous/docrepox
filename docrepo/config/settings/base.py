# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
from .utils import env

VERSION = "24.4.2"

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost"])

ROOT_URLCONF = "config.urls"

ENABLE_EXTENSIONS = False  # Enable customization extensions

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
                "apps.repo.context_processors.global_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
