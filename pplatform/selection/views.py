from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from pplatform.catalog.models import Product

from .forms import SelectionAddProductForm
from .selection import Selection


@require_POST
def selection_add(request, product_id):
    selection = Selection(request)
    product = get_object_or_404(Product, id=product_id)
    form = SelectionAddProductForm(request.POST)
    if form.is_valid():
        # cd = form.cleaned_data
        selection.add(product=product)
    # return redirect("selection:selection_detail")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@require_POST
def selection_remove(request, product_id):
    selection = Selection(request)
    product = get_object_or_404(Product, id=product_id)
    selection.remove(product)
    # return redirect("selection:selection_detail")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def selection_detail(request):
    selection = Selection(request)
    return render(request, "selection/detail.html", {"selection": selection})
