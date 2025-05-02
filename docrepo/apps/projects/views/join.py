from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from apps.comms.models import Communication
from apps.comms.utils import acknowledge_comm, create_comm
from apps.core.views import View

from ..models import Project
from ..utils.project import get_group_by_type

User = get_user_model()


class RequestProjectJoinView(View):
    """
    View for requesting a project join
    """

    def post(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        user = request.user
        managers = project.get_managers()

        create_comm(
            from_user=user,
            to_group=managers,
            subject=f"Request to join project: {project.name} from {user.username}",
            content=f"Request to join project: {project.name} from {user.username}",
            category="project_join_request",
            related_element=project,
        )

        messages.add_message(
            request,
            messages.INFO,
            f"Request to join project: {project.name} sent.",
        )

        return HttpResponseRedirect(
            reverse("repo:folder", args=[project.folder.parent.pk])
        )


class AddRequesterToProjectGroupView(View):
    """
    View for acknowledging project request join. Sets join request comm as acknowledged.
    """

    def post(self, request, project_id, user_id, group_type):
        user = User.objects.get(pk=user_id)
        project = Project.objects.get(pk=project_id)
        group = get_group_by_type(project=project, group_type=group_type)

        if not group:
            raise Http404

        user.groups.add(group)
        acknowledge_comm(user=user, object_id=project_id)

        return HttpResponseRedirect(
            reverse(
                "repo:projects:project_details",
                args=[
                    project.pk,
                ],
            )
        )


class RejectRequestJoinView(View):
    """
    View for rejecting the project join request by deleting it
    """

    def post(self, request, req_join_id):
        comm = Communication.objects.get(pk=req_join_id)
        project = comm.related_element
        comm.delete()

        return HttpResponseRedirect(
            reverse(
                "repo:projects:project_details",
                args=[
                    project.pk,
                ],
            )
        )
