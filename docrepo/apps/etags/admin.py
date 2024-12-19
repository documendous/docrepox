from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Tag


admin.site.register(Tag, ModelAdmin)
