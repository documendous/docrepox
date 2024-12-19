# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
from config.settings.utils import BASE_DIR


VERSION = "v0.0.2"

ALLOWED_HOSTS = [
    "localhost",
]

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

if ENABLE_EXTENSIONS:
    TEMPLATES[0]["DIRS"].append(BASE_DIR / "extensions/templates")
