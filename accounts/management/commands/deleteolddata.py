from django.core.management.base import BaseCommand, CommandError
from accounts.models import authTokenModel
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Delete objects older than 1 minute'
    def handle(self, *args, **options):
        authTokenModel.objects.filter(publishing_time__lte=datetime.now()-timedelta(minutes=1)).delete()
        self.stdout.write('Deleted objects older than 1 minute')