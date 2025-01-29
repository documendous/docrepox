from django.conf import settings
from django.db.models import Q, QuerySet
from django.http import HttpRequest

from .models import Project


def get_managed_projects() -> QuerySet:
    """
    Returns a list of projects of visibility "managed"
    """
    return Project.objects.filter(
        visibility="managed",
    ).order_by(
        "-created"
    )[: settings.MAX_CONTENT_ITEM_SIZE]


def get_accessible_project_list() -> QuerySet:
    """
    Returns a list of projects with visibility of either "public" or "managed"
    Any user can see these projects and know they exist.
    """
    return Project.objects.filter(
        Q(visibility="public") | Q(visibility="managed")
    ).order_by("-created")[: settings.MAX_CONTENT_ITEM_SIZE]


def get_public_projects() -> QuerySet:
    """
    Returns a list of projects with visibility "public"
    """
    return Project.objects.filter(visibility="public").order_by("-created")[
        : settings.MAX_CONTENT_ITEM_SIZE
    ]


def get_owned_projects(request: HttpRequest) -> QuerySet:
    """
    Returns a list of projects owned by the current user.
    """
    return Project.objects.filter(owner=request.user).order_by("-created")[
        : settings.MAX_CONTENT_ITEM_SIZE
    ]


def get_associated_projects(request: HttpRequest) -> QuerySet:
    """
    Returns a list of projects the current user is a member of but not any the user owns.
    """
    return (
        Project.objects.filter(
            Q(managers_group__in=request.user.groups.values_list("name", flat=True))
            | Q(editors_group__in=request.user.groups.values_list("name", flat=True))
            | Q(readers_group__in=request.user.groups.values_list("name", flat=True))
        )
        .distinct()
        .exclude(owner=request.user)
        .order_by("-created")[: settings.MAX_CONTENT_ITEM_SIZE]
    )
