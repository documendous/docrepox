import logging
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from apps.core.views import View
from apps.repo import rules
from apps.repo.models.element.folder import Folder


class EmptyRecycleFolderView(View):
    """
    View to hard delete all folders and documents in a recycling folder
    """

    def post(self, request, folder_id):
        log = logging.getLogger(__name__)
        trashcan_folder = Folder.objects.get(pk=folder_id, owner=request.user)
        if trashcan_folder.name == "Recycle":
            children = trashcan_folder.get_children()
            if children:
                for each in children:
                    try:
                        rules.can_delete_element(request, each)
                        each.delete()
                    except Exception as err:  # pragma: no coverage
                        log.error(repr(err))
                        messages.error(
                            request,
                            f"Unable to delete {each.type}: {each.name}",
                        )
                messages.info(
                    request,
                    "Items permanently deleted.",
                )
            else:
                messages.info(request, "Trashcan empty.")  # pragma: no coverage
        else:
            raise Http404
        return HttpResponseRedirect(
            reverse(
                "repo:folder",
                args=[
                    trashcan_folder.pk,
                ],
            )
        )
