import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.core.utils.storage import delete_content_file
from apps.repo.models.element.version import Version
from apps.repo.utils.system.user import create_user_home_folder, update_user_home_folder

from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Auto-creates a user profile and home folder when a user is created
    """
    if created:
        if instance.username != settings.ADMIN_USERNAME:
            Profile.objects.create(user=instance)
            create_user_home_folder(user=instance)
    else:
        update_user_home_folder(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.username != settings.ADMIN_USERNAME:
        instance.profile.save()


@receiver(post_delete, sender=Version)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Auto hard deletes version content files when parent document is deleted.
    """
    delete_content_file(instance)


log = logging.getLogger(__name__)

try:
    from extensions.apps.repo.signals import *  # noqa: F403, F401
except ModuleNotFoundError:  # pragma: no coverage
    log.warning("Expected module: 'signals' in extensions not found")
