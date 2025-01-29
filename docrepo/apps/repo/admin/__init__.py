import logging

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.clipboard.models import Clipboard, PastedDocument, PastedFolder
from apps.dashlets.models import Motd

from ..models import Document, Folder, Mimetype, Profile, Version
from .model_admins import DocumentAdmin, FolderAdmin, ProfileAdmin, VersionAdmin

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Folder, FolderAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(Mimetype, ModelAdmin)
admin.site.register(Clipboard, ModelAdmin)
admin.site.register(PastedDocument, ModelAdmin)
admin.site.register(PastedFolder, ModelAdmin)
admin.site.register(Motd, ModelAdmin)

log = logging.getLogger(__name__)

try:
    from extensions.apps.repo.admin import *  # noqa: F403, F401
except ModuleNotFoundError:  # pragma: no coverage
    log.warning("Expected module: 'admin' in extensions not found")
