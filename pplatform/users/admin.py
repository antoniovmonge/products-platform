from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from pplatform.users.forms import CustomUserChangeForm, CustomUserCreationForm
from pplatform.users.models import CustomUser


# @admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = (
        "email",
        "name",
        "company_own",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "company_own",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (_("Company"), {"fields": ("company_own",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    search_fields = ("email", "name", "company_own__name")
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)
