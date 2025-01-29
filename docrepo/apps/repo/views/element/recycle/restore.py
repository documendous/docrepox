from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse

from apps.core.views import View
from apps.repo import rules
from apps.repo.utils.helpers import update_with_new_name
from apps.repo.utils.static.lookup import get_model


class RestoreElementView(View):
    """
    View for restoring folders and documents to original parent
    """

    def post(self, request, element_type, element_id):
        Model = get_model(element_type)
        element = Model.objects.get(pk=element_id)
        rules.can_restore_element(request, element)
        element.parent = element.orig_parent
        element.name = element.orig_name
        element.is_deleted = False
        element.orig_parent = None

        try:
            element.save()
        except IntegrityError:  # pragma: no coverage
            update_with_new_name(element)
        return HttpResponseRedirect(
            reverse(
                "repo:folder",
                args=[request.user.profile.recycle_folder.pk],
            )
        )
