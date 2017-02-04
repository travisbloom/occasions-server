from django.db import models

from common.models import BaseModel
from people.models import Person


# TODO I should normalize location in to City, Country models
class Location(BaseModel):
    street_number = models.CharField(max_length=50)
    street_name = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=25)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)


class PersonLocationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('location')


class PersonLocation(BaseModel):
    person = models.ForeignKey(Person, related_name='locations')
    location = models.ForeignKey(Location)

    objects = PersonLocationManager()

    class Meta:
        unique_together = (
            ('person', 'location'),
        )
