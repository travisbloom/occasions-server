import pendulum
from django.core.management.base import BaseCommand

from events.default_events_data.us_holidays import get_us_holidays_initial_data
from events.models import Event, EventDate


class Command(BaseCommand):
    help = 'Generate the an EventDate for all events that are about to pass their next date'

    def handle(self, *args, **options):
        self.generate_next_dates_for_events()
        self.generate_next_dates_for_default_events()

    @staticmethod
    def generate_next_dates_for_default_events():
        us_holidays = get_us_holidays_initial_data()
        events = (
            Event.objects
                .filter(
                is_default_event=True,
                is_reoccuring_yearly=True
            )
                .exclude(event_dates__date_start__gte=pendulum.Date.today().add(weeks=1)) \
                .prefetch_related('event_dates')
        )
        event_dates_to_create = []
        for event in events:
            furthest_out_event = sorted(
                event.event_dates.all(),
                key=lambda event_date: event_date.date_start,
                reverse=True
            )[0]
            event_date = EventDate(
                event=event,
                date_start=us_holidays[event.slug]['date_start'](
                    furthest_out_event.date_start.year + 1
                )
            )
            event_dates_to_create.append(event_date)
        EventDate.objects.bulk_create(event_dates_to_create, batch_size=200)

    @staticmethod
    def generate_next_dates_for_events():

        events = (
            Event.objects
                .filter(
                is_default_event=False,
                is_reoccuring_yearly=True
            )
                .exclude(event_dates__date_start__gte=pendulum.Date.today().add(weeks=1)) \
                .prefetch_related('event_dates')
        )
        event_dates_to_create = []
        for event in events:
            furthest_out_event = sorted(
                event.event_dates.all(),
                key=lambda event_date: event_date.date_start,
                reverse=True
            )[0]

            event_date = EventDate(
                event=event,
                date_start=pendulum.Date.instance(furthest_out_event.date_start).add(years=1)
            )
            event_dates_to_create.append(event_date)
        EventDate.objects.bulk_create(event_dates_to_create, batch_size=200)
