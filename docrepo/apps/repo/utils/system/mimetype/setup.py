from apps.repo.models import Mimetype
from apps.repo.utils.system.mimetype.data import mimetypes


def add_mimetypes():
    mimetype_instances = [
        Mimetype(name=mt["name"], extension_list=", ".join(mt["extensions"]))
        for mt in mimetypes
    ]
    Mimetype.objects.bulk_create(mimetype_instances)
