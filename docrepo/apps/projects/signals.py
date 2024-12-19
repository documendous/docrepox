from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.projects.models import Project
from apps.projects.utils.project import (
    change_project_folder_name,
    create_project_folder,
    create_project_groups,
)


User = get_user_model()


@receiver(pre_save, sender=Project)
def capture_old_name(sender, instance, **kwargs):
    """
    Saves old name of project before creation
    """
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            instance._old_name = old_instance.name
        except sender.DoesNotExist:
            instance._old_name = None
    else:
        instance._old_name = None  # pragma: no coverage


@receiver(post_save, sender=Project)
def create_or_update_project_folder(sender, instance, created, **kwargs):
    """
    Creates project folder when a new project is created and when updating,
    changes the project folder's name accordingly
    """
    if created:
        create_project_groups(instance)
        create_project_folder(instance)

    elif hasattr(instance, "_old_name") and instance.name != instance._old_name:
        change_project_folder_name(instance)
