import logging
from operator import attrgetter
from typing import List

from django.contrib.auth.models import Group, User
from django.db.models import Q, QuerySet
from django.http import HttpRequest
from django.template.defaultfilters import slugify

from apps.core.utils.queryset import field_name, is_reversed
from apps.repo.models.element.document import Document
from apps.repo.models.element.folder import Folder
from apps.repo.utils.system.object import get_system_projects_folder

from ..models import Project


def add_owner_to_managers_group(instance: Project, managers_group: Group) -> None:
    """
    Adds project creater (project owner) to project managers' group
    """
    log = logging.getLogger(__name__)
    instance.owner.groups.add(managers_group)
    log.debug(f"Added: {instance.owner} to managers group")


def create_project_groups(instance: Project) -> None:
    """
    Create default groups for a project
    """
    log = logging.getLogger(__name__)
    groups = ["managers", "editors", "readers"]

    for group in groups:
        group_name = f"project_{slugify(instance.name)}_{group}"
        setattr(instance, f"{group}_group", group_name)
        g = Group.objects.create(name=group_name)
        log.debug(f"Group: {group_name} created.")

        if group == "managers":
            add_owner_to_managers_group(instance, managers_group=g)


def create_project_folder(instance: Project) -> None:
    """
    Create the root folder for a project
    """
    folder = Folder.objects.create(
        name=instance.name,
        owner=instance.owner,
        parent=get_system_projects_folder(),
    )

    instance.folder = folder
    instance.save()


def change_project_folder_name(instance: Project) -> None:
    """
    Changes profile folder's name. As part of the create project folder signal.
    """
    folder = getattr(instance, "folder", None)

    if folder:
        folder.name = instance.name
        folder.save()


def delete_project_groups(instance):
    # Delete associated groups if they exist
    for group_name in [
        instance.managers_group,
        instance.editors_group,
        instance.readers_group,
    ]:
        if group_name:
            try:
                group = Group.objects.get(name=group_name)
                group.delete()
            except Group.DoesNotExist:  # pragma: no coverage
                pass


def get_accessible_projects(user: HttpRequest) -> QuerySet:  # pragma: no coverage
    """
    Returns a list of projects a user is either a member of is a public project
    """
    if user.profile.is_admin_user():
        projects = Project.objects.filter(is_active=True)
    else:
        projects = Project.objects.filter(
            Q(visibility="public")
            | Q(
                id__in=[
                    project.id
                    for project in Project.objects.all()
                    if project.is_member(user)
                ]
            ),
            is_active=True,
        )

    return projects


def get_public_or_managed_projects() -> List[Project]:
    return list(
        Project.objects.filter(
            Q(visibility="public") | Q(visibility="managed"), is_active=True
        )
    )


def get_private_projects(user: User) -> List[Project]:
    return [
        project
        for project in Project.objects.filter(visibility="private", is_active=True)
        if project.is_member(user)
    ]


def get_nonadmin_viewable_project_list(user) -> List[Project]:
    return get_public_or_managed_projects() + get_private_projects(user)


def get_sorted_projects(
    projects: List[Project], order_by_filter: str
) -> List[Project]:  # pragma: no coverage
    try:
        projects.sort(
            key=attrgetter(field_name(order_by_filter)),
            reverse=is_reversed(order_by_filter),
        )
    except AttributeError:
        pass

    return projects


def get_viewable_project_list(
    user: User, order_by_filter: str | None = None
) -> List[Project]:
    """
    Returns a list of projects a user can view in a list but not necessarily access.
    """
    if user.profile.is_admin_user():
        projects = list(Project.objects.filter(is_active=True))
    else:
        projects = get_nonadmin_viewable_project_list(user)

    if order_by_filter:  # pragma: no coverage
        projects = get_sorted_projects(projects, order_by_filter)

    return projects


def is_a_project_folder(folder: Folder) -> bool:
    """
    Returns boolean if a folder is a root folder for a project
    """
    if folder.type == "folder":
        return Project.objects.filter(folder=folder).exists()
    elif folder.type == "project":
        return True
    return False


def get_accessible_project_documents(
    user: HttpRequest, max_size=5
) -> QuerySet:  # pragma: no coverage
    """
    Returns a limited list of documents from all of a user's projects
    """
    project_list = Project.objects.filter(
        Q(visibility="public") | Q(visibility="managed") | Q(visibility="private")
    ).order_by("-created")[:max_size]

    document_list = Document.objects.all().order_by("-created")[:5]

    user_projects_documents = []
    for project in project_list:
        if project.is_member(user):
            for document in document_list:
                if project == document.parent_project:
                    user_projects_documents.append(document)

    return user_projects_documents[:max_size]
