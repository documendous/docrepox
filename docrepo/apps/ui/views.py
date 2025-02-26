from django.http import HttpResponseRedirect
from django.urls import reverse

from apps.core.views import View

from .models import Setting


class ModifySettingsView(View):
    def get(self, request, key, value):
        setting, _ = Setting.objects.get_or_create(key=key, user=request.user)
        setting.value = value
        setting.save()
        next = request.GET.get("next", None)

        if next:
            url = f"repo:{next}"
        else:
            url = "repo:index"

        return HttpResponseRedirect(reverse(url))
