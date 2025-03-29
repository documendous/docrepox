from django.contrib.auth import get_user_model
from django.db import models

from apps.core.models import ActivatedModel, TimestampedModel
from apps.repo.models.element.document import Document

User = get_user_model()


class ProxiedDocument(TimestampedModel, ActivatedModel):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta(TimestampedModel.Meta, ActivatedModel.Meta):
        unique_together = (("document", "manager"),)

    def __str__(self):
        return self.document.get_full_path()
