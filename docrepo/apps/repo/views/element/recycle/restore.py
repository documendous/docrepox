from django.http import JsonResponse
from django.urls import reverse

from apps.core.views import View
from apps.repo import rules
from apps.repo.utils.static.lookup import get_model


class RestoreElementView(View):
    def post(self, request, element_type, element_id):
        Model = get_model(element_type)
        instance = Model.objects.get(pk=element_id)

        rules.can_restore_element(request, instance)

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
