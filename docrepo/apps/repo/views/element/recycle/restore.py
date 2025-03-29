from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from apps.core.views import View
from apps.repo import rules
from apps.repo.models.element.folder import Folder
from apps.repo.utils.static.lookup import get_model


class RestoreElementView(View):
    def post(self, request, element_type, element_id):
        Model = get_model(element_type)
        instance = Model.objects.get(pk=element_id)

        rules.can_restore_element(request.user, instance)

        instance.reset_to_orig_parent()

        return JsonResponse(
            {
                "success": True,
                "redirect_recycle": reverse(
                    "repo:folder", args=[request.user.profile.recycle_folder.pk]
                ),
                "redirect_original": reverse("repo:folder", args=[instance.parent.pk]),
            }
        )


class RestoreElementsView(View):
    """
    View for restoring folders and documents to original parent
    """

    def post(self, request, parent_id):
        parent = Folder.objects.get(pk=parent_id)
        children = parent.get_children()

        for child in children:
            rules.can_restore_element(request.user, child)
            child.reset_to_orig_parent()

        return HttpResponseRedirect(
            reverse(
                "repo:folder",
                args=[parent.pk],
            )
        )
