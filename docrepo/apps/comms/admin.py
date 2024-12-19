from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Communication


admin.site.register(Communication, ModelAdmin)
