from django.apps import AppConfig


class TransformationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.transformations"

    def ready(self):
        from .signals import auto_delete_file_on_delete
