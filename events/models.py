import pendulum
from django.db import models

from common.models import BaseModel
from people.models import Person


class EventType(BaseModel):
    name = models.CharField(max_length=255, primary_key=True)
    display_name = models.CharField(max_length=255)
    is_externally_visible = models.BooleanField(blank=True, default=True)

    class Meta:
        db_table = 'app_event_type'

    def __str__(self):
        return self.display_name


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

    class Meta:
        db_table = 'app_event'

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

    class Meta:
        db_table = 'app_event_to_event_type'


class EventDate(models.Model):
    event = models.ForeignKey(Event, related_name='event_dates')
    date_start = models.DateField()

    class Meta:
        db_table = 'app_event_date'

    def __str__(self):
        return "{} on {}".format(self.event, self.date_start)


class AssociatedEvent(BaseModel):
    creating_person = models.ForeignKey(Person, related_name='created_events')
    receiving_person = models.ForeignKey(
        Person, related_name='received_events')
    event = models.ForeignKey(Event, related_name='created_events')

    class Meta:
        db_table = 'app_associated_event'

    def __str__(self):
        return "{}: created by {}, for {}".format(
            self.event,
            self.creating_person,
            self.receiving_person
        )
