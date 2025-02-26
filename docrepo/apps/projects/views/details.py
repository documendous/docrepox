from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import render

from apps.comms.models import Communication
from apps.core.views import View
from apps.projects import rules
from apps.repo.utils.model import get_path_with_links
from apps.repo.utils.system.object import get_system_root_folder

from ..forms import MultipleUserSelectForm
from ..models import Project

User = get_user_model()


class ProjectDetailsView(View):
    """
    View for project's details
    """

    def get(self, request, project_id):
        project = Project.objects.get(pk=project_id)

        rules.can_view_project_details(request, element=project.folder)

        path_with_links = get_path_with_links(project.folder, request.user)

        managers_group = Group.objects.filter(
            name=project.managers_group,
        ).first()

        editors_group = Group.objects.filter(
            name=project.editors_group,
        ).first()

        readers_group = Group.objects.filter(
            name=project.readers_group,
        ).first()

        managers_select_form = MultipleUserSelectForm(group=managers_group)
        editors_select_form = MultipleUserSelectForm(group=editors_group)
        readers_select_form = MultipleUserSelectForm(group=readers_group)

        if project.in_managers_group(request.user):
            communications = Communication.objects.filter(
                content_type__model="project", object_id=project.id
            )
        else:
            communications = Communication.objects.none()

        return render(
            request,
            "projects/project_details.html",
            {
                "has_add_user_errors": 0,
                "home_folder_id": request.user.profile.home_folder.id,
                "path_with_links": path_with_links,
                "project": project,
                "root_folder_id": get_system_root_folder().id,
                "managers_group": managers_group,
                "editors_group": editors_group,
                "readers_group": readers_group,
                "managers_select_form": managers_select_form,
                "editors_select_form": editors_select_form,
                "readers_select_form": readers_select_form,
                "project_comments_enabled": settings.ENABLE_PROJECT_COMMENTS,
                "communications": communications,
            },
        )
