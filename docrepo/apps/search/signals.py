from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.search.utils import index_document

from .models import DocumentIndex


@receiver(post_save, sender=DocumentIndex)
def index_document_handler(sender, instance, created, **kwargs):
    """
    Trigger index_document() when a new DocumentIndex is created.
    """
    if created:  # Only run when a new instance is created
        if settings.ENABLE_FULL_TEXT_SEARCH:
            index_document(instance)
