import time

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from ...tasks import member_celery_test

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        member_celery_test.delay()
