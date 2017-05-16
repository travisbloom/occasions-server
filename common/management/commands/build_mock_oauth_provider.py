from django.core.management import BaseCommand
from oauth2_provider.models import Application

from people.models import User


class Command(BaseCommand):
    help = 'foo'

    def handle(self, *args, **options):
        application = Application(
            authorization_grant_type=Application.GRANT_PASSWORD,
            client_type=Application.CLIENT_CONFIDENTIAL,
            client_id='MOCK_CLIENT_ID',
            client_secret='MOCK_CLIENT_ID',
            name='Occasions',
            user=User.objects.filter(is_superuser=True).first()
        )
        application.save()
