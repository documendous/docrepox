from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models

from apps.core.models import Generic

User = get_user_model()


class Bookmark(Generic):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content_object = GenericForeignKey("content_type", "object_id")

    """
    Linking examples: each bookmark to a profile and its association:

    document = Document.objects.get(pk=document_id)
    bookmark = Bookmark.objects.create(
        profile=my_profile, content_object=document
    )
    """
