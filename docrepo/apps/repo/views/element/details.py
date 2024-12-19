from django.conf import settings
from django.shortcuts import render
from apps.core.views import View
from apps.repo import rules
from apps.repo.utils.static.lookup import get_model
from apps.repo.utils.system.object import get_system_root_folder
from apps.repo.forms.element import UpdateVersionForm


class ElementDetailsView(View):
    """
    View for showing an element's details (document or folder)
    """

    def get(self, request, element_id, element_type):
        Model = get_model(element_type)
        element = Model.objects.get(pk=element_id)
        if element_type == "document":
            parent = element.parent
        elif element_type == "folder":
            parent = element

        rules.can_view_element_details(request, element)

        path_with_links = parent.get_path_with_links(request.user)
        return render(
            request,
            "repo/element_details.html",
            {
                "element": element,
                "has_version_errors": False,
                "home_folder_id": request.user.profile.home_folder.id,
                "path_with_links": path_with_links,
                "root_folder_id": get_system_root_folder().id,
                "has_version_errors": 0,
                "update_version_form": UpdateVersionForm(),
                "scope": "summary",
                "folder_comments_enabled": settings.ENABLE_FOLDER_COMMENTS,
                "document_comments_enabled": settings.ENABLE_DOCUMENT_COMMENTS,
                "public_comments_enabled": settings.ENABLE_PUBLIC_COMMENTS,
            },
        )
