from .utils import BASE_DIR

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

STATIC_ROOT = "/tmp/staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "staticfiles",
    BASE_DIR / "extensions" / "staticfiles",
]

MEDIA_URL = "media/"

MEDIA_ROOT = BASE_DIR / "mediafiles"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
