import logging
from typing import Any

from django.contrib import messages
from django.views import View as DjangoView


class MultipleFormView(DjangoView):
    """View for handling multiple form saves"""

    def _save_multi_forms(
        self,
        forms,
        success_msg,
        error_msg,
    ):
        try:
            for form in forms:
                form.save()
            messages.add_message(
                self.request,
                messages.SUCCESS,
                success_msg,
            )
        except Exception as err:  # pragma: no cover
            messages.add_message(
                self.request,
                messages.ERROR,
                error_msg,
            )
            self.log(repr(err))


class View(DjangoView):
    """
    Standard view for views
    """

    context: dict[str, Any] = {}

    def dispatch(self, request, *args, **kwargs):
        log = logging.getLogger(__name__)
        log.debug(
            f"{self.__class__.__name__} view called with {request.method} method."
        )
        return super().dispatch(request, *args, **kwargs)
