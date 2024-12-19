from django.apps import AppConfig
from django.conf import settings


class ClipboardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.clipboard"

    def ready(self):
        if settings.DELETE_CLIPBOARD_ON_LOGOUT:
            from .signals import clear_user_clipboard  # noqa F401
