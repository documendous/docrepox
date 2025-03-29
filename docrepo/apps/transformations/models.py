from django.db import models

from apps.core.models import ContentFileModel, TimestampedModel, UUIDPrimaryKeyModel


class Rendition(TimestampedModel, UUIDPrimaryKeyModel, ContentFileModel):
    version = models.ForeignKey("repo.Version", on_delete=models.CASCADE)

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["version"]),
            models.Index(fields=["content_file"]),
            models.Index(fields=["created"]),
            models.Index(fields=["modified"]),
        ]


class Preview(Rendition):  # pragma: no coverage

    def __str__(self):
        return f"{self.content_file.name}|{self.version.content_file.name}|{self.version.tag}"


class Thumbnail(Rendition):  # pragma: no coverage

    def __str__(self):
        return f"{self.content_file.name}|{self.version.content_file.name}|{self.version.tag}"
