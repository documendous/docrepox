from config.settings import INSTALLED_APPS

unfold_app = "unfold"
admin_index = INSTALLED_APPS.index("django.contrib.admin")
INSTALLED_APPS.insert(admin_index, unfold_app)

# Unfold Settings

UNFOLD = {
    "SITE_TITLE": "Documendous",
    "SITE_HEADER": None,
}
