from django.conf import settings

from pplatform.catalog.models import Product


class Selection:
    def __init__(self, request):
        """
        Initialize Selection of Products
        """
        self.session = request.session
        selection = self.session.get(settings.SELECTION_SESSION_ID)
        if not selection:
            # save an empty selection in the session
            selection = self.session[settings.SELECTION_SESSION_ID] = {}
        self.selection = selection

    def add(self, product):
        """
        Add a product to the selection.
        """
        product_id = str(product.id)
        if product_id not in self.selection:
            self.selection[product_id] = {"name": product.name, "slug": product.slug}
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the selection.
        """
        product_id = str(product.id)
        if product_id in self.selection:
            del self.selection[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the selection and get products
        from the database.
        """
        product_ids = self.selection.keys()
        # get the product objects and add them to the selection
        products = Product.objects.filter(id__in=product_ids)
        selection = self.selection.copy()
        for product in products:
            selection[str(product.id)]["product"] = product
        for item in selection.values():
            item["name"] = item["name"]
            yield item

    def __len__(self):
        """
        Count all items in the selection
        """
        return len(self.selection)

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
