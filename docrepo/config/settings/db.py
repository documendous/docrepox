from .utils import env

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env("SQL_HOST"),
        "PORT": env("SQL_PORT"),
        "USER": env("SQL_USER"),
        "PASSWORD": env("SQL_PASSWORD"),
        "NAME": env("SQL_DATABASE"),
    }
}
