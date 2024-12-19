from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from apps.clipboard.models import Clipboard, PastedDocument, PastedFolder
from unfold import admin as unfold_admin
from unfold.admin import ModelAdmin
from apps.dashlets.models import Motd
from .models import Document, Folder, Version, Profile, Mimetype


class VersionInline(unfold_admin.TabularInline):
    model = Version
    extra = 0
    readonly_fields = ("pk",)


class ElementInline(unfold_admin.TabularInline):  # pragma: no coverage
    extra = 0
    readonly_fields = ("linked_name",)
    exclude = (
        "name",
        "title",
        "description",
        "owner",
        "is_hidden",
    )

    def linked_name(self, obj):
        url = reverse(self.base_url, args=[obj.pk])
        return format_html(
            f'<a href="{url}">{obj.name}</a>',
        )

    linked_name.short_description = "Name"  # type: ignore


class DocumentInline(ElementInline):
    model = Document
    base_url = "admin:repo_document_change"
    fk_name = "parent"


class FolderInline(ElementInline):
    model = Folder
    base_url = "admin:repo_folder_change"
    fk_name = "parent"


class BaseElementAdmin(ModelAdmin):  # pragma: no coverage
    list_display = (
        "name",
        "id",
        "full_path",
        "owner",
    )
    readonly_fields = ("id", "full_path")

    def full_path(self, obj):
        return obj.get_full_path()

    full_path.admin_order_field = "Full Path"  # type: ignore
    full_path.short_description = "Full Path"  # type: ignore


class DocumentAdmin(BaseElementAdmin):
    inlines = [VersionInline]


class FolderAdmin(BaseElementAdmin):
    inlines = [
        FolderInline,
        DocumentInline,
    ]


class VersionAdmin(ModelAdmin):
    list_display = (
        "id",
        "content_file",
        "tag",
        "parent",
    )
    readonly_fields = ("id",)


class ProfileAdmin(ModelAdmin):
    pass


# admin.site.register(Project, ModelAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Folder, FolderAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(Mimetype, ModelAdmin)
admin.site.register(Clipboard, ModelAdmin)
admin.site.register(PastedDocument, ModelAdmin)
admin.site.register(PastedFolder, ModelAdmin)
admin.site.register(Motd, ModelAdmin)
