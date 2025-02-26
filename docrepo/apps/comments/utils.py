from uuid import UUID

from django.urls import reverse

from apps.projects.utils.project import is_a_project_folder
from apps.repo.models.element.folder import Folder


def get_details_url(element_type: str, element_id: UUID) -> str:
    """
    Returns an element details url for document, folder and project
    """
    url = reverse("repo:element_details", args=[element_type, element_id])

    if element_type == "folder":
        folder = Folder.objects.get(pk=element_id)

        if is_a_project_folder(folder):
            project = folder.parent_project
            url = reverse(
                "repo:projects:project_details",
                args=[
                    project.pk,
                ],
            )

    return url
