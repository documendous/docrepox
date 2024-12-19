"""
System functions that don't require the import of models
"""


def is_system_projects_folder(folder):
    """
    Returns True if folder is the system projects folder (/ROOT/Projects)
    """
    return folder.name == "Projects" and folder.parent.name == "ROOT"
