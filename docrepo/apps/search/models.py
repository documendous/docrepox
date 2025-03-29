from django.db import models

from apps.core.models import UUIDPrimaryKeyModel
from apps.repo.models.element.document import Document


class DocumentIndex(UUIDPrimaryKeyModel):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    is_indexed = models.BooleanField(default=False)
    last_indexed = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Document Index"
        verbose_name_plural = "Document Indexes"

        indexes = [
            models.Index(fields=["document"]),
            models.Index(fields=["is_indexed"]),
            models.Index(fields=["last_indexed"]),
        ]

    def __str__(self):
        return self.document.get_full_path()
