from django import template

from apps.comms.models import Communication

register = template.Library()


@register.simple_tag
def has_unread_comms(user) -> bool:  # pragma: no coverage
    """
    Return True/False based on if user has unacknowledged communications
    """
    return Communication.objects.filter(
        acknowledged=False,
        msg_to=user,
    ).exists()
