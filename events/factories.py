import factory
import pendulum

from events.models import (
    EventType,
    Event,
    AssociatedEvent,
)
from people.factories import PersonFactory


def reset_event_factories():
    EventTypeFactory.reset_sequence()
    EventFactory.reset_sequence()
    AssociatedEventFactory.reset_sequence()


class EventTypeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = EventType

    id = factory.Sequence(lambda num: num + 1)
    name = factory.Iterator(["event_type_1", "event_type_2", "event_type_3", "event_type_4"])
    display_name = factory.LazyAttribute(lambda obj: "{} display name".format(obj.name))


class EventFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Event

    id = factory.Sequence(lambda num: num + 1)
    name = factory.Sequence(lambda num: 'event_name_{}'.format(num))
    slug = factory.LazyAttribute(lambda obj: "{}_slug".format(obj.name))
    date_start = factory.Sequence(lambda num: pendulum.Date(2017, 1, 1).add(months=num))
    time_start = factory.Sequence(lambda num: pendulum.Time(13, 30, 30) if num % 2 == 0 else None)
    is_default_event = factory.Sequence(lambda num: num % 2 == 0)
    is_reoccuring_yearly = factory.Sequence(lambda num: num % 2 == 0)

    # @factory.post_generation
    # def event_types(self, create, extracted, **kwargs):
    #     if extracted:
    #         # A list of groups were passed in, use them
    #         for event_type in extracted:
    #             self.event_types.add(event_type)
    #     else:
    #         self.event_types.add(EventType.objects.first())
    #


class AssociatedEventFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = AssociatedEvent

    id = factory.Sequence(lambda num: num + 1)
    creating_person = factory.SubFactory(PersonFactory)
    receiving_person = factory.SubFactory(PersonFactory)
    event = factory.SubFactory(EventFactory)
