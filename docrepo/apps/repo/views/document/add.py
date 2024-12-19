import logging
from apps.repo.forms.element import AddVersionForm
from apps.repo.views.document.abstract import BaseCreateDocumentView


class AddDocumentView(BaseCreateDocumentView):
    """
    View for adding single document upload
    """

    log = logging.getLogger(__name__)
    template_name = "repo/element_list.html"

    def _set_extra_context(self):
        self.context.update({"add_version_form": self.add_version_form})

    def _set_version_form(self, request):
        self.version_form = AddVersionForm(request.POST, request.FILES)
