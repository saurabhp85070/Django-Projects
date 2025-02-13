from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Deletes unverified users who signed up more than 24 hours ago.'

    def handle(self, *args, **kwargs):
        #time_threshold = timezone.now() - timedelta(hours=24)
        time_threshold = timezone.now() - timedelta(minutes=5)
        unverified_users = User.objects.filter(is_active=False, date_joined__lt=time_threshold)
        count = unverified_users.count()
        unverified_users.delete()
        self.stdout.write(f"Deleted {count} unverified user(s).")
