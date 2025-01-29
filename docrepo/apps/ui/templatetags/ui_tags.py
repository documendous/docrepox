from django import template

from apps.core.utils.core import str_to_bool
from apps.ui.models import Setting

register = template.Library()


@register.simple_tag
def ui_setting(request, key, type="bool"):
    if not request.user.is_authenticated:  # pragma: no coverage
        return None

    setting, created = Setting.objects.get_or_create(key=key, user=request.user)

    if type == "bool":
        if created:
            setting.value = "true"
            setting.save()

    return str_to_bool(setting.value)
