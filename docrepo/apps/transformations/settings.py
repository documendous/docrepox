# Transformations
from django.conf import settings

SOFFICE_EXE = (
    "/usr/bin/soffice"  # Path to open/libre/star office executable for transformations
)

SOFFICE_TEMP_DIR = settings.BASE_DIR / "mediafiles/content/tmp"  # Temp dir for soffice

ALLOWED_PREVIEW_TYPES = (
    ".conf",
    ".doc",
    ".docx",
    ".gif",
    ".html",
    ".jpg",
    ".jpeg",
    ".md",
    ".pdf",
    ".png",
    ".ppt",
    ".pptx",
    ".txt",
    ".xls",
    ".xlsx",
    ".xml",
)  # Allowed previewable types

MAX_PREVIEW_SIZE = 10000000  # Max size in bytes allowed for preview transformation

RENDER_HTML_PREVIEW = False

"""
Replaces problematic characters in a text file that interfere with LibreOffice PDF output.
    - Converts smart quotes to straight quotes
    - Replaces em/en dashes with regular dashes
    - Limits underscore sequences
Warning: Setting to True replaces the content of your text file to allow for successful conversion to PDF.
"""
SANITIZE_TEXT_FILES = False

TRANSFORMABLE_TYPES = (
    ".doc",
    ".docx",
    ".md",
    ".ppt",
    ".pptx",
    ".txt",
    ".xls",
    ".xlsx",
)  # Allowed transformable types to PDF
