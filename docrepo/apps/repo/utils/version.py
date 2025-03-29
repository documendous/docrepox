import logging

from ..models.element.document import Document
from ..models.element.version import Version


def update_version_tag(change_type: str, document: Document) -> str:
    """
    Updates a version tag: version is 0.0 formatted string
    'minor' updates by 0.1
    'major' updates by 1.0
    """
    current_version_tag = document.current_version_tag
    tag = current_version_tag
    major = int(tag.split(".")[0])
    minor = int(tag.split(".")[1])

    if change_type == "Major":
        major += 1
        minor = 0

    else:
        minor += 1

    return f"{major}.{minor}"


def get_content_from_version(version: Version) -> str:
    # Read content from the latest version if available
    initial_content = ""

    if version and version.content_file:
        try:
            with version.content_file.open("r") as file:
                initial_content = file.read()

        except Exception as err:  # pragma: no coverage
            log = logging.getLogger(__name__)
            log.error(
                f"Error reading content for document id {version.parent.pk}: {err}"
            )

    return initial_content
