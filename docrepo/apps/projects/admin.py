from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Project

admin.site.register(Project, ModelAdmin)
