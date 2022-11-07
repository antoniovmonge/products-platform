"""Script to load the products.csv to the database.

To run this script:

docker-compose -f local.yml run --rm django python manage.py runscript load_products_csv
"""
import csv

from django.template.defaultfilters import slugify

from pplatform.catalog.models import Company

CSV_FILENAME = "pplatform/data/products_df_small.csv"
list_company_names = []
companies_to_create = []


def run():
    if not Company.objects.all():
        with open(CSV_FILENAME, encoding="utf8", errors="ignore") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                company_name = row.get("Company")
                if company_name in list_company_names:
                    list_company_names.append(company_name)
                    print("xxx => Repeated")
                else:
                    company = Company(name=company_name, slug=slugify(company_name))
                    companies_to_create.append(company)

                    list_company_names.append(company_name)
                    print(company_name, "added")

            Company.objects.bulk_create(companies_to_create)

    pass
