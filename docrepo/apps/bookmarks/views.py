from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from apps.bookmarks.models import Bookmark
from apps.bookmarks.utils import add_bookmark, remove_bookmark
from apps.core.views import View
from apps.repo.utils.system.object import get_system_root_folder


class BookmarkListView(View):
    def get(self, request):
        """
        List view for bookmarks
        """
        bookmarks = Bookmark.objects.filter(owner=request.user)
        home_folder = request.user.profile.home_folder
        root_folder = get_system_root_folder()
        self.context.update(
            {
                "bookmarks": bookmarks,
                "children": [bookmark.content_object for bookmark in bookmarks],
                "home_folder_id": home_folder.id,
                "root_folder_id": root_folder.id,
                "is_bookmark_list_view": True,
            },
        )
        return render(request, "repo/bookmark_list.html", self.context)


class AddBookmarkView(View):
    def post(self, request, element_type, element_pk):
        """
        Add bookmark view
        """
        add_bookmark(request, element_type, element_pk)
        if "HTTP_REFERER" in request.META:  # pragma: no coverage
            return_url = request.META["HTTP_REFERER"]
        else:
            return_url = reverse(
                "repo:element_details", args=[element_type, element_pk]
            )
        return HttpResponseRedirect(return_url)


class RemoveBookmarkView(View):
    def post(self, request, element_type, element_pk):
        """
        Remove bookmark view
        """
        remove_bookmark(request, element_type, element_pk)
        if "HTTP_REFERER" in request.META:  # pragma: no coverage
            return_url = request.META["HTTP_REFERER"]
        else:
            return_url = reverse(
                "repo:element_details", args=[element_type, element_pk]
            )
        return HttpResponseRedirect(return_url)
