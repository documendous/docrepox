import logging
from typing import List, Tuple

from django.conf import settings
from django.contrib import messages
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from apps.core.utils.core import get_extension
from apps.repo import rules
from apps.repo.models.element.document import Document
from apps.repo.models.element.folder import Folder
from apps.repo.models.element.version import Version
from apps.repo.utils.helpers import create_with_new_name
from apps.repo.views.document.abstract import BaseCreateDocumentView
from apps.search.models import DocumentIndex


class AddMultiDocumentsView(BaseCreateDocumentView):  # pragma: no coverage
    """
    View for adding multiple documents upload
    """

    MAX_MESSAGE_SIZE = 10

    def _process_files(
        self, files: List, parent: Folder, user
    ) -> Tuple[List[str], List[str]]:
        log = logging.getLogger(__name__)
        info_message_list = []
        error_message_list = []

        for f in files[: settings.DATA_UPLOAD_MAX_NUMBER_FILES]:
            try:
                new_document = Document.objects.create(
                    name=f.name, parent=parent, owner=user
                )
            except IntegrityError:
                new_document = create_with_new_name("document", f.name, user, parent)

            if new_document:
                Version.objects.create(parent=new_document, content_file=f)
                self._set_mimetype(new_document)
                info_message_list.append(f.name)
            else:
                error_message_list.append(f.name)

            extension = get_extension(file_name=new_document.name)

            if settings.ENABLE_FULL_TEXT_SEARCH and (
                extension in settings.TRANSFORMABLE_TYPES or extension.lower() == ".pdf"
            ):
                log.debug(f"Creating document index for document: {new_document.name}")
                DocumentIndex.objects.create(document=new_document)
                log.debug("Successfully created")

        return info_message_list, error_message_list

    def post(self, request, folder_id) -> HttpResponseRedirect:
        parent = get_object_or_404(Folder, pk=folder_id)
        rules.can_create_document(request.user, parent)
        uploaded_files = request.FILES.getlist("content_file")

        info_message_list, error_message_list = self._process_files(
            uploaded_files, parent, request.user
        )

        if info_message_list:
            self._add_success_message(request, info_message_list)

        if error_message_list:
            self._add_error_message(request, error_message_list)

        return HttpResponseRedirect(reverse("repo:folder", args=[parent.pk]))

    def _add_success_message(self, request, file_names: List[str]):
        extra_message = ""

        if len(file_names) > self.MAX_MESSAGE_SIZE:
            extra_message = f"... and {len(file_names) - self.MAX_MESSAGE_SIZE} more."

        message_content = (
            f"The following documents were successfully uploaded:<ul class='text-left mb-2'>"
            f"{''.join(f'<li class="ml-2">- {name}</li>' for name in file_names[:self.MAX_MESSAGE_SIZE])}"
            f"</ul>{extra_message}"
        )

        messages.info(request, message_content)

    def _add_error_message(self, request, file_names: List[str]):
        message_content = (
            f"The following documents could not be created:<ul>"
            f"{''.join(f'<li>{name}</li>' for name in file_names)}"
            f"</ul>"
        )

        messages.error(request, message_content)
