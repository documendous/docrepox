import logging

from django.apps import apps
from django.db.models import Model
from django.http import Http404


def get_model(element_type: str) -> Model:
    """
    A helper function to get a model object by its name.
    Returns a 404 to users if the model is not found, while logging the error.
    """
    log = logging.getLogger(__name__)
    log.debug(f"Attempting to lookup model: {element_type}")
    try:
        Model = apps.get_model("repo", element_type)
        log.debug("Model found in 'repo'.")
    except LookupError:
        try:
            Model = apps.get_model("projects", element_type)
            log.debug("Model found in 'projects'.")
        except LookupError:  # pragma: no coverage
            log.error(
                f"Access denied or invalid model lookup: {element_type}", exc_info=True
            )
            raise Http404(f"The requested resource '{element_type}' was not found.")
    return Model


def is_a_user_home_folder(folder) -> bool:
    Profile = apps.get_model("repo", "Profile")
    return True if Profile.objects.filter(home_folder=folder).exists() else False
