from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.core.models import TimestampedModel

User = get_user_model()


class Communication(TimestampedModel):
    """
    Model used for communication between users in the application
    """

    msg_from = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comm_msg_from"
    )
    msg_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comm_msg_to"
    )
    category = models.CharField(max_length=24, choices=settings.COMMS_CATEGORY_CHOICES)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True
    )
    object_id = models.UUIDField(null=True, blank=True)
    related_element = GenericForeignKey()

    def __str__(self):
        return f"From: {self.msg_from} To: {self.msg_to} Subj: {self.subject}"

    """
    Model used for communication between users in the application

    Usage examples:

    # Create a general communication without any relation
    communication = Communication.objects.create(
        msg_from=sender,
        msg_to=recipient,
        category="message",
        subject="General Update",
        content="This is a general message"
    )

    # Create a communication linked to a specific project
    project = Project.objects.get(pk=project_id)
    communication = Communication.objects.create(
        msg_from=sender,
        msg_to=recipient,
        category="notification",
        subject="Project Update",
        content="Important project message",
        related_element=project
    )

    # Query communications for a specific element
    project_communications = Communication.objects.filter(
        content_type__model="project",
        object_id=project.id
    )

    # Query standalone communications (no related element)
    standalone_messages = Communication.objects.filter(
        content_type__isnull=True
    )
    """
