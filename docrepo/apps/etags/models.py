from django.db import models


class Tag(models.Model):
    """
    A tag for an element (folder, document or project)
    """

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Taggable(models.Model):
    """
    Taggable mixin, set by default for all elements (folder, document or project)
    """

    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        abstract = True
