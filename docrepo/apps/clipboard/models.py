from django.contrib.auth import get_user_model
from django.db import models

from apps.repo.models.element.document import Document
from apps.repo.models.element.folder import Folder

User = get_user_model()


class PastedDocument(models.Model):
    """
    A document currently pasted in the user's clipboard
    """

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        blank=True,
    )
    pasted_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.document.get_full_path()


class PastedFolder(models.Model):
    """
    A folder currently pasted in the user's clipboard
    """

    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, blank=True)
    pasted_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.folder.get_full_path()


class Clipboard(models.Model):
    """
    Collection for user's current pasted documents and folders
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    documents = models.ManyToManyField(PastedDocument, blank=True)
    folders = models.ManyToManyField(PastedFolder, blank=True)

    def __str__(self):
        return self.user.username
