import logging
from datetime import datetime

from django.apps import apps

from apps.core.utils.core import get_name_and_ext


def create_with_new_name(
    model_type, name, owner, parent, title=None, description=None, set_pk_none=False
):  # pragma: no coverage
    """
    Allows for creation of an element (folder or document) with a
    non-default name if the element failed creation due to invalid name
    """
    log = logging.getLogger(__name__)
    timestamp = datetime.now().strftime("%m%d%Y-%H%M-%S.%f")[:-3]
    file_name, ext = get_name_and_ext(file_name=name)
    Model = apps.get_model("repo", model_type)
    model = Model()
    model.name = f"{file_name}-{timestamp}{ext}"
    model.title = title
    model.description = description
    model.owner = owner
    model.parent = parent

    if set_pk_none:
        model.pk = None

    model.save()
    log.debug(f"{file_name} changed to {model.name}")
    log.debug(f"{model.name} moved to new parent {model.parent}")

    return model


def update_with_new_name(model):  # pragma: no coverage
    """
    Changes name of the element (folder or document) when moving to
    a new location where the element name clashes with a pre-existing one
    """
    log = logging.getLogger(__name__)
    timestamp = datetime.now().strftime("%m%d%Y-%H%M-%S.%f")[:-3]
    file_name, ext = get_name_and_ext(file_name=model.name)
    model.name = f"{file_name}-{timestamp}{ext}"
    model.save()
    log.debug(f"{file_name} changed to {model.name}")

    return model
