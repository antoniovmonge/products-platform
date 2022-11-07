"""Script to load the products.csv to the database.

To run this script:

docker-compose -f local.yml run --rm django python manage.py runscript load_products_csv
"""
import csv

from django.template.defaultfilters import slugify

from pplatform.catalog.models import Category

CSV_FILENAME = "pplatform/data/products_df_small.csv"
categories_on_list = []
categories_to_create = []


def run():
    if not Category.objects.all():
        with open(CSV_FILENAME, encoding="utf8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                category_name = row.get("Material_type").strip("'[]")
                if category_name in categories_on_list:
                    print("xxx => Repeated")
                else:
                    category = Category(name=category_name, slug=slugify(category_name))
                    categories_to_create.append(category)

                    categories_on_list.append(category_name)
                    print(category_name, "added")

            Category.objects.bulk_create(categories_to_create)

    pass
