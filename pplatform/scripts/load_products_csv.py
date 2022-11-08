"""Script to load the products.csv to the database.

To run this script:

docker-compose -f local.yml run --rm django python manage.py runscript load_products_csv
"""

import csv
from datetime import datetime

from django.template.defaultfilters import slugify

from pplatform.catalog.models import Category, Company, Product

CSV_FILENAME = "pplatform/data/products_df.csv"

product_names_list = []
create_array_products = []


def run():
    if not Product.objects.all():
        with open(CSV_FILENAME, encoding="utf8", errors="ignore") as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                product_name = row.get("NAME")
                category_name = row.get("Material_type").strip("'[]")
                image_new_path = row.get("image_path")[7:]
                product = Product(
                    name=product_name,
                    slug=slugify(f"{product_name}{datetime.now().time()}"),
                    company=Company.objects.get(name=row.get("Company")),
                    category=Category.objects.get(name=category_name),
                    status="PB",  # Published
                    image=f"products/{image_new_path}",
                )
                if product.name in product_names_list:
                    print("already in db")
                else:
                    product_names_list.append(product.name)
                    create_array_products.append(product)
                    print(product.name)

            Product.objects.bulk_create(create_array_products)

    pass
