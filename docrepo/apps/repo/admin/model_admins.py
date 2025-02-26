from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.urls import reverse
from django.utils.html import format_html

from ..models.element.document import Document
from ..models.element.folder import Folder
from ..models.element.version import Version


class VersionInline(admin.TabularInline):
    model = Version
    extra = 0
    readonly_fields = ("pk",)


class ElementInline(admin.TabularInline):  # pragma: no coverage
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
