from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

from .models import Product


def paginate_products(request, projects, results):
    page = request.GET.get("page")
    paginator = Paginator(projects, results)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    leftIndex = int(page) - 1

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = int(page) + 1

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, projects


def search_products(request):
    search_query = ""

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    products = Product.objects.distinct().filter(
        Q(name__icontains=search_query)
        | Q(company__name__icontains=search_query)  # |
        # Q(product_type__name__icontains=search_query) |
        # Q(material_types__name__icontains=search_query)
    )

    return products, search_query
