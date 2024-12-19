from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Bookmark


class BookmarkAdmin(ModelAdmin):  # pragma: no coverage
    list_display = ("element_name", "element_type", "owner")

    def element_name(self, obj: Bookmark) -> str:
        return str(obj.content_object)

    def element_type(self, obj: Bookmark) -> str:
        return obj.content_type.name


# Setting short descriptions for methods
setattr(BookmarkAdmin.element_name, "short_description", "Element Name")
setattr(BookmarkAdmin.element_type, "short_description", "Type")


admin.site.register(Bookmark, BookmarkAdmin)
