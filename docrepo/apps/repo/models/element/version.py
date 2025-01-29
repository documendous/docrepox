from django.db import models

from apps.core.models import ContentFileModel, TimestampedModel, UUIDPrimaryKeyModel
from apps.repo.settings import DEFAULT_DOCUMENT_VERSION


class Version(
    TimestampedModel, UUIDPrimaryKeyModel, ContentFileModel
):  # pragma: no coverage
    """
    File version for document
    """

    parent = models.ForeignKey(
        "Document", on_delete=models.CASCADE, null=True, blank=True
    )
    tag = models.CharField(
        "Version number", max_length=20, default=DEFAULT_DOCUMENT_VERSION
    )

    class Meta:
        unique_together = ("parent", "tag")
        verbose_name = "Document Version"
        verbose_name_plural = "Document Versions"

    def __str__(self):
        return f"{self.content_file.name}|{self.tag}"

    @property
    def size(self):
        try:
            return self.content_file.size
        except FileNotFoundError:
            return 0
