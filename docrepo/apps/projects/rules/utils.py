def get_project_for_element(element):
    """
    Retrieves the parent project for a given element, if available.
    - Returns None if no project is associated.
    """
    parent = getattr(element, "parent", None)
    orig_parent = getattr(element, "orig_parent", None)

    if parent:
        return getattr(parent, "parent_project", None) or getattr(
            orig_parent, "parent_project", None
        )

    elif element.type == "project":
        return element

    return None
