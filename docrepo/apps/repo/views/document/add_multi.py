from django.contrib import messages
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from apps.repo import rules
from apps.repo.models.element.document import Document
from apps.repo.models.element.folder import Folder
from apps.repo.models.element.version import Version
from apps.repo.utils.helpers import create_with_new_name
from apps.repo.views.document.abstract import BaseCreateDocumentView


class AddMultiDocumentsView(BaseCreateDocumentView):  # pragma: no coverage
    """
    View for adding multiple documents upload
    """

    def post(self, request, folder_id):
        parent = get_object_or_404(Folder, pk=folder_id)
        rules.can_create_document(request, parent)
        info_message = ""
        error_message = ""

        if request.FILES:
            for f in self.request.FILES.getlist("content_file"):
                try:
                    new_document = Document.objects.create(
                        name=f.name, parent=parent, owner=request.user
                    )
                except IntegrityError:
                    new_document = create_with_new_name(
                        "document", f.name, request.user, parent
                    )
                if new_document:
                    Version.objects.create(parent=new_document, content_file=f)
                    self._set_mimetype(new_document)
                    info_message += f"<li>{f.name}</li>"

            if info_message:
                messages.info(
                    request,
                    f"<p>The following documents were succcessfully uploaded:</p><p><ul>{info_message}</ul><p>",
                )

            if error_message:
                messages.error(
                    request,
                    f"<p>The following documents already exist and cannot be created here:</p><p><ul>{error_message}</ul><p>",
                )

        return HttpResponseRedirect(
            reverse(
                "repo:folder",
                args=[
                    parent.pk,
                ],
            )
        )
