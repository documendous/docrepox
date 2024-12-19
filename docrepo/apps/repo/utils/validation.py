from ..settings import DUPLICATE_PEER_MSG


def has_duplicate_peers(parent, file_name):
    """
    A check for a folder or document having same name as other folders or documents with same parent
    """
    children = parent.get_children(include_hidden=True)
    for child in children:
        if file_name == child.name:
            add_msg = DUPLICATE_PEER_MSG.format(file_name)
            return add_msg
    return ""
