from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SendemailConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pplatform.sendemail"
    verbose_name = _("Send Emails")
