from typing import Any

from django.shortcuts import render

from apps.core.views import View
from apps.dashlets.utils.motd import get_motd
from apps.projects.querysets import (
    get_accessible_project_list,
    get_associated_projects,
    get_managed_projects,
    get_owned_projects,
    get_public_projects,
)
from apps.projects.utils.project import get_accessible_project_documents

from ..querysets import get_owned_documents
from ..utils.system.object import get_system_root_folder


class IndexView(View):
    """
    Main dashboard view
    """

    template_name = "ui/index.html"
    context: dict[str, Any] = {}

    def get(self, request):
        managed_projects = get_managed_projects()
        project_list = get_accessible_project_list()
        user_owned_documents = get_owned_documents(request)
        user_project_documents = get_accessible_project_documents(request)
        public_projects = get_public_projects()
        owned_projects = get_owned_projects(request)
        associated_projects = get_associated_projects(request)

        use_motd, motd = get_motd()

        self.context = {
            "associated_projects": associated_projects,
            "document_list": user_owned_documents,
            "user_projects_documents": user_project_documents,
            "home_folder_id": request.user.profile.home_folder.id,
            "managed_projects": managed_projects,
            "motd": motd,
            "owned_projects": owned_projects,
            "project_list": project_list,
            "public_projects": public_projects,
            "root_folder_id": get_system_root_folder().id,
            "use_motd": use_motd,
        }

        return render(request, self.template_name, context=self.context)
