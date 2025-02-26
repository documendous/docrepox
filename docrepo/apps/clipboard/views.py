from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse

from apps.clipboard.utils.paste import add_to_clipboard
from apps.core.views import View
from apps.repo.utils.static.lookup import get_model

from .models import Clipboard
from .services import (
    copy_clipboard_elements_to_parent,
    delete_clipboard_documents,
    delete_clipboard_folders,
    move_clipboard_elements_to_parent,
    remove_clipboard_item,
)


class PasteMoveElementsView(View):

    def post(self, request, folder_id):
        """
        View that moves a folder or document to another parent folder
        """
        move_clipboard_elements_to_parent(request, folder_id)

        return HttpResponseRedirect(
            reverse(
                "repo:folder",
                args=[folder_id],
            )
        )


class PasteCopyElementsView(View):
    def post(self, request, folder_id):
        """
        View that deep copies (sub folders and documents including version but not renditions) a folder or document to another parent folder
        """
        copy_clipboard_elements_to_parent(request, folder_id)

        return HttpResponseRedirect(
            reverse(
                "repo:folder",
                args=[folder_id],
            )
        )


class AddElementClipboardView(View):
    def _get_url_with_args(self, element, page_number=1, search_term=None):
        url = reverse(
            "repo:folder",
            args=[element.parent.pk],
        )

        if page_number > 1:  # pragma: no coverage
            url += f"?page={page_number}"

        if search_term:  # pragma: no coverage
            if page_number > 1:
                url += "&"
            else:
                url += "?"

            url += f"search_term={search_term}"

        return url

    def post(self, request, element_type, element_id):
        """
        View that puts folder or document into user's clipboard
        """
        clipboard, _ = Clipboard.objects.get_or_create(user=request.user)
        page_number = int(request.GET.get("page", 1))
        search_term = request.POST.get("search_term", None)
        is_summary = request.POST.get("scope", None)
        Model = get_model(element_type)
        element = Model.objects.get(pk=element_id)
        success = add_to_clipboard(request, clipboard, element)

        if not success:  # pragma: no coverage
            raise Http404

        if is_summary:  # pragma: no coverage
            return HttpResponseRedirect(
                reverse(
                    "repo:element_details",
                    args=[
                        element.parent.type,
                        element.parent.pk,
                    ],
                )
            )
        else:
            return HttpResponseRedirect(
                self._get_url_with_args(element, page_number, search_term)
            )


class RemoveItemView(View):
    """
    Removes a document or folder from a user's active clipboard
    """

    def post(self, request, item_type, item_id):  # pragma: no coverage
        """
        View to remove document or folder from clipboard
        """
        remove_clipboard_item(item_type, item_id)
        return HttpResponse("")


class RemoveDocumentsView(View):
    def post(self, request):
        try:
            delete_clipboard_documents(user=request.user)

            return HttpResponse("", status=200)

        except Clipboard.DoesNotExist:
            return HttpResponse("Clipboard not found", status=404)

        except Exception as e:  # pragma: no coverage
            return HttpResponse(f"Error: {str(e)}", status=500)


class RemoveFoldersView(View):
    def post(self, request):
        try:
            delete_clipboard_folders(user=request.user)

            return HttpResponse("", status=200)

        except Clipboard.DoesNotExist:
            return HttpResponse("Clipboard not found", status=404)

        except Exception as e:  # pragma: no coverage
            return HttpResponse(f"Error: {str(e)}", status=500)
