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
        "category",
        "verified",
        "status",
        "updated",
    ]
    list_filter = (
        "verified",
        "company__name",
        "category",
        # "updated"
    )
    search_fields = ["name", "company__name", "category__name"]
    list_editable = ["status", "verified"]
    prepopulated_fields = {"slug": ("name",)}
    raw_id_fields = ["company", "created_by"]
    date_hierarchy = "updated"
