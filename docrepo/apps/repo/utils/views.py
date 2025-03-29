from django.apps import apps
from django.conf import settings
from django.shortcuts import get_object_or_404

from apps.repo import rules
from apps.repo.forms.element import AddFolderForm
from apps.repo.models.element.document import Document
from apps.repo.models.element.version import Version
from apps.repo.utils.document import create_version, set_mimetype
from apps.repo.utils.model import get_path_with_links
from apps.repo.utils.system.object import get_system_root_folder


class DocumentCreator:
    """
    Class for creating documents
    """

    def _set_mimetype(self, document, mimetype=None):  # pragma: no coverage
        """
        Sets mimetype for a document
        """
        set_mimetype(document, mimetype=mimetype)

    def _get_common_context(self, parent, request):
        """
        Returns common context for a Document view
        """
        return {
            "folder": parent,
            "add_document_form": self.document_form,
            "add_folder_form": AddFolderForm(),
            "home_folder_id": request.user.profile.home_folder.id,
            "root_folder_id": get_system_root_folder().id,
            "children": parent.get_children(),
            "path_with_links": get_path_with_links(parent, request.user),
            "has_document_errors": self.has_document_errors,
            "has_multi_document_errors": 0,
            "has_create_document_errors": 0,
            "has_folder_errors": 0,
            "create_doc_use_modal": settings.CREATE_DOC_USE_MODAL,
        }

    def _create_version(self, document, version_form, mimetype=None):
        """
        Creates the versioned file for a document
        """
        create_version(
            document=document,
            content_file=version_form.cleaned_data.get("content_file"),
            mimetype=mimetype,
        )


class DocumentRetriever:
    """
    Class for retrieving documents
    """

    def _get_file(self, request, parent_id, parent_type="Document", version_tag=None):
        """
        Returns document and physical file path
        """
        Model = apps.get_model("repo", parent_type)

        document = get_object_or_404(
            Model,
            pk=parent_id,
        )

        rules.can_view_element_details(request.user, document)
        version = get_version(version_tag, document)

        if version and hasattr(version, "content_file"):
            file_path = version.content_file.path
        else:
            file_path = None  # pragma: no coverage

        return (document, file_path)


def get_version(version_tag: str, document: Document) -> Version:
    if version_tag:  # pragma: no coverage
        return Version.objects.get(parent=document, tag=version_tag)
    else:
        return (
            Version.objects.filter(
                parent=document,
            )
            .order_by("-created")
            .first()
        )
