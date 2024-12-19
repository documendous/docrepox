from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from apps.comms.models import Communication
from apps.comms.utils import send_comm
from apps.core.views import View
from apps.projects.models import Project


User = get_user_model()


class RequestProjectJoinView(View):
    """
    View for requesting a project join
    """

    def post(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        user = request.user
        managers = project.get_managers()

        send_comm(
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
    View for acknowledging project request join. Deletes the join request.
    """

    def post(self, request, project_id, user_id, group_type):
        user = User.objects.get(pk=user_id)
        project = Project.objects.get(pk=project_id)

        if group_type == "readers":
            group = Group.objects.get(name=project.readers_group)
        elif group_type == "editors":
            group = Group.objects.get(name=project.editors_group)
        elif group_type == "managers":
            group = Group.objects.get(name=project.managers_group)
        else:
            raise Http404

        user.groups.add(group)
        communications = Communication.objects.filter(
            content_type__model="project", object_id=project.id
        )
        for each in communications:
            each.delete()
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
