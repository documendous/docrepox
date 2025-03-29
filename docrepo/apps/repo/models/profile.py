from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from apps.avatars.models import Avatar
from apps.repo.models.element import Folder

User = get_user_model()


class Profile(models.Model):
    """
    Associated profile for user - auto-created when a user is added to the system
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    home_folder = models.ForeignKey(
        Folder, on_delete=models.SET_NULL, null=True, blank=True
    )

    avatar = GenericRelation(Avatar)

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["home_folder"]),
        ]

    @property
    def recycle_folder(self) -> Folder:
        """
        User's recycle folder
        """
        recycle_folder = Folder.objects.get(
            name="Recycle",  # Hard-coded purposely
            parent=self.home_folder,
        )

        return recycle_folder

    def is_admin_user(self) -> bool:
        """
        Returns True if user is the system admin user
        """
        return self.user.username == settings.ADMIN_USERNAME

    def get_avatar_url(self):
        avatar = self.avatar.first()
        return avatar.image_file.url if avatar else None

    def __str__(self):
        return self.user.username  # pragma: no cover
