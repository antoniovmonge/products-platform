from django.urls import path

from . import views

app_name = "pplatform.catalog"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path(
        "category/<slug:category_slug>/",
        views.product_list,
        name="product_list_by_category",
    ),
    path(
        "company/<slug:company_slug>/",
        views.product_list,
        name="product_list_by_company",
    ),
    # path("product/<int:id>/<slug:slug>/", views.product_detail, name="product_detail"),
    path(
        "product/<int:year>/<int:month>/<int:day>/<slug:slug>/",
        views.product_detail,
        name="product_detail",
    ),
    path(
        "manage/my-products/",
        views.ManageProductListView.as_view(),
        name="manage_product_list",
    ),
    path("manage/create/", views.ProductCreateView.as_view(), name="product_create"),
    path(
        "manage/product/<pk>/edit/",
        views.ProductUpdateView.as_view(),
        name="product_edit",
    ),
    path(
        "manage/product/<pk>/delete/",
        views.ProductDeleteView.as_view(),
        name="product_delete",
    ),
    path(
        "manage/product/<int:product_id>/content/<model_name>/create/",
        views.ContentCreateUpdateView.as_view(),
        name="product_content_create",
    ),
    path(
        "manage/product/<int:product_id>/content/<model_name>/<id>/",
        views.ContentCreateUpdateView.as_view(),
        name="product_content_update",
    ),
    path(
        "manage/content/<int:id>/delete/",
        views.ContentDeleteView.as_view(),
        name="product_content_delete",
    ),
    path(
        "manage/product/<int:id>/content/",
        views.ProductContentListView.as_view(),
        name="product_content_list",
    ),
]

new_urlpatterns = [
    path("manage/products/", views.ProductList.as_view(), name="product-list-htmx"),
]

htmx_urlpatterns = [
    path("manage/add-product/", views.add_product, name="add-product"),
    path(
        "manage/delete-product/<int:pk>/", views.delete_product, name="delete-product"
    ),
]

urlpatterns += new_urlpatterns + htmx_urlpatterns
