from django.db import models


class Mimetype(models.Model):  # pragma: no coverage
    """
    Mimetype model for Document
    """

    name = models.CharField(max_length=200, unique=True)
    extension_list = models.CharField(max_length=200)

    def __str__(self):
        return self.name
