from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Project


admin.site.register(Project, ModelAdmin)
