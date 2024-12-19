from django.apps import AppConfig


class RepoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.repo"

    def ready(self):
        from .signals import (
            auto_delete_file_on_delete,
            create_user_profile,
            save_user_profile,
        )
