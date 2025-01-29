import logging

from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate

from apps.core.utils.db import table_exists

logger = logging.getLogger(__name__)


class RepoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.repo"

    def ready(self):
        from .signals import (
            auto_delete_file_on_delete,
            create_user_profile,
            save_user_profile,
        )

        # Connect post_migrate signal
        post_migrate.connect(self._post_migrate_handler, sender=self)

        # Call directly during startup if migrations are applied
        if not settings.ADMIN_ALLOW_ALL:
            self._delete_admin_project_bookmarks()

    def _post_migrate_handler(self, *args, **kwargs):  # pragma: no coverage
        """
        Handler executed after migrations to delete admin bookmarks
        for projects where the admin is not a member.
        """
        if not settings.ADMIN_ALLOW_ALL:
            self._delete_admin_project_bookmarks()

    def _delete_admin_project_bookmarks(self):  # pragma: no coverage
        """
        Deletes all bookmarks related to the Project model for the admin user
        where the admin is not a member of the project.
        """
        if not table_exists("django_content_type"):
            logger.debug(
                "Skipping _delete_admin_project_bookmarks: ContentType table does not exist."
            )
            return

        try:
            from django.contrib.contenttypes.models import ContentType

            from apps.bookmarks.models import Bookmark
            from apps.projects.models import Project
            from apps.repo.utils.system.object import get_admin_user

            project_content_type = ContentType.objects.get_for_model(Project)
            admin_user = get_admin_user()

            if admin_user:
                bookmarks = Bookmark.objects.filter(
                    owner=admin_user, content_type=project_content_type
                )

                bookmarks_to_delete = []
                for bookmark in bookmarks:
                    project = Project.objects.filter(id=bookmark.object_id).first()
                    if project and not project.is_member(admin_user):
                        bookmarks_to_delete.append(bookmark.id)

                deleted_count, _ = Bookmark.objects.filter(
                    id__in=bookmarks_to_delete
                ).delete()
                logger.debug(
                    f"Deleted {deleted_count} bookmarks for projects the admin is not a member of."
                )
        except Exception as e:
            logger.error(f"Error deleting bookmarks for admin user: {e}")
