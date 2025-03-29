from .models import ProxiedDocument


def is_proxied_by_user(document, user):  # pragma: no coverage
    if document.type == "document":
        return ProxiedDocument.objects.filter(
            document=document,
            manager=user,
        ).exists()

    return False
