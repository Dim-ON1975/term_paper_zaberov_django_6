from django.core.management import BaseCommand

from account.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='zaberov.dv@internet.ru',
            first_name='Admin',
            last_name='Zaberov',
            is_staff=True,
            is_superuser=True,
        )

        user.set_password('123qwe456asd')
        user.save()
