from django.contrib import admin

from .models import Category, Company, Product


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "company",
        # "slug",
        # "price",
        "verified",
        # "created",
        "updated",
    ]
    list_filter = (
        "verified",
        "company__name",
        # "created",
        # "updated"
    )
    list_editable = [
        # "price",
        "verified"
    ]
    prepopulated_fields = {"slug": ("name",)}
