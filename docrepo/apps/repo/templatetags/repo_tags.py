from django import template
from apps.repo.utils.system.object import get_admin_user


register = template.Library()


@register.simple_tag
def is_admin_user(request) -> bool:  # pragma: no coverage
    """
    Return True if user is the system admin user
    """
    user = request.user
    return user == get_admin_user()
