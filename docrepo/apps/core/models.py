import uuid
from functools import cached_property

from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, models

from apps.core.utils.storage import content_file_name
from apps.etags.models import Taggable
from apps.repo.utils.helpers import update_with_new_name

User = get_user_model()


class TimestampedModel(models.Model):
    """
    Allows for auto timestamps on associated models
    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDPrimaryKeyModel(models.Model):
    """
    UUID primary key for associated models. Ensures uniqueness
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class HasFolderParent(models.Model):
    """
    Sets parent folder for elements (folders and documents)
    """

    parent = models.ForeignKey(
        "Folder", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        abstract = True


class HasOwner(models.Model):
    """
    Sets owner for associated models
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Generic(models.Model):
    """
    Base Generic model type
    """

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    object_id = models.UUIDField(null=True, blank=True)

    class Meta:
        abstract = True


class Element(
    TimestampedModel, UUIDPrimaryKeyModel, HasOwner, Taggable
):  # pragma: no coverage
    """
    Base model for repository objects
    """

    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def is_recycle_folder(self) -> bool:
        """
        Returns True/False if folder is a recycle folder
        """
        if self.type == "folder" and self.name == "Recycle":
            return True

        return False

    def get_ancestors(self) -> list:
        """
        Returns list of all ancestors of elements
        """
        current_folder = self
        ancestors = [current_folder.id]

        while hasattr(current_folder, "parent") and current_folder.parent:
            ancestors.append(current_folder.parent.id)
            current_folder = current_folder.parent

        return ancestors

    def is_in_recycle_path(self) -> bool:  # pragma: no coverage
        """
        Determines if the current folder is located within a user's recycle bin path.

        This method checks if the current folder or any of its parent folders
        have the name "Recycle". It traverses up the folder hierarchy using the
        `parent` attribute until no parent folder exists or a match is found.

        Returns:
            bool: True if the folder or any of its parent folders are in the recycle bin path,
                otherwise False.
        """
        recycle_folder_name = "Recycle"
        current_folder = self

        if hasattr(current_folder, "parent"):
            while current_folder.parent:
                if (
                    current_folder.parent.name == recycle_folder_name
                    or current_folder.name == recycle_folder_name
                ):
                    return True

                current_folder = current_folder.parent

        return False

    @cached_property
    def parent_project(self):
        """
        Returns a project if element is part of a project or None if not
        """
        Project = apps.get_model("projects", "Project")
        ancestors = self.get_ancestors()
        projects = Project.objects.all()

        for folder_id in ancestors:
            for project in projects:
                if project.folder.id == folder_id:
                    return project

        return None

    @cached_property
    def is_document(self) -> bool:
        return self.type == "document"

    @cached_property
    def is_folder(self) -> bool:
        return self.type == "folder"

    class Meta:
        abstract = True


class IsRecyclable(models.Model):
    """
    Model to handle recycling functions
    """

    orig_parent = models.ForeignKey(
        "repo.Folder",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_orig_parent",
    )

    orig_name = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def reset_to_orig_parent(self):
        self.parent = self.orig_parent
        self.name = self.orig_name
        self.is_deleted = False
        self.orig_parent = None

        try:
            self.save()
        except IntegrityError:  # pragma: no coverage
            update_with_new_name(self)

    class Meta:
        abstract = True


class ActivatedModel(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class ContentFileModel(models.Model):
    content_file = models.FileField(upload_to=content_file_name)

    class Meta:
        abstract = True


class KeyValuePairModel(TimestampedModel):
    key = models.CharField(max_length=30)
    value = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
