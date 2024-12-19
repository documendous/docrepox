import logging
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from apps.core.views import View
from apps.repo.utils.system.object import (
    get_system_root_folder,
    get_system_projects_folder,
)
from ..forms import AddProjectForm
from ..utils.project import get_viewable_project_list

User = get_user_model()


class ProjectsView(View):
    """
    View for list of projects in a similar fashion as folders view
    """

    log = logging.getLogger(__name__)
    template_name = "projects/project_list.html"

    def _get_common_context(self, request, add_project_form):
        parent = get_system_projects_folder()
        home_folder = request.user.profile.home_folder
        root_folder = get_system_root_folder()
        path_with_links = parent.get_path_with_links(
            request.user
        ) or home_folder.get_path_with_links(request.user)

        projects = get_viewable_project_list(request)

        return {
            "add_project_form": add_project_form,
            "folder": parent,
            "home_folder_id": home_folder.id,
            "path_with_links": path_with_links,
            "projects": projects,
            "root_folder_id": root_folder.id,
            "has_project_errors": 0,
        }

    def get(self, request):
        add_project_form = AddProjectForm()
        context = self._get_common_context(request, add_project_form)
        return render(request, self.template_name, context)

    def post(self, request):
        log = logging.getLogger(__name__)
        add_project_form = AddProjectForm(request.POST)
        if add_project_form.is_valid():
            project = add_project_form.save(commit=False)
            project.owner = request.user
            project.save()

            messages.add_message(
                request,
                messages.INFO,
                f'Project "{project.name}" was successfully created.',
            )

            return HttpResponseRedirect(reverse("repo:projects:index"))

        log.debug(add_project_form.errors)

        context = self._get_common_context(request, add_project_form)
        context["has_project_errors"] = 1
        return render(request, self.template_name, context)
