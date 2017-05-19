from django.core.management import BaseCommand
from oauth2_provider.models import Application

from events.factories import generate_events_initial_testing_data
from locations.factories import generate_initial_location_data
from people.factories import generate_people_initial_testing_data
from people.models import User
from products.factories import generate_products_initial_data
from transactions.factories import generate_transactions_initial_data


class Command(BaseCommand):
    help = 'foo'

    def handle(self, *args, **options):
        application = Application(
            authorization_grant_type=Application.GRANT_PASSWORD,
            client_type=Application.CLIENT_CONFIDENTIAL,
            client_id='MOCK_CLIENT_ID',
            client_secret='MOCK_CLIENT_SECRET',
            name='Occasions',
            user=User.objects.filter(is_superuser=True).first()
        )
        application.save()

        generate_people_initial_testing_data(small_sample=True)
        generate_initial_location_data(small_sample=True)
        generate_events_initial_testing_data(small_sample=True)
        generate_products_initial_data(small_sample=True)
        generate_transactions_initial_data(small_sample=True)

