from django.conf import settings
from django.db.models import Q, QuerySet

from .models import Project

active_project_qs = Project.objects.filter(is_active=True)


def get_managed_projects() -> QuerySet:
    """
    Returns a list of projects of visibility "managed"
    """
    return active_project_qs.filter(
        visibility="managed",
    ).order_by(
        "-created"
    )[: settings.MAX_CONTENT_ITEM_SIZE]


def get_accessible_project_list() -> QuerySet:
    """
    Returns a list of projects with visibility of either "public" or "managed"
    Any user can see these projects and know they exist.
    """
    return active_project_qs.filter(
        Q(visibility="public") | Q(visibility="managed")
    ).order_by("-created")[: settings.MAX_CONTENT_ITEM_SIZE]


def get_public_projects() -> QuerySet:
    """
    Returns a list of projects with visibility "public"
    """
    return active_project_qs.filter(visibility="public").order_by("-created")[
        : settings.MAX_CONTENT_ITEM_SIZE
    ]


def get_owned_projects(user) -> QuerySet:
    """
    Returns a list of projects owned by the current user.
    """
    return active_project_qs.filter(owner=user).order_by("-created")[
        : settings.MAX_CONTENT_ITEM_SIZE
    ]


def get_associated_projects(user) -> QuerySet:
    """
    Returns a list of projects the current user is a member of but not any the user owns.
    """
    return (
        active_project_qs.filter(
            Q(managers_group__in=user.groups.values_list("name", flat=True))
            | Q(editors_group__in=user.groups.values_list("name", flat=True))
            | Q(readers_group__in=user.groups.values_list("name", flat=True))
        )
        .distinct()
        .exclude(owner=user)
        .order_by("-created")[: settings.MAX_CONTENT_ITEM_SIZE]
    )
