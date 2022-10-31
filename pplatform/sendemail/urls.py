from django.urls import path

from .views import contactView, successView

app_name = "pplatform.sendemail"

urlpatterns = [
    path("contact-us/", contactView, name="contact-us"),
    path("success/", successView, name="success"),
]
