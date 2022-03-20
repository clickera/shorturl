from django.contrib.auth.models import User
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Create a superuser"

    def handle(self, *args, **options):
        User.objects.create_superuser("admin", "test@test.com", "qwerty123")