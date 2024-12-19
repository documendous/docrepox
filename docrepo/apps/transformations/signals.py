from django.dispatch import receiver
from django.db.models.signals import post_delete
from apps.core.utils.storage import delete_content_file
from apps.transformations.models import Preview


@receiver(post_delete, sender=Preview)
def auto_delete_file_on_delete(sender, instance, **kwargs):  # pragma: no coverage
    """
    Auto hard deletes preview content files when preview is deleted.
    """
    delete_content_file(instance)
