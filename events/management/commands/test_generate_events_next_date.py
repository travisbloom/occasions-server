import pendulum

from common.testing_util.base_test_case import BaseTestCase
from events.factories import EventFactory, EventDateFactory
from events.management.commands.generate_events_next_date import GenerateEventsNextDateCommand


class GenerateEventsNextDateCommandTestCase(BaseTestCase):

    def setUp(self):
        self.base_date = pendulum.Date.today()
        self.date_to_update_off = self.base_date.add(days=3)
        for _ in range(10):
            self.event_to_update = EventFactory(
                post__has_event_date=False,
                is_reoccuring_yearly=True,
                is_default_event=False
            )
            EventDateFactory(
                event=self.event_to_update,
                date_start=self.date_to_update_off
            )
            EventDateFactory(
                event=self.event_to_update,
                date_start=self.base_date.subtract(years=1, days=3)
            )
            EventDateFactory(
                event=self.event_to_update,
                date_start=self.base_date.subtract(years=2, days=3)
            )
        self.event_without_update = EventFactory(
            post__has_event_date=False,
            is_reoccuring_yearly=True,
            is_default_event=False
        )
        EventDateFactory(
            event=self.event_without_update,
            date_start=self.base_date.add(months=3)
        )

    def test__when_calling_generate_next_dates_for_events__properly_updates_relevant_events(self):
        with self.assertNumQueries(4):
            GenerateEventsNextDateCommand.generate_next_dates_for_events()
        self.event_to_update.refresh_from_db()
        self.event_without_update.refresh_from_db()
        self.assertEqual(len(self.event_without_update.event_dates.all()), 1)
        self.assertEqual(len(self.event_to_update.event_dates.all()), 4)
        self.assertEqual(
            self.event_to_update.event_dates.order_by('date_start').last().date_start,
            self.date_to_update_off.add(years=1).date()
        )
