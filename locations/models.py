from django.db import models

from common.models import BaseModel
from people.models import Person


# TODO I should normalize location in to City, Country models
class Location(BaseModel):
    street_address_line1 = models.CharField(max_length=455)
    street_address_line2 = models.CharField(max_length=255, default='', blank=True)
    postal_code = models.CharField(max_length=25)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='USA', blank=True)


class AssociatedLocationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('location')


class AssociatedLocation(BaseModel):
    person = models.ForeignKey(Person, related_name='associated_locations')
    location = models.ForeignKey(Location)

    objects = AssociatedLocationManager()

    class Meta:
        unique_together = (
            ('person', 'location'),
        )
