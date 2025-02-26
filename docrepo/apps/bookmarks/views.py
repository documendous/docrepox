from django.shortcuts import render
from django.urls import reverse

from apps.core.views import View, redirect_to_referer_or_default
from apps.repo.utils.system.object import get_system_root_folder

from .models import Bookmark
from .utils import add_bookmark, get_valid_bookmarks, remove_bookmark


class BookmarkListView(View):
    def get(self, request):
        """
        List view for bookmarks
        """
        bookmarks = Bookmark.objects.filter(owner=request.user)
        valid_children = get_valid_bookmarks(bookmarks, user=request.user)
        home_folder = request.user.profile.home_folder
        root_folder = get_system_root_folder()

        self.context.update(
            {
                "bookmarks": bookmarks,
                "children": valid_children,
                "home_folder_id": home_folder.id,
                "is_bookmark_list_view": True,
                "root_folder_id": root_folder.id,
            }
        )

        return render(request, "repo/bookmark_list.html", self.context)


class AddBookmarkView(View):
    def post(self, request, element_type, element_pk):
        """
        Add bookmark view
        """
        add_bookmark(request, element_type, element_pk)

        return redirect_to_referer_or_default(
            request,
            default_url=reverse(
                "repo:element_details", args=[element_type, element_pk]
            ),
        )


class RemoveBookmarkView(View):
    def post(self, request, element_type, element_pk):
        """
        Remove bookmark view
        """
        remove_bookmark(request, element_type, element_pk)

        return redirect_to_referer_or_default(
            request,
            default_url=reverse(
                "repo:element_details", args=[element_type, element_pk]
            ),
        )
