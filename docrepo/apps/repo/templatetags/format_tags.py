from django import template

register = template.Library()


@register.filter
def human_readable_size(size):  # pragma: no coverage
    """
    Returns a human readable file size
    """
    if size is None or size == "":
        return "--"

    units = ["B", "KB", "MB", "GB", "TB", "PB"]

    for unit in units:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0

    return f"{size:.2f} PB"  # In case size is very large


@register.filter
def bool_to_int(value):  # pragma: no coverage
    """
    Returns an int for bool (1 for True/0 for False), mainly used for Django to Javascript conversions.
    """
    return 1 if value else 0
