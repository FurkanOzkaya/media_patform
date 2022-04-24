from django.contrib.auth import get_user_model

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        User = get_user_model()
        if not list(User.objects.filter(username="admin")):
            User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
