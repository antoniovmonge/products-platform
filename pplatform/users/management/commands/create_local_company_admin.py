from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError

from pplatform.users.models import Company

User = get_user_model()


class Command(BaseCommand):
    """
    Create the basic superuser
    `docker-compose -f local.yml run --rm django python manage.py create_instructor`
    """

    help = "Seed database with an 'COMPANY_ADMIN' user"

    def handle(self, *args, **options):

        if not settings.DEBUG:
            raise CommandError(
                "This command cannot be run when settings DEBUG == False,"
                + " to guard against accidental use on production."
            )

        # Local Company_Admin User
        if User.objects.filter(email="company-admin@email.com").exists():
            print("The company-admin local default user already exists.")
        else:
            self.stdout.write("Creating local COMPANY_ADMIN user...")
            create_local_company_admin_user()
            add_user_to_group()
            self.stdout.write("Local COMPANY_ADMIN user was created")


def create_local_company_admin_user():
    User.objects.create_user(
        email="company-admin@email.com",
        password="testpass123",
        company_own=Company.objects.get(name="Cosentino"),
    )
    EmailAddress.objects.create(
        # User is selected in this way because it must be a MaterialsUser Instance
        user=User.objects.get(email="company-admin@email.com"),
        email="company-admin@email.com",
        verified=True,
        primary=True,
    )


def add_user_to_group():
    user = User.objects.get(email="company-admin@email.com")
    group = Group.objects.get(name="company_admin")
    group.user_set.add(user)
