from django.apps import apps
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count, Q
from django.forms.models import modelform_factory
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from pplatform.selection.forms import SelectionAddProductForm
from pplatform.selection.selection import Selection

from .models import Category, Company, Content, Product
from .utils import paginate_products, search_products

User = get_user_model()


def product_list(request, category_slug=None, company_slug=None):
    category = None
    # We count the products with a PB (Published) status
    categories = Category.objects.annotate(
        total_products=Count("products", filter=Q(products__status="PB"))
    )
    company = None
    companies = Company.objects.annotate(
        total_products=Count("products", filter=Q(products__status="PB"))
    )
    total_products = Product.published.all()

    # THE NEXT LINE IS INCLUDED IN "utils.py" UNDER THE "search_products()" function
    # products = Product.published.all()

    # Search Query
    products, search_query = search_products(request)

    # Filters on sidebar
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    if company_slug:
        company = get_object_or_404(Company, slug=company_slug)
        products = products.filter(company=company)

    # Paginator
    custom_range, products = paginate_products(request, products, 12)

    # Add selection to be able to check if the products are
    # already selected for comparison.
    selection = Selection(request)
    selection_list = str([item for item in selection])
    context = {
        "category": category,
        "categories": categories,
        "company": company,
        "companies": companies,
        "products": products,
        "selection_list": selection_list,
        "search_query": search_query,
        "custom_range": custom_range,
        "total_products": total_products,
    }
    return render(request, "catalog/product/list.html", context)


def product_detail(request, year, month, day, slug):
    product = get_object_or_404(
        Product,
        # id=id,
        slug=slug,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    # SELECTION is for adding to the comparison list
    selection_product_form = SelectionAddProductForm()
    selection = Selection(request)
    selection_list = str([item for item in selection])

    context = {
        "product": product,
        "selection_product_form": selection_product_form,
        "selection_list": selection_list,
    }
    return render(request, "catalog/product/detail.html", context)


# class ManageProductListView(ListView):
#     model = Product
#     template_name = "catalog/manage/product/list.html"

#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(company=self.request.user.company_own)


class CompanyOwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(company=self.request.user.company_own)


class CompanyOwnerEditMixin:
    def form_valid(self, form):
        form.instance.company = self.request.user.company_own
        return super().form_valid(form)


class CompanyOwnerProductMixin(
    CompanyOwnerMixin, LoginRequiredMixin, PermissionRequiredMixin
):
    model = Product
    fields = ["category", "name", "description"]
    success_url = reverse_lazy("catalog:manage_product_list")


class CompanyOwnerProductEditMixin(CompanyOwnerProductMixin, CompanyOwnerEditMixin):
    template_name = "catalog/manage/product/manage-product.html"


class ManageProductListView(CompanyOwnerProductMixin, ListView):
    template_name = "catalog/manage/product/list.html"
    permission_required = "catalog.view_product"


class ProductCreateView(CompanyOwnerProductEditMixin, CreateView):
    permission_required = "catalog.add_product"


class ProductUpdateView(CompanyOwnerProductEditMixin, UpdateView):
    permission_required = "catalog.change_product"


class ProductDeleteView(CompanyOwnerProductMixin, DeleteView):
    template_name = "catalog/manage/product/delete.html"
    permission_required = "catalog.delete_product"


class ContentCreateUpdateView(TemplateResponseMixin, View):
    product = None
    model = None
    obj = None
    template_name = "catalog/manage/content/form.html"

    def get_model(self, model_name):
        if model_name in ["text", "video", "image", "file"]:
            return apps.get_model(app_label="catalog", model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=["company", "created", "updated"])
        return Form(*args, **kwargs)

    def dispatch(self, request, product_id, model_name, id=None):
        self.product = get_object_or_404(
            Product, id=product_id, company=request.user.company_own
        )
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(
                self.model, id=id, company=request.user.company_own
            )

        return super().dispatch(request, product_id, model_name, id)

    def get(self, request, product_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({"form": form, "object": self.obj})

    def post(self, request, product_id, model_name, id=None):
        form = self.get_form(
            self.model, instance=self.obj, data=request.POST, files=request.FILES
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.company = request.user.company_own
            obj.save()
            if not id:
                # New content
                Content.objects.create(product=self.product, item=obj)
            return redirect("catalog:product_content_list", self.product.id)
        return self.render_to_response({"form": form, "object": self.obj})


class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(
            Content, id=id, product__company=request.user.company_own
        )
        product = content.product
        content.item.delete()
        content.delete()
        return redirect("catalog:product_content_list", product.id)


class ProductContentListView(TemplateResponseMixin, View):
    template_name = "catalog/manage/product/content_list.html"

    def get(self, request, id):
        product = get_object_or_404(Product, id=id, company=request.user.company_own)
        return self.render_to_response({"product": product})


# New views for htmx


class ProductList(CompanyOwnerProductMixin, ListView):
    template_name = "catalog/manage/product/htmx/products.html"
    permission_required = "catalog.view_product"
    model = Product
    context_object_name = "products"

    def get_queryset(self):
        company = self.request.user.company_own
        return company.products.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["categories"] = Category.objects.all()
        return context


@login_required
def add_product(request):
    name = request.POST.get("product-name")
    category_name = request.POST.get("category")
    category = Category.objects.get(name=category_name)
    company_name = request.user.company_own
    company = Company.objects.get(name=company_name)

    # create the product
    if name:
        Product.objects.create(
            name=name,
            category=category,
            company=company,
            status="PB",  # For testing
        )

        # return template with all of the company's products
        products = request.user.company_own.products.all()
        return render(
            request,
            "catalog/manage/product/htmx/partials/product-list.html",
            {"products": products},
        )


@login_required
@require_http_methods(["DELETE"])
def delete_product(request, pk):
    # remove the product
    request.user.company_own.products.filter(pk=pk).delete()

    # return the template fragment
    products = request.user.company_own.products.all()
    return render(
        request,
        "catalog/manage/product/htmx/partials/product-list.html",
        {"products": products},
    )


# New views for SELECTION - htmx


class SelectionList(LoginRequiredMixin, ListView):
    template_name = "catalog/product/htmx/products.html"
    model = Product
    context_object_name = "products"

    def get_queryset(self):
        user = self.request.user
        return user.products.all()


def search_products_htmx(request):
    search_text = request.POST.get("search")
    user_products = request.user.products.all()

    results = Product.objects.filter(name__icontains=search_text).exclude(
        name__in=user_products.values_list("name", flat=True)
    )
    context = {"results": results}
    return render(request, "catalog/product/htmx/partials/search-results.html", context)


@login_required
def add_product_to_selection(request):
    user = User.objects.filter(email=request.user.email)
    name = request.POST.get("product-name")

    product = Product.objects.get(name=name)
    request.user.products.add(product)

    products = Product.objects.filter(users__in=user)
    messages.success(request, f"Added {name} to your selection.")
    return render(
        request,
        "catalog/product/htmx/partials/product-list.html",
        {"products": products},
    )


def clear_messages(request):
    return HttpResponse("")


@login_required
@require_http_methods(["DELETE"])
def delete_product_form_selection(request, pk):
    product = Product.objects.get(pk=pk)
    name = product.name
    request.user.products.remove(pk)

    products = request.user.products.all()
    messages.info(request, f"Deleted {name} to your selection.")
    return render(
        request,
        "catalog/product/htmx/partials/product-list.html",
        {"products": products},
    )
