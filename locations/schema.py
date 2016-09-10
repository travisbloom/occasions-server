from graphene import relay, ObjectType, Mutation, String, Field
from graphene.contrib.django.filter import DjangoFilterConnectionField
from graphene.contrib.django.types import DjangoNode

from .models import Location, PersonLocation


class LocationNode(DjangoNode):
    class Meta:
        model = Location


class PersonLocationNode(DjangoNode):
    class Meta:
        model = PersonLocation
        filter_fields = ['person']


class Query(ObjectType):
    location = relay.NodeField(LocationNode)
    locations = DjangoFilterConnectionField(LocationNode)

    person_location = relay.NodeField(PersonLocationNode)
    person_locations = DjangoFilterConnectionField(PersonLocationNode)

    class Meta:
        abstract = True
