from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.projects"

    def ready(self):
        from .signals import (  # noqa: F401
            create_or_update_project_folder,
            delete_project_objects,
        )
