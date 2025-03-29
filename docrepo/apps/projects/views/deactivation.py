from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse

from apps.core.views import View
from apps.projects import rules
from apps.projects.models import Project

User = get_user_model()


class DeactivateProjectView(View):
    def post(self, request, project_id):
        project = Project.objects.get(pk=project_id)
        deactivate = request.POST.get("deactivate", None)
        rules.can_deactivate_project(request.user, project.folder)

        if deactivate:
            project.is_active = False
            project.save()

        return HttpResponseRedirect(reverse("repo:projects:index"))
