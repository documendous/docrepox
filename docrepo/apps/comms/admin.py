from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Communication

admin.site.register(Communication, ModelAdmin)
