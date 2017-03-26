import pendulum
from factory.django import DjangoModelFactory

from events.models import (
    Location,
    AssociatedLocation
)
from people.factories import PersonFactory


class LocationFactory(factory.Factory):

    class Meta:
        model = Location

    street_address_line1 = factory.Sequence(lambda num: "{} Main St.".format(num))
    street_address_line2 = factory.Sequence(lambda num: "Apt #{}".format(num))
    postal_code = factory.Sequence(lambda num: 11111 + num)
    city = factory.Sequence(lambda num: "city_{}".format(num))
    state = factory.Iterator(["CT", "CA", "MA", "DE"])


class AssociatedLocationFactory(factory.Factory):

    class Meta:
        model = AssociatedLocation

    location = factory.SubFactory(LocationFactory)
