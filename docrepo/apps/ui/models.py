from django.contrib.auth import get_user_model
from django.db import models

from apps.core.models import KeyValuePairModel

User = get_user_model()


class Setting(KeyValuePairModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("key", "user"),)
        verbose_name = "UI Setting"
        verbose_name_plural = "UI Settings"

    def __str__(self):
        return f"{self.user.username} | {self.key}: {self.value}"
