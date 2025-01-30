import datetime
from typing import List

from apps.repo.models.element.document import Document


def user_can_navigate_path(folder, user):
    """
    Return True if user can navigate the folder
    """
    return (
        folder.owner == user
        or user.is_superuser
        or folder.parent_project
        and (
            folder.parent_project.visibility == "public"
            or folder.parent_project.is_member(user)
        )
    )


def order_children_by_filter(children: list, order_by_filter: str) -> List:
    """
    Returns a sorted children list (chained list of documents and folders)
    """
    reverse = order_by_filter.startswith("-")
    field = order_by_filter.lstrip("-")

    def sort_key(x):
        value = getattr(x, field, None)
        # Handle None values by returning a fallback
        if value is None:
            return ""
        # Handle datetime objects
        if isinstance(value, datetime.datetime):
            return value
        # Handle other values, assuming they are strings
        return str(value).lower()

    result = sorted(children, key=sort_key, reverse=reverse)
    return result


def get_current_version_tag(document: Document) -> str:
    """
    Returns most current version tag of a document else returns an empty string
    """
    current_version_tag = ""
    versions = document.get_versions()
    if versions:
        current_version_tag = versions[0]
    return current_version_tag
