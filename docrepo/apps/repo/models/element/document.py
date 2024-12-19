import logging
from django.conf import settings
from django.db import models
from apps.comments.models import Commentable
from apps.core.models import Element, HasFolderParent, IsRecyclable
from .version import Version
from .mimetype import Mimetype


class Document(Element, HasFolderParent, IsRecyclable, Commentable):
    """
    Element representing files with meta data
    """

    mimetype = models.ForeignKey(
        Mimetype,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        unique_together = (("name", "parent"),)
        indexes = [
            models.Index(fields=["parent"]),
            models.Index(fields=["mimetype"]),
            models.Index(fields=["created"]),
            models.Index(fields=["is_deleted"]),
        ]

    def get_full_path(self) -> str:
        """
        Returns full path to document
        """
        path = (  # pragma: no cover
            f"/{self.name}"
            if not self.parent
            else f"{self.parent.get_full_path()}/{self.name}"
        )
        return path  # pragma: no cover

    @property
    def current_version_tag(self) -> str:  # pragma: no cover
        """
        Returns latest version tag for document
        """
        versions = self.get_versions()
        if versions:
            return versions[0].tag
        else:
            return "Unknown"

    @property
    def current_version(self) -> Version | None:  # pragma: no cover
        """
        Returns latest version object for document if it exists
        """
        versions = self.get_versions()
        if versions:
            return versions[0]
        else:
            return None

    def get_versions(self):
        """
        Returns queryset list of all version objects for document
        """
        return Version.objects.filter(parent=self).order_by(
            "-created"
        )  # pragma: no cover

    def content_file_path(self) -> str:  # pragma: no coverage
        """
        Returns the relative path (minus the BASE_DIR) of the latest content file
        """
        log = logging.getLogger(__name__)
        versions = Version.objects.filter(parent=self).order_by("-created")
        if versions.exists():
            try:
                latest_version = versions[0]
                content_file_path = latest_version.content_file.path.replace(
                    str(settings.BASE_DIR), ""
                ).lstrip("/")
            except Exception as err:
                log.error(f"Missing content file for document id: {self.pk}: {err}")
                content_file_path = "--"

        return content_file_path

    def document_size(self) -> float:  # pragma: no coverage
        """
        Returns the size of a document
        """
        log = logging.getLogger(__name__)
        versions = Version.objects.filter(parent=self).order_by("-created")
        if versions.exists():
            try:
                latest_version = versions[0]
                document_size = latest_version.content_file.size
            except FileNotFoundError as err:
                log.error(f"Missing content file for document id: {self.pk}: {err}")
                document_size = 0

        return document_size

    @property
    def type(self) -> str:
        """
        Returns str type of this element
        """
        return "document"

    def __str__(self):
        return self.get_full_path()  # pragma: no cover
