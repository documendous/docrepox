from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Setting

admin.site.register(Setting, ModelAdmin)
