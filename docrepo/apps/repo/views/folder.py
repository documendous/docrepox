import logging

from django.conf import settings
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.defaultfilters import truncatechars
from django.urls import reverse

from apps.clipboard.models import Clipboard
from apps.core.views import View
from apps.repo import rules
from apps.repo.forms.element import AddDocumentForm, AddFolderForm, AddVersionForm
from apps.repo.models.element.folder import Folder
from apps.repo.utils.helpers import create_with_new_name
from apps.repo.utils.model import get_path_with_links
from apps.repo.utils.system.object import (
    get_system_projects_folder,
    get_system_root_folder,
)


class FolderView(View):
    """
    View for listing of document and folders
    """

    log = logging.getLogger(__name__)
    template_name = "repo/element_list.html"
    paginate_by = settings.FOLDER_VIEW_PAGINATE_BY

    def _include_hidden(self):
        return self.request.user.is_superuser

    def _set_common_context(self, parent, request, order_by_filter=None):
        add_folder_form = AddFolderForm()
        add_document_form = AddDocumentForm()
        add_version_form = AddVersionForm()
        home_folder = request.user.profile.home_folder
        root_folder = get_system_root_folder()
        path_with_links = get_path_with_links(parent, request.user)

        children = parent.get_children(
            include_hidden=self._include_hidden(), order_by_filter=order_by_filter
        )

        clipboard, _ = Clipboard.objects.get_or_create(user=request.user)

        self.context = {
            "add_document_form": add_document_form,
            "add_folder_form": add_folder_form,
            "add_version_form": add_version_form,
            "children": children,
            "folder": parent,
            "home_folder_id": home_folder.id,
            "path_with_links": path_with_links,
            "root_folder_id": root_folder.id,
            "has_folder_errors": 0,
            "has_document_errors": 0,
            "has_multi_document_errors": 0,
            "has_create_document_errors": 0,
            "clipboard_documents": clipboard.documents.all(),
            "clipboard_folders": clipboard.folders.all(),
            "create_doc_use_modal": settings.CREATE_DOC_USE_MODAL,
            "use_hx_boost_ext": settings.USE_HX_BOOST_EXT,
            "use_hx_boost_int": settings.USE_HX_BOOST_INT,
            "max_upload_files": settings.DATA_UPLOAD_MAX_NUMBER_FILES,
        }

    def get(self, request, folder_id):
        parent = get_object_or_404(Folder, pk=folder_id)
        rules.can_view_folder(request, parent)

        if parent == get_system_projects_folder():
            return HttpResponseRedirect(reverse("repo:projects:index"))

        self._set_common_context(parent, request)
        order_by_filter = request.GET.get("order_by", None)
        search_term = request.GET.get("search_term", None)

        children = parent.get_children(
            include_hidden=self._include_hidden(),
            order_by_filter=order_by_filter,
            search_term=search_term,
        )

        paginator = Paginator(children, self.paginate_by)
        page = request.GET.get("page", 1)

        try:
            paginated_children = paginator.page(page)  # pragma: no coverage
        except PageNotAnInteger:  # pragma: no coverage
            paginated_children = paginator.page(1)
        except EmptyPage:  # pragma: no coverage
            paginated_children = paginator.page(paginator.num_pages)

        self._set_common_context(parent, request, order_by_filter=order_by_filter)
        self.context["children"] = paginated_children

        if search_term:  # pragma: no coverage
            self.context["search_term"] = search_term

        return render(request, self.template_name, self.context)

    def post(self, request, folder_id):
        parent = get_object_or_404(Folder, pk=folder_id)
        rules.can_create_folder_children(request, parent)

        name = request.POST.get("name", None)
        title = request.POST.get("title", None)
        description = request.POST.get("description", None)
        add_folder_form = AddFolderForm(request.POST)
        self._set_common_context(parent, request)

        if name:
            try:
                Folder.objects.create(
                    name=name,
                    title=title,
                    description=description,
                    owner=request.user,
                    parent=parent,
                )

                messages.add_message(
                    request,
                    messages.INFO,
                    f'Folder "{truncatechars(name, 30)}" was successfully created.',
                )

                return HttpResponseRedirect(
                    reverse(
                        "repo:folder",
                        args=[parent.id],
                    )
                )

            except IntegrityError:  # pragma: no coverage
                create_with_new_name(
                    "folder", name, request.user, parent, title, description
                )

                return HttpResponseRedirect(
                    reverse(
                        "repo:folder",
                        args=[parent.id],
                    )
                )

            except Exception as e:  # pragma: no coverage
                self.log.exception("Error creating folder")
                add_folder_form.add_error(None, str(e))

        self.context["add_folder_form"] = add_folder_form
        self.context["has_folder_errors"] = 1

        return render(request, self.template_name, self.context)
