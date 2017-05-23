import factory

from locations.models import (
    Location,
    AssociatedLocation
)
from people.models import Person


def reset_location_factories():
    LocationFactory.reset_sequence()
    AssociatedLocationFactory.reset_sequence()


def generate_initial_location_data(small_sample):
    for person in Person.objects.all():
        for _ in range(2 if small_sample else 5):
            AssociatedLocationFactory(
                person=person
            )


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Location

    id = factory.Sequence(lambda num: num + 1)
    street_address_line1 = factory.Sequence(lambda num: "{} Main St.".format(num))
    street_address_line2 = factory.Sequence(lambda num: "Apt #{}".format(num))
    postal_code = factory.Sequence(lambda num: 11111 + num)
    city = factory.Sequence(lambda num: "city_{}".format(num))
    state = factory.Iterator(["CT", "CA", "MA", "DE"])


class AssociatedLocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AssociatedLocation

    id = factory.Sequence(lambda num: num + 1)
    location = factory.SubFactory(LocationFactory)
