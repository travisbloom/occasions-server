from django.db import models
import pendulum

from common.models import BaseModel
from people.models import Person


class EventType(BaseModel):
    name = models.CharField(max_length=255, primary_key=True)
    display_name = models.CharField(max_length=255)
    is_externally_visible = models.BooleanField(blank=True, default=True)

    def __str__(self):
        return self.display_name


class EventManager(models.Manager):

    def get_queryset(self):
        return (
            super().get_queryset()
            .prefetch_related('event_types')
        )


class Event(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, default='')
    event_types = models.ManyToManyField(
        EventType,
        through='EventToEventType',
        related_name='events'
    )
    is_default_event = models.BooleanField(default=True)
    is_reoccuring_yearly = models.BooleanField(default=True)

    objects = EventManager()

    def __str__(self):
        return self.name

    @property
    def next_date(self):
        return self.event_dates.filter(
            date_start__gte=pendulum.now().subtract(days=1)
        ).first()


class EventToEventType(BaseModel):
    event = models.ForeignKey(Event)
    event_type = models.ForeignKey(EventType)


class EventDate(models.Model):
    event = models.ForeignKey(Event, related_name='event_dates')
    date_start = models.DateField()

    def __str__(self):
        return "{} on {}".format(self.event, self.date_start)


class AssociatedEventManager(models.Manager):

    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related('event', 'receiving_person')
            .prefetch_related('event__event_types')
        )


class AssociatedEvent(BaseModel):
    creating_person = models.ForeignKey(Person, related_name='created_events')
    receiving_person = models.ForeignKey(
        Person, related_name='received_events')
    event = models.ForeignKey(Event, related_name='created_events')

    objects = AssociatedEventManager()

    def __str__(self):
        return "{}: created by {}, for {}".format(
            self.event,
            self.creating_person,
            self.receiving_person
        )
