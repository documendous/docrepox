import logging

from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver

from .models import Clipboard


@receiver(user_logged_out)
def clear_user_clipboard(sender, user, request, **kwargs):  # pragma: no coverage
    """
    On user_logged_out event, the user's clipboard is deleted
    """
    log = logging.getLogger(__name__)
    try:
        clipboard = Clipboard.objects.get(user=user)
        clipboard.delete()
        log.debug(f"Clipboard of {user} cleared")
    except Clipboard.DoesNotExist:
        pass
