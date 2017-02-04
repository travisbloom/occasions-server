from django.db import models

from model_utils import Choices

from common.models import BaseModel
from people.models import Person


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
    event_type = models.CharField(max_length=30, choices=EVENT_TYPES, blank=True, null=True)
    date_start = models.DateField()
    # TODO change this to a TimeField once graphene supports it
    time_start = models.CharField(default='', blank=True, max_length=40)
    is_default_event = models.BooleanField(default=True)
    is_reoccuring_yearly = models.BooleanField(default=True)


class AssociatedEventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('event', 'receiving_person')


class AssociatedEvent(BaseModel):
    creating_person = models.ForeignKey(Person, related_name='created_events')
    receiving_person = models.ForeignKey(Person, related_name='received_events')
    event = models.ForeignKey(Event, related_name='created_events')

    objects = AssociatedEventManager()
