from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from apps.bookmarks.templatetags.bookmark_tags import is_bookmarked
from apps.bookmarks.utils import remove_bookmark
from apps.core.views import View
from apps.repo import rules
from apps.repo.utils.helpers import update_with_new_name
from apps.repo.utils.static.lookup import get_model


class RecycleElementView(View):
    """
    View handline soft deletes of documents and folders, places element in recycling folder, removes bookmarks
    """

    def post(self, request, element_type, element_id):
        Model = get_model(element_type)
        element = Model.objects.get(pk=element_id)
        rules.can_recycle_element(request, element)

        element.orig_parent = element.parent
        element.orig_name = element.name
        element.is_deleted = True
        element.parent = request.user.profile.recycle_folder

        if is_bookmarked(element, user=request.user):
            remove_bookmark(request, element_type, element_id)

        try:
            element.save()
        except IntegrityError:  # pragma: no coverage
            update_with_new_name(element)
        return HttpResponseRedirect(
            reverse(
                "repo:folder",
                args=[element.orig_parent.pk],
            )
        )
