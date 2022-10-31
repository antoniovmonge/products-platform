from django.urls import path

from . import views

app_name = "pplatform.selection"

urlpatterns = [
    path("", views.selection_detail, name="selection_detail"),
    path("add/<int:product_id>/", views.selection_add, name="selection_add"),
    path("remove/<int:product_id>/", views.selection_remove, name="selection_remove"),
]
