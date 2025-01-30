from django.db.models import QuerySet

from apps.core.models import Element

from .models import Communication


def send_comm(
    from_user: str,
    to_group: QuerySet,
    subject: str,
    content: str,
    category: str | None = None,
    related_element: Element | None = None,
) -> None:
    for member in to_group:
        Communication.objects.create(
            msg_from=from_user,
            msg_to=member,
            subject=subject,
            content=content,
            category=category,
            related_element=related_element,
        )
