import factory
import pendulum

from events.models import (
    EventType,
    Event,
    AssociatedEvent,
    EventDate)
from people.factories import PersonFactory


def reset_event_factories():
    EventTypeFactory.reset_sequence()
    EventFactory.reset_sequence()
    AssociatedEventFactory.reset_sequence()


class EventTypeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = EventType

    name = factory.Sequence(lambda num: "event_type_{}".format(num))
    display_name = factory.LazyAttribute(lambda obj: "{} display name".format(obj.name))


class EventFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Event

    id = factory.Sequence(lambda num: num + 1)
    name = factory.Sequence(lambda num: 'event_name_{}'.format(num))
    slug = factory.LazyAttribute(lambda obj: "{}_slug".format(obj.name))
    is_default_event = factory.Sequence(lambda num: num % 2 == 0)
    is_reoccuring_yearly = factory.Sequence(lambda num: num % 2 == 0)

    @factory.post_generation
    def post(self, create, extracted, has_event_date=True, has_event_type=True, **kwargs):
        if has_event_date:
            EventDateFactory(event=self)
        if has_event_type:
            self.event_types.add(EventType.objects.first() or EventTypeFactory())



class EventDateFactory(factory.django.DjangoModelFactory):
    event = factory.SubFactory(EventFactory)
    date_start = factory.Sequence(lambda num: pendulum.now().add(months=num))

    class Meta:
        model = EventDate


class AssociatedEventFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = AssociatedEvent

    id = factory.Sequence(lambda num: num + 1)
    creating_person = factory.SubFactory(PersonFactory)
    receiving_person = factory.SubFactory(PersonFactory)
    event = factory.SubFactory(EventFactory)

    @factory.post_generation
    def post(self, create, extracted, has_event_date=False, has_event_type=False, **kwargs):
        if has_event_date:
            EventDateFactory(event=self.event)
        if has_event_type:
            self.event.event_types.add(EventType.objects.first())
