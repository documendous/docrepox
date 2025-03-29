from django import template

from apps.repo import rules

register = template.Library()


@register.simple_tag
def is_admin_user(user) -> bool:  # pragma: no coverage
    """
    Return True if user is the system admin user
    """
    return user.profile.is_admin_user()


@register.simple_tag
def can_move_element(user, element) -> bool:
    return rules.can_move_element(user, element, from_tag=True)


@register.simple_tag
def can_view_element_details(user, element) -> bool:
    return rules.can_view_element_details(user, element, from_tag=True)


@register.simple_tag
def can_retrieve_document(user, document) -> bool:  # pragma: no coverage
    return rules.can_retrieve_document(user, document, from_tag=True)


@register.simple_tag
def can_recycle_element(user, element) -> bool:
    return rules.can_recycle_element(user, element, from_tag=True)


@register.simple_tag
def can_restore_element(user, element) -> bool:
    return rules.can_restore_element(user, element, from_tag=True)


@register.simple_tag
def can_delete_element(user, element) -> bool:
    return rules.can_delete_element(user, element, from_tag=True)


@register.simple_tag
def can_delete_property(user, property) -> bool:  # pragma: no coverage
    return rules.can_delete_property(user, property, from_tag=True)


@register.simple_tag
def can_update_property(user, property) -> bool:  # pragma: no coverage
    return rules.can_update_property(user, property, from_tag=True)


@register.simple_tag
def can_create_document(user, parent) -> bool:  # pragma: no coverage
    return rules.can_create_document(user, parent, from_tag=True)


@register.simple_tag
def can_add_webproxy(user, element) -> bool:
    return rules.can_add_webproxy(user, element, from_tag=True)


@register.simple_tag
def can_create_folder_children(user, parent) -> bool:
    return rules.can_create_folder_children(user, parent, from_tag=True)


@register.simple_tag
def can_update_element(user, element) -> bool:
    return rules.can_update_element(user, element, from_tag=True)


@register.simple_tag
def can_update_content(user, element) -> bool:
    return rules.can_update_content(user, element, from_tag=True)


@register.simple_tag
def can_bookmark(user, element) -> bool:
    return rules.can_bookmark(user, element, from_tag=True)


@register.simple_tag
def can_delete_comment(
    user,
    comment_id,
    element_type,
    element_id,
) -> bool:
    return rules.can_delete_comment(
        user,
        comment_id,
        element_type,
        element_id,
        from_tag=True,
    )
