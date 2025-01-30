from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Tag

admin.site.register(Tag, ModelAdmin)
