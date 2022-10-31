from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SelectionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pplatform.selection"
    verbose_name = _("Selection")
