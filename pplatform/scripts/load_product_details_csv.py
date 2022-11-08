"""Script to load the products.csv to the database.

To run this script:

docker-compose -f local.yml run --rm django python manage.py runscript load_products_csv
"""

import csv

from pplatform.catalog.models import Product, ProductDetail

CSV_FILENAME = "pplatform/data/products_df.csv"

product_names_list = []
list_product_details = []


def run():
    if not ProductDetail.objects.all():
        with open(CSV_FILENAME, encoding="utf8") as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                product_name = row.get("NAME")
                # Fix the bad csv
                if product_name in product_names_list:
                    print("duplicated")
                else:
                    product_names_list.append(product_name)
                    try:
                        total_co2e_kg_mf = float(row.get("total_co2e_kg_mf"))
                    except ValueError:
                        total_co2e_kg_mf = None

                    try:
                        total_biogenic_co2e = float(row.get("total_biogenic_co2e"))
                    except ValueError:
                        total_biogenic_co2e = None

                    product_detail = ProductDetail(
                        product=Product.objects.get(name=product_name),
                        declared_unit=row.get("declared_unit"),
                        total_co2e_kg_mf=total_co2e_kg_mf,
                        total_biogenic_co2e=total_biogenic_co2e,
                    )
                    list_product_details.append(product_detail)
                    print("details for: ", product_detail.product)

            ProductDetail.objects.bulk_create(list_product_details)

    pass
