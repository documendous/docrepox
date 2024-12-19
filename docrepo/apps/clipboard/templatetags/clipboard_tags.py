from django import template
from apps.clipboard.models import Clipboard

register = template.Library()


@register.simple_tag
def element_in_clipboard(request, element):  # pragma: no coverage
    """
    Checks if element (document or folder) is in the user's clipboard
    """
    try:
        clipboard = Clipboard.objects.get(user=request.user)
    except Clipboard.DoesNotExist:
        return False

    if element.type == "document":
        return clipboard.documents.filter(document=element).exists()
    elif element.type == "folder":
        return clipboard.folders.filter(folder=element).exists()
    else:
        return False
