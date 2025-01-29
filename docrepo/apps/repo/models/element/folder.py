import logging
from itertools import chain
from typing import List

from django.conf import settings
from django.db import models
from django.forms import ValidationError
from django.template.defaultfilters import truncatechars
from django.urls import reverse

from apps.comments.models import Commentable
from apps.core.models import Element, HasFolderParent, IsRecyclable

from ...models.element.version import Version
from ...utils.access import has_public_access
from ...utils.model import order_children_by_filter, user_can_navigate_path
from ...utils.static.lookup import is_a_user_home_folder
from .document import Document


class Folder(Element, HasFolderParent, IsRecyclable, Commentable):
    """
    Element representing files with meta data
    """

    is_hidden = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Folder"
        verbose_name_plural = "Folders"
        unique_together = (("name", "parent"),)
        indexes = [
            models.Index(fields=["parent"]),
            models.Index(fields=["created"]),
            models.Index(fields=["is_deleted"]),
        ]

    @classmethod
    def has_root_folder(cls):
        return cls.objects.filter(name="ROOT", parent__isnull=True).exists()

    def get_full_path(self) -> str:
        """
        Returns the full repository path for the folder
        """
        path = (
            f"/{self.name}"
            if not self.parent
            else f"{self.parent.get_full_path()}/{self.name}"
        )
        return truncatechars(path, 60)

    def get_path_with_links(self, user) -> str:
        """
        Returns the full repository path with links for each individual folder in the path
        """
        link_class = "hover:text-blue-700 relative group"
        title = "Navigate through folders"
        if not self.parent:
            url = reverse(
                "repo:folder",
                args=[
                    self.id,
                ],
            )
            return f'<a href="{url}" class="{link_class}" title="{title}" hx-boost="{settings.USE_HX_BOOST_EXT}">{truncatechars(self.name, 30)}</a>'
        else:
            if user_can_navigate_path(self, user):
                parent_path = self.parent.get_path_with_links(user)
                url = reverse(
                    "repo:folder",
                    args=[
                        self.id,
                    ],
                )
                return f'{parent_path} / <a href="{url}" class="{link_class}"  title="{title}" hx-boost="{settings.USE_HX_BOOST_EXT}">{truncatechars(self.name, 30)}</a>'
            else:
                if has_public_access(self):
                    url = reverse(
                        "repo:folder",
                        args=[
                            self.id,
                        ],
                    )
                    return f'<a href="{url}" class="{link_class}" title="{title}" hx-boost="{settings.USE_HX_BOOST_EXT}">{truncatechars(self.name, 30)}</a>'
                else:
                    return ""

    def get_children(self, include_hidden=False, order_by_filter=None) -> List[Element]:
        """
        Returns a list of elements (documents & folders) sorted with folders first,
        and optionally sorted by the given field.
        """
        documents = Document.objects.filter(parent=self)
        folders = (
            Folder.objects.filter(parent=self)
            if include_hidden
            else Folder.objects.filter(parent=self, is_hidden=False)
        )
        children = list(chain(folders, documents))

        if order_by_filter:
            children = order_children_by_filter(children, order_by_filter)

        return children

    def has_children(self) -> bool:
        """
        Returns True/False if folder contains children elements (documents or folders)
        """
        if Folder.objects.filter(parent=self) or Document.objects.filter(parent=self):
            return True
        return False

    def get_child_documents(self):  # pragma: no coverage
        """
        Returns a list of child documents for a parent folder
        """
        documents = Document.objects.filter(parent=self)
        return documents

    def get_child_folders(self):  # pragma: no coverage
        """
        Returns a list of child folders (subfolders) for a parent folder
        """
        folders = Folder.objects.filter(parent=self)
        return folders

    def get_descendant_count(self, include_hidden=False) -> int:
        """
        Returns a count of all descendent children elements
        """
        count = 0
        stack = [self]

        while stack:
            current_folder = stack.pop()
            documents = Document.objects.filter(
                parent=current_folder,
            ).count()
            folders = (
                Folder.objects.filter(parent=current_folder)
                if include_hidden
                else Folder.objects.filter(
                    parent=current_folder,
                    is_hidden=False,
                )
            )
            count += documents
            count += folders.count()
            stack.extend(folders)

        return count

    @property
    def folder_size(self) -> float:  # pragma: no coverage
        """
        Returns the size of a folder and all descendent file sizes
        """
        log = logging.getLogger(__name__)
        total_size = 0
        stack = [self]

        while stack:
            current_folder = stack.pop()
            documents = Document.objects.filter(parent=current_folder)

            for document in documents:
                versions = Version.objects.filter(parent=document).order_by("-created")
                if versions.exists():
                    try:
                        latest_version = versions[0]
                        total_size += latest_version.content_file.size
                    except FileNotFoundError as err:
                        log.error(
                            f"Missing content file for document id: {document.pk}: {err}"
                        )
                        total_size += 0
                else:
                    log.error(f"No versions exist for document id: {document.pk}")

            subfolders = Folder.objects.filter(parent=current_folder)
            stack.extend(subfolders)

        return total_size

    def clean(self) -> None:  # pragma: no coverage
        """
        Validation of form creation
        """
        if self.name == "ROOT" and not self.parent:
            return
        if not self.parent and Folder.has_root_folder():
            raise ValidationError("All folders must have a parent.")
        if self.parent == self:
            raise ValidationError("A folder cannot assign itself as its own parent.")
        if is_a_user_home_folder(folder=self):
            raise ValidationError("User home folder's name cannot be changed.")

    def save(self, *args, **kwargs) -> None:  # pragma: no coverage
        """
        Saves folder object
        """
        self.clean()
        super().save(*args, **kwargs)

    @property
    def type(self) -> str:
        """
        Returns type of folder which is "folder"
        """
        return "folder"

    def __str__(self):
        return self.get_full_path()
