from django.db import models

from occasions.models import BaseModel
from people.models import Person

#TODO I should normalize location in to City, Country models
class Location(BaseModel):
    street_number = models.CharField(max_length=50)
    street_name = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=25)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)


class PersonLocation(BaseModel):
    person = models.ForeignKey(Person, related_name='locations')
    location = models.ForeignKey(Location)

    class Meta:
        unique_together = (
            ('person', 'location'),
        )
