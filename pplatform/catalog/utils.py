from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

from .models import Product


def paginate_products(request, products, results):
    page = request.GET.get("page")
    paginator = Paginator(products, results)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        products = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        products = paginator.page(page)

    leftIndex = int(page) - 2

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = int(page) + 5

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, products


def search_products(request):
    search_query = ""

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    products = Product.published.distinct().filter(
        Q(name__icontains=search_query)
        | Q(description__icontains=search_query)
        | Q(company__name__icontains=search_query)
        | Q(category__name__icontains=search_query)  # |
        # Q(material_types__name__icontains=search_query)
    )

    return products, search_query
