from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.transformations.models import Preview, Thumbnail


admin.site.register(Preview, ModelAdmin)
admin.site.register(Thumbnail, ModelAdmin)
