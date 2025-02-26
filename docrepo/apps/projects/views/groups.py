from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from apps.core.views import View
from apps.projects import rules

from ..forms import MultipleUserSelectForm
from ..models import Project

User = get_user_model()


class AddUserToProjectView(View):
    """
    View for adding user(s) to a project group
    """

    def post(self, request, project_id, group_id):
        project = get_object_or_404(Project, pk=project_id)
        group = Group.objects.get(pk=group_id)

        if (
            group.name == project.managers_group
            or group.name == project.editors_group
            or group.name == project.readers_group
        ):
            user_select_form = MultipleUserSelectForm(request.POST, group=group)

            if user_select_form.is_valid():
                for user in user_select_form.cleaned_data["users"]:
                    user.groups.add(group)

            return HttpResponseRedirect(
                reverse(
                    "repo:projects:project_details",
                    args=[project.pk],
                )
            )

        raise Http404  # pragma: no coverage


class RemoveUserFromProjectGroupView(View):
    """
    View for removing user(s) from a project group
    """

    def post(self, request, project_id, user_id, group_id):
        project = Project.objects.get(pk=project_id)
        rules.can_remove_user_from_project_group(request, project.folder)
        user = User.objects.get(pk=user_id)
        group = Group.objects.get(pk=group_id)
        user.groups.remove(group)

        return HttpResponseRedirect(
            reverse(
                "repo:projects:project_details",
                args=[project.pk],
            )
        )
