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

                    try:
                        carbon_sorting = row.get("carbon_sorting")
                    except ValueError:
                        carbon_sorting = None

                    try:
                        water_use_kg = float(row.get("water_use_kg"))
                    except ValueError:
                        water_use_kg = None

                    try:
                        use_and_maintenance = float(row.get("use_and_maintenance"))
                    except ValueError:
                        use_and_maintenance = None

                    try:
                        end_of_life = float(row.get("end_of_life"))
                    except ValueError:
                        end_of_life = None

                    try:
                        recycled_content = float(row.get("recycled_content"))
                    except ValueError:
                        recycled_content = None
                    try:
                        recyclable_content = float(row.get("recyclable_content"))
                    except ValueError:
                        recyclable_content = None
                    try:
                        reuse_potential = float(row.get("reuse_potential"))
                    except ValueError:
                        reuse_potential = None
                    try:
                        odp = float(row.get("odp"))
                    except ValueError:
                        odp = None
                    try:
                        manufacturing = float(row.get("manufacturing"))
                    except ValueError:
                        manufacturing = None
                    try:
                        on_site_installation = float(row.get("on_site_installation"))
                    except ValueError:
                        on_site_installation = None
                    try:
                        energy_recovery_possibility = float(
                            row.get("energy_recovery_possibility")
                        )
                    except ValueError:
                        energy_recovery_possibility = None

                    product_detail = ProductDetail(
                        product=Product.objects.get(name=product_name),
                        declared_unit=row.get("declared_unit"),
                        total_co2e_kg_mf=total_co2e_kg_mf,
                        total_biogenic_co2e=total_biogenic_co2e,
                        carbon_sorting=carbon_sorting,
                        water_use_kg=water_use_kg,
                        use_and_maintenance=use_and_maintenance,
                        end_of_life=end_of_life,
                        recycled_content=recycled_content,
                        recyclable_content=recyclable_content,
                        reuse_potential=reuse_potential,
                        odp=odp,
                        manufacturing=manufacturing,
                        on_site_installation=on_site_installation,
                        energy_recovery_possibility=energy_recovery_possibility,
                    )
                    list_product_details.append(product_detail)
                    print("details for: ", product_detail.product)

            ProductDetail.objects.bulk_create(list_product_details)

    pass
