from django.db import models

from common.models import BaseModel
from people.models import Person


# TODO I should normalize location in to City, Country models
class Location(BaseModel):
    street_address_line1 = models.CharField(max_length=455)
    street_address_line2 = models.CharField(
        max_length=255, default='', blank=True)
    postal_code = models.CharField(max_length=25)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='USA', blank=True)

    class Meta:
        db_table = 'app_location'

    def __str__(self):
        return "{}".format(self.display_name)

    @property
    def display_name(self):
        return "{street_address_line1}{street_address_line2}, {city} {state} {postal_code}".format(
            street_address_line1=self.street_address_line1,
            street_address_line2=" {}".format(
                self.street_address_line2) if self.street_address_line2 else "",
            city=self.city,
            state=self.state,
            postal_code=self.postal_code)


class AssociatedLocation(BaseModel):
    person = models.ForeignKey(Person, related_name='associated_locations')
    location = models.ForeignKey(Location)

    class Meta:
        db_table = 'app_associated_location'
        unique_together = (
            ('person', 'location'),
        )

    def __str__(self):
        return "{} ({})".format(self.location, self.person)
