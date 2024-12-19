from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Comment(models.Model):
    """
    Comment for element
    """

    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-created",)


class Commentable(models.Model):
    """
    Mixin to allow comments for a model (by default set for Document, Folder, Projects)
    """

    comments = models.ManyToManyField(Comment, blank=True)

    class Meta:
        abstract = True
