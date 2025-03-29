from django import template

from ..utils import is_proxied_by_user

register = template.Library()


@register.simple_tag
def document_is_proxied(user, element) -> bool:  # pragma: no coverage
    return is_proxied_by_user(document=element, user=user)
