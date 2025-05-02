import logging

from django.contrib.auth.models import User
from django.db.models import QuerySet

from apps.core.models import Element

from .models import Communication


def create_comm(
    from_user: str,
    to_group: QuerySet,
    subject: str,
    content: str,
    category: str | None = None,
    related_element: Element | None = None,
) -> None:
    """Creates a communication instance"""
    for member in to_group:
        Communication.objects.create(
            msg_from=from_user,
            msg_to=member,
            subject=subject,
            content=content,
            category=category,
            related_element=related_element,
        )


def acknowledge_comm(user: User, object_id) -> None:  # pragma: no coverage
    """Acknowledges a communication instance"""
    log = logging.getLogger(__name__)

    try:
        communication = Communication.objects.get(
            object_id=object_id,
            msg_from=user,
            acknowledged=False,
        )

        communication.set_acknowledged()
        log.info("Associated communication marked as acknowledged.")

    except Communication.DoesNotExist:
        log.info("Associated communication does not exist. Nothing to delete.")
