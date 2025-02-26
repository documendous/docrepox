from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models
from django.db.models import QuerySet

from apps.comments.models import Commentable
from apps.core.models import ActivatedModel, Element
from apps.repo.models.element import Folder


class Project(Element, ActivatedModel, Commentable):  # pragma: no coverage
    """
    Project model - allows for grouping of document, folder and authorizations
    """

    name = models.CharField(max_length=255, unique=True)

    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    visibility = models.CharField(
        max_length=30,
        choices=(
            ("public", "Public"),
            ("managed", "Managed"),
            ("private", "Private"),
        ),
        default="public",
    )

    managers_group = models.CharField(max_length=355, null=True, blank=True)
    editors_group = models.CharField(max_length=355, null=True, blank=True)
    readers_group = models.CharField(max_length=355, null=True, blank=True)

    class Meta:
        unique_together = (
            ("name", "managers_group"),
            ("name", "editors_group"),
            ("name", "readers_group"),
        )

        ordering = ["-created"]

        indexes = [
            models.Index(fields=["visibility", "is_active"]),  # Compound index
            models.Index(fields=["managers_group", "is_active"]),
            models.Index(fields=["editors_group", "is_active"]),
            models.Index(fields=["readers_group", "is_active"]),
            models.Index(fields=["owner"]),
            models.Index(
                fields=["created"]
            ),  # Retain if sorting by created date is frequent
            models.Index(fields=["folder"]),  # Retain for folder-based queries
        ]

    @property
    def type(self) -> str:
        """
        Returns type of project
        """
        return "project"

    def in_managers_group(self, user) -> bool:
        """
        Returns True if user is a manager (or in manager's group)
        """
        if not self.managers_group:
            return False
        try:
            group = Group.objects.get(name=self.managers_group)
            return group in user.groups.all()
        except Group.DoesNotExist:
            return False

    def in_editors_group(self, user) -> bool:
        """
        Returns True if user is an editor (or in editor's group)
        """
        if not self.editors_group:
            return False
        try:
            group = Group.objects.get(name=self.editors_group)
            return group in user.groups.all()
        except Group.DoesNotExist:
            return False

    def in_readers_group(self, user) -> bool:
        """
        Returns True if user is a reader (or in reader's group)
        """
        if not self.readers_group:
            return False
        try:
            group = Group.objects.get(name=self.readers_group)
            return group in user.groups.all()
        except Group.DoesNotExist:
            return False

    def is_member(self, user) -> bool:
        """
        Returns True if user is a member of project
        """
        if (
            self.in_managers_group(user)
            or self.in_editors_group(user)
            or self.in_readers_group(user)
            or self.owner == user
        ):
            return True
        return False

    def get_managers(self) -> QuerySet:
        """
        Returns QuerySet of all users who are members of the managers group

        Returns:
            QuerySet: QuerySet of User objects who are managers
        """
        if not self.managers_group:
            return get_user_model().objects.none()
        try:
            group = Group.objects.get(name=self.managers_group)
            return group.user_set.all()
        except Group.DoesNotExist:
            return get_user_model().objects.none()

    def get_editors(self) -> QuerySet:
        """
        Returns QuerySet of all users who are members of the editors group

        Returns:
            QuerySet: QuerySet of User objects who are editors
        """
        if not self.editors_group:
            return get_user_model().objects.none()
        try:
            group = Group.objects.get(name=self.editors_group)
            return group.user_set.all()
        except Group.DoesNotExist:
            return get_user_model().objects.none()

    def get_readers(self) -> QuerySet:
        """
        Returns QuerySet of all users who are members of the readers group

        Returns:
            QuerySet: QuerySet of User objects who are readers
        """
        if not self.readers_group:
            return get_user_model().objects.none()
        try:
            group = Group.objects.get(name=self.readers_group)
            return group.user_set.all()
        except Group.DoesNotExist:
            return get_user_model().objects.none()

    def get_role_display(self, user) -> str:
        """
        Returns display string of a user's role in a project (manager, editor, reader, nonmember)
        """
        if settings.ADMIN_ALLOW_ALL and user.profile.is_admin_user():
            return "admin"
        elif user in self.get_managers():
            return "manager"
        elif user in self.get_editors():
            return "editor"
        elif user in self.get_readers():
            return "reader"
        else:
            return "nonmember"

    def get_all_members(self) -> QuerySet:
        """
        Returns QuerySet of all users who are members of any project group (managers, editors, or readers)

        Returns:
            QuerySet: QuerySet of User objects who are members of the project
        """
        User = get_user_model()

        return User.objects.filter(
            groups__name__in=[
                name
                for name in [
                    self.managers_group,
                    self.editors_group,
                    self.readers_group,
                ]
                if name is not None
            ]
        ).distinct()

    def __str__(self):
        return self.name
