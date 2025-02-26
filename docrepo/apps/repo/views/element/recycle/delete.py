from django.http import HttpResponseRedirect
from django.urls import reverse

from apps.core.views import View
from apps.repo import rules
from apps.repo.utils.static.lookup import get_model


class DeleteElementView(View):
    """
    View for handling hard deletes of folders and documents
    """

    def post(self, request, element_type, element_id):
        Model = get_model(element_type)
        element = Model.objects.get(pk=element_id)
        rules.can_delete_element(request, element)
        element.delete()

        return HttpResponseRedirect(
            reverse(
                "repo:folder",
                args=[request.user.profile.recycle_folder.pk],
            )
        )
