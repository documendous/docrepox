from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Avatar(models.Model):
    image_file = models.ImageField(upload_to="avatars/")

    # Generic relation fields
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.image_file.name


"""
Example usage:

from myapp.models import Avatar, UserProfile
from django.contrib.contenttypes.models import ContentType

# Creating a user profile
user = UserProfile.objects.create(name="John Doe")

# Attaching an avatar
avatar = Avatar.objects.create(
    image_file="path/to/image.jpg",
    content_type=ContentType.objects.get_for_model(user),
    object_id=user.id
)

# Get avatar from profile:

profile.get_avatar()

"""
