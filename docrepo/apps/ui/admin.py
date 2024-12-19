from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Setting


admin.site.register(Setting, ModelAdmin)
