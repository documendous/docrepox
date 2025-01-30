from django import template

from apps.repo import rules

register = template.Library()


@register.simple_tag
def is_admin_user(request) -> bool:  # pragma: no coverage
    """
    Return True if user is the system admin user
    """
    return request.user.profile.is_admin_user()


@register.simple_tag
def can_move_element(request, element) -> bool:
    return rules.can_move_element(request, element, from_tag=True)


@register.simple_tag
def can_view_element_details(request, element) -> bool:
    return rules.can_view_element_details(request, element, from_tag=True)


@register.simple_tag
def can_recycle_element(request, element) -> bool:
    return rules.can_recycle_element(request, element, from_tag=True)


@register.simple_tag
def can_restore_element(request, element) -> bool:
    return rules.can_restore_element(request, element, from_tag=True)


@register.simple_tag
def can_delete_element(request, element) -> bool:
    return rules.can_delete_element(request, element, from_tag=True)


@register.simple_tag
def can_create_document(request, parent) -> bool:  # pragma: no coverage
    return rules.can_create_document(request, parent, from_tag=True)


@register.simple_tag
def can_create_folder_children(request, parent) -> bool:
    return rules.can_create_folder_children(request, parent, from_tag=True)


@register.simple_tag
def can_update_element(request, element) -> bool:
    return rules.can_update_element(request, element, from_tag=True)


@register.simple_tag
def can_bookmark(request, element) -> bool:
    return rules.can_bookmark(request, element, from_tag=True)


@register.simple_tag
def can_delete_comment(
    request,
    comment_id,
    element_type,
    element_id,
) -> bool:
    return rules.can_delete_comment(
        request,
        comment_id,
        element_type,
        element_id,
        from_tag=True,
    )
