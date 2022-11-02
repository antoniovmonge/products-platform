from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from pplatform.users.models import Company


class Command(BaseCommand):
    """
    Create company in local environment
    `docker-compose -f local.yml run --rm django python manage.py create_local_company`
    """

    help = "Seed database with a Company"

    def handle(self, *args, **options):

        if not settings.DEBUG:
            raise CommandError(
                "This command cannot be run when settings DEBUG == False,"
                + " to guard against accidental use on production."
            )

        if Company.objects.filter(name="Cosentino").exists():
            print("This company already exists.")
        else:
            self.stdout.write("Creating local COMPANY...")
            create_local_company()
            self.stdout.write("Local COMPANY was created")


def create_local_company():
    Company.objects.create(
        name="Cosentino",
        slug="cosentino",
    )
