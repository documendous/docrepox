from django.contrib import messages
from django.db import IntegrityError
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from apps.bookmarks.templatetags.bookmark_tags import is_bookmarked
from apps.bookmarks.utils import remove_bookmark
from apps.clipboard.utils.clipboard import is_in_clipboard, remove_from_clipboard
from apps.core.views import View
from apps.repo import rules
from apps.repo.models.element.folder import Folder
from apps.repo.utils.helpers import update_with_new_name
from apps.repo.utils.static.lookup import get_model


class BaseRecycleElementView(View):
    def move_to_recycle_folder(self, user, element):
        element.orig_parent = element.parent
        element.orig_name = element.name
        element.is_deleted = True
        element.parent = user.profile.recycle_folder

        if is_bookmarked(element, user=user):
            remove_bookmark(user, element.type, element.id)

        if is_in_clipboard(user, element):
            remove_from_clipboard(user, element)

        try:
            element.save()
        except IntegrityError:  # pragma: no coverage
            update_with_new_name(element)


class RecycleElementView(BaseRecycleElementView):
    """
    View handline soft deletes of documents and folders, places
    element in recycling folder, removes bookmarks
    """

    def post(self, request, element_type, element_id):
        Model = get_model(element_type)
        element = Model.objects.get(pk=element_id)
        rules.can_recycle_element(request.user, element)
        self.move_to_recycle_folder(request.user, element)
        messages.info(request, f"Placed {element.name} in your recycle folder.")

        return HttpResponseRedirect(
            reverse(
                "repo:folder",
                args=[element.orig_parent.pk],
            ),
        )


class RecycleElementsView(BaseRecycleElementView):
    """
    View handline soft deletes of all documents and folders in a given
    parent folder, places element in recycling folder, removes bookmarks
    """

    def _set_messages(self, recyclable_items, unrecyclable_items):
        if recyclable_items:
            messages.info(
                self.request, f"Placed {recyclable_items} items in your recycle folder."
            )
        if unrecyclable_items:  # pragma: no coverage
            messages.warning(
                self.request, f"Unable to recycle {unrecyclable_items} items."
            )

    def post(self, request, parent_id):
        parent = Folder.objects.get(pk=parent_id)
        children = parent.get_children()
        unrecyclable_items = 0
        recyclable_items = 0
        can_recycle = False

        for child in children:
            try:
                can_recycle = rules.can_recycle_element(request.user, child)
            except Http404:  # pragma: no coverage
                unrecyclable_items += 1
                can_recycle = False

            if can_recycle:
                self.move_to_recycle_folder(request.user, child)
                recyclable_items += 1

        self._set_messages(recyclable_items, unrecyclable_items)

        return HttpResponseRedirect(
            reverse(
                "repo:folder",
                args=[parent.pk],
            )
        )
