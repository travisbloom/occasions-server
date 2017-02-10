from django.db import models

from model_utils import Choices

from common.models import BaseModel
from people.models import Person

class EventType(BaseModel):
    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)


class EventManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset()
                .prefetch_related('event_types')
        )

# Create your models here.
class Event(BaseModel):
    TYPE_BIRTHDAY = 'birthday'
    TYPE_ANNIVERSARY = 'anniversary'
    TYPE_RELIGIOUS = 'religious'
    TYPE_GEOPOLITICAL = 'geopolitical'

    EVENT_TYPES = Choices(
        TYPE_BIRTHDAY,
        TYPE_ANNIVERSARY,
        TYPE_RELIGIOUS,
        TYPE_GEOPOLITICAL,
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, default='')
    event_types = models.ManyToManyField(EventType, related_name='events')
    date_start = models.DateField()
    time_start = models.TimeField(blank=True, null=True)
    is_default_event = models.BooleanField(default=True)
    is_reoccuring_yearly = models.BooleanField(default=True)

    objects = EventManager()


class AssociatedEventManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset()
                .select_related('event', 'receiving_person')
                .prefetch_related('event__event_types')
        )


class AssociatedEvent(BaseModel):
    creating_person = models.ForeignKey(Person, related_name='created_events')
    receiving_person = models.ForeignKey(Person, related_name='received_events')
    event = models.ForeignKey(Event, related_name='created_events')

    objects = AssociatedEventManager()
