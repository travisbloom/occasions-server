from itertools import cycle

import factory
import pendulum
from django.utils.text import slugify

from events.default_events_data.event_types import event_types_initial_data
from events.default_events_data.us_holidays import get_us_holidays_initial_data
from events.models import (
    EventType,
    Event,
    AssociatedEvent,
    EventDate, EventToEventType)
from people.factories import PersonFactory
from people.models import User


def reset_event_factories():
    EventTypeFactory.reset_sequence()
    EventDateFactory.reset_sequence()
    EventFactory.reset_sequence()
    AssociatedEventFactory.reset_sequence()


def generate_events_initial_testing_data(small_sample):
    today = pendulum.now().date()
    event_types = [
        EventType(pk=key, **value)
        for key, value in sorted(event_types_initial_data.items())
    ]
    EventType.objects.bulk_create(event_types)
    default_events = []
    for key, value in sorted(get_us_holidays_initial_data().items()):
        date_start_fn = value.pop('date_start')
        event_types = value.pop('event_types')
        event = Event(
            slug=key,
            **value,
            is_default_event=True,
            is_reoccuring_yearly=True
        )
        event.save()
        EventToEventType.objects.bulk_create([
            EventToEventType(event_type=event_type, event=event)
            for event_type in EventType.objects.filter(pk__in=event_types)
        ])

        next_date = date_start_fn(today.year)
        next_date_in_a_year = date_start_fn(today.year + 1)
        event_date = EventDate(
            event=event,
            date_start=(
                next_date if
                today.diff(next_date).in_days() > 5
                else next_date_in_a_year if
                today.diff(next_date_in_a_year).in_days() > 5
                else date_start_fn(today.year + 2)
            )
        )
        event_date.save()
        default_events.append(event)

    users = User.objects.all().prefetch_related(
        'person',
        'person__from_relationships',
        'person__from_relationships__to_person'
    )

    default_events_cycle = cycle(default_events)
    for user in users:
        for relationship in user.person.from_relationships.all():
            for _ in range(1 if small_sample else 2):
                event = AssociatedEvent(
                    event=next(default_events_cycle),
                    receiving_person=relationship.to_person,
                    creating_person=user.person,
                )
                event.save()
            # custom event
            event = AssociatedEventFactory(
                receiving_person=relationship.to_person,
                creating_person=user.person,
            )
            event.save()


class EventTypeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = EventType

    name = factory.Sequence(lambda num: "event_type_{}".format(num))
    display_name = factory.LazyAttribute(lambda obj: "{} display name".format(obj.name))


class EventFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Event

    name = factory.Sequence(lambda num: 'event_name_{}'.format(num))
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    is_default_event = False
    is_reoccuring_yearly = True

    @factory.post_generation
    def post(self, create, extracted, has_event_date=True, has_event_type=True, **kwargs):
        if has_event_date:
            EventDateFactory(event=self)
        if has_event_type:
            EventToEventType.objects.bulk_create([
                EventToEventType(event_type=EventType.objects.first(), event=self)
            ])



class EventDateFactory(factory.django.DjangoModelFactory):
    event = factory.SubFactory(EventFactory)
    date_start = factory.Sequence(lambda num: pendulum.now().add(months=num))

    class Meta:
        model = EventDate


class AssociatedEventFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = AssociatedEvent

    creating_person = factory.SubFactory(PersonFactory)
    receiving_person = factory.SubFactory(PersonFactory)
    event = factory.SubFactory(EventFactory)

    @factory.post_generation
    def post(self, create, extracted, has_event_date=False, has_event_type=False, **kwargs):
        if has_event_date:
            EventDateFactory(event=self.event)
        if has_event_type:
            EventToEventType.objects.bulk_create([
                EventToEventType(event_type=EventType.objects.first(), event=self.event)
            ])
