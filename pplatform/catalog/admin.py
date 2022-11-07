from django.contrib import admin

from .models import Category, Product, ProductDetail


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


@admin.register(ProductDetail)
class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ["product", "declared_unit"]
    list_filter = ("declared_unit",)
