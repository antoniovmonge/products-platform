"""Script to load the products.csv to the database.

To run this script:

docker-compose -f local.yml run --rm django python manage.py runscript load_products_csv
"""

import csv

from django.template.defaultfilters import slugify

from pplatform.catalog.models import Category, Company, Product

CSV_FILENAME = "pplatform/data/products_df_small.csv"

create_array_products = []


def run():
    if not Product.objects.all():
        with open(CSV_FILENAME, encoding="utf8", errors="ignore") as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                product_name = row.get("NAME")
                category_name = row.get("Material_type").strip("'[]")
                product = Product(
                    name=product_name,
                    slug=slugify(product_name),
                    company=Company.objects.get(name=row.get("Company")),
                    category=Category.objects.get(name=category_name),
                    status="PB",  # Published
                )
                create_array_products.append(product)
                print(product.name)

            Product.objects.bulk_create(create_array_products)

    pass
