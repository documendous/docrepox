import logging
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Motd(models.Model):
    """Message of the day model"""

    title = models.CharField(max_length=100)
    content = models.TextField()
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        verbose_name = "MOTD"
        verbose_name_plural = "MOTDs"

    def __str__(self):
        return f"{self.title} by {self.owner.username}"


log = logging.getLogger(__name__)


if settings.ENABLE_EXTENSIONS:
    try:
        from extensions.apps.dashlets.models import *  # noqa: F403 F401
    except ModuleNotFoundError:
        log.warning("Expected module: 'models' in extensions not found")
