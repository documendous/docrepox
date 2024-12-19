from django.apps import apps


def get_model(element_type):
    try:
        Model = apps.get_model("repo", element_type)
    except LookupError:
        Model = apps.get_model("projects", element_type)
    return Model
