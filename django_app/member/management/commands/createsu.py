from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from config.settings import config

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        username = config['django']['default_superuser']['username']
        email = config['django']['default_superuser']['email']
        password = config['django']['default_superuser']['password']
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
